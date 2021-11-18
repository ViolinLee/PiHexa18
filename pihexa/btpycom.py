# btpycom.py
# Python 2.7 version
# Author: AP

"""
Library that implements a event-based Bluetooth client-server system in contrast to the standard stream-based systems.
Messages are sent in byte blocks (may be UTF-8 or ASCII encoded strings). The null charactor is used as
End-of-Transmission indicator. The Bluetooth RFCOMM protocol is used.

Dependencies: Widcomm packages (Bluez)
"""

from threading import Thread
import time
import sys
from bluetooth import *

BTCOM_VERSION = "1.00 - March 20, 2017"
TCPCOM_VERSION = "UNKNOW"


# ================================== Server ================================
# ---------------------- class BTServer ------------------------
class BTServer(Thread):
    """
    Class that represents a Bluetooth server.
    """
    isVerbose = False
    CONNECTED = "CONNECTED"
    LISTENING = "LISTENING"
    TERMINATED = "TERMINATED"
    MESSAGE = "MESSAGE"

    def __init__(self, serviceName, stateChanged, isVerbose=False):
        """
        Creates a Bluetooth server that listens for a connecting client.
        The server runs in its own thread, so the
        constructor returns immediately. State changes invoke the callback
        onStateChanged(state, msg) where state is one of the following strings:
        "LISTENING", "CONNECTED", "MESSAGE", "TERMINATED". msg is a string with
        further information: LISTENING: empty, CONNECTED: connection url, MESSAGE:
        message received, TERMINATED: empty. The server uses an internal handler
        thread to detect incoming messages.
        @param serviceName: the service name the server is exposing
        @param stateChanged: the callback function to register
        @param isVerbose: if true, debug messages are written to System.out, default: False
        """
        Thread.__init__(self)
        self.serviceName = serviceName
        self.stateChanged = stateChanged
        BTServer.isVerbose = isVerbose
        self.isClientConnected = False
        self.clientSocket = None
        self.start()

    def run(self):
        BTServer.debug("BTServer thread started")
        self.serverSocket = BluetoothSocket(RFCOMM)
        BTServer.debug("Socket created")
        try:
            self.serverSocket.bind(("", PORT_ANY))
        except socket.error as msg:
            print("Fatal error while creating BTServer: Bind failed.", msg[0], msg[1])
            sys.exit()
        BTServer.debug("Socket bind successful ")
        try:
            self.serverSocket.listen(1)
        except:
            print("Fatal error while BTServer enters listening mode.")
            sys.exit()

        BTServer.debug("Socket listening engaged.")
        self.port = self.serverSocket.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.serverSocket, self.serviceName,
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE])
        BTServer.debug("Service " + self.serviceName + " is exposed")
        BTServer.debug("Bluetooth server listening at channel " + str(self.port))
        try:
            self.stateChanged(BTServer.LISTENING, str(self.port))
        except Exception as e:
            print("Caught exception in BTServer.LISTENING:", e)

        self.serverSocket.settimeout(30)
        self.isServerRunning = True
        self.isTerminating = False
        while self.isServerRunning:
            isListening = True
            while isListening:
                try:
                    BTServer.debug("Calling accept() with timeout = 30 s")
                    self.clientSocket, self.clientInfo = self.serverSocket.accept()  # blocking
                    BTServer.debug(
                        "Accepted connection from " + self.clientInfo[0] + " at channel " + str(self.clientInfo[1]))
                    isListening = False
                except:
                    if self.isTerminating:
                        break
                    pass
            if self.isTerminating:
                self.isServerRunning = False
                break
            BTServer.debug("Accepted connection from " + self.clientInfo[0] + " at channel " + str(self.clientInfo[1]))
            if self.isClientConnected:  # another client is connected
                BTServer.debug("Returning form blocking accept(). Client refused")
                self.clientSocket.close()
                isListening = True
                continue
            self.isClientConnected = True
            self.socketHandler = ServerHandler(self)
            self.socketHandler.start()
            try:
                self.stateChanged(BTServer.CONNECTED, self.clientInfo)
            except Exception as e:
                print("Caught exception in BTServer.CONNECTED:", e)
        if self.clientSocket != None:
            self.clientSocket.close()
        self.serverSocket.close()
        self.isClientConnected = False
        try:
            self.stateChanged(BTServer.TERMINATED, "")
        except Exception as e:
            print("Caught exception in BTServer.TERMINATED:", e)
        self.isServerRunning = False
        BTServer.debug("BTServer thread terminated")

    def disconnect(self):
        """
        Closes the connection with the client and enters
        the LISTENING state
        """
        BTServer.debug("Calling Server.disconnect()")
        if self.isClientConnected:
            self.isClientConnected = False
            try:
                self.stateChanged(BTServer.LISTENING, str(self.port))
            except Exception as e:
                print("Caught exception in BTServer.LISTENING:", e)
            BTServer.debug("Close client socket now")
            self.clientSocket.close()

    def sendMessage(self, msg):
        """
        Sends the information msg to the client (as String, the character \0 (ASCII 0) serves as end of
        string indicator, it is transparently added and removed)
        @param msg: the message to send
        """
        BTServer.debug("sendMessage() with msg: " + msg)
        if not self.isClientConnected:
            BTServer.debug("Not connected")
            return
        self.clientSocket.sendall(msg + "\0")

    def terminate(self):
        """
        Terminates the server (finishs the listening state).
        """
        BTServer.debug("Calling terminate()")
        self.isTerminating = True

    def isConnected(self):
        """
        Returns True, if a client is connected to the server.
        @return: True, if the communication link is established
        """
        return self.isClientConnected

    def isTerminated(self):
        """
        Returns True, if the server is in TERMINATED state.
        @return: True, if the server thread is terminated
        """
        return self.isServerRunning

    @staticmethod
    def debug(msg):
        if BTServer.isVerbose:
            print("   BTServer-> " + msg)

    @staticmethod
    def getVersion():
        """
        Returns the library version.
        @return: the current version of the library
        """
        return BTCOM_VERSION


# ---------------------- class ServerHandler ------------------------
class ServerHandler(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        BTServer.debug("ServerHandler started")
        bufSize = 4096
        try:
            data = bytearray()
            while True:
                inBlock = True
                while inBlock:
                    reply = self.server.clientSocket.recv(bufSize)
                    data.extend(reply)
                    if b'\0' in data:  # 注：C/C++中'\0'为字符串结尾
                        junk = data.split(b'\0')  # more than 1 message may be received if
                        # transfer is fast. data: xxxx\0yyyyy\0zzz\0
                        for i in range(len(junk) - 1):
                            BTServer.debug("Received message: " + str(junk[i]) + " len: " + str(len(junk[i])))
                            if len(junk[i]) > 0:
                                try:
                                    self.server.stateChanged(BTServer.MESSAGE, str(junk[i]))
                                except Exception as e:
                                    print("Caught exception in BTServer.MESSAGE:", e)
                            else:
                                BTServer.debug("Got empty message as EOT")
                                BTServer.debug("ServerHandler thread terminated")
                                self.server.disconnect()
                                return
                        inBlock = False
                        data = bytearray(junk[len(junk) - 1])  # remaining bytes
        except:  # Happens if client is disconnecting
            BTServer.debug("Exception from blocking conn.recv(), Msg: " + str(sys.exc_info()[0]) + \
                           " at line # " + str(sys.exc_info()[-1].tb_lineno))

        self.server.disconnect()
        BTServer.debug("ServerHandler thread terminated")


# ================================== Client ================================
# -------------------------------- class BTClient --------------------------
class BTClient:
    """
    Class that represents a Bluetooth socket based client. To connect a client via Bluetooth,
    the Bluetooth MAC address (12 hex characters) and the Bluetooth port (channel) of the server
    must be known (server info). All other server information is irrelevant (Bluetooth friendly name, Bluetooth service name),
    but the server info may be retrieved by a Bluetooth search from the server name or the service name.
    """
    isVerbose = False
    CONNECTING = "CONNECTING"
    CONNECTION_FAILED = "CONNECTION_FAILED"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    MESSAGE = "MESSAGE"

    def __init__(self, stateChanged, isVerbose=False):
        """
        Creates a Bluetooth client prepared for a connection with a
        BTServer. The client uses an internal handler thread to detect incoming messages.
        State changes invoke the callback
        onStateChanged(state, msg) where state is one of the following strings:
        "CONNECTING", "CONNECTION_FAILED", "DISCONNECTED", "MESSAGE". msg is a string with
        additional information: CONNECTING: serverInfo, CONNECTED: serverInfo,
        CONNECTION_FAILED: serverInfo, DISCONNECTED: empty, MESSAGE: message received
        @param stateChanged: the callback function to register
        @param isVerbose: if true, debug messages are written to System.out
        """
        self.isClientConnected = False
        self.isClientConnecting = False
        self.serviceName = ""
        self.macAddress = ""
        self.channel = -1
        self.stateChanged = stateChanged
        self.inCallback = False
        BTClient.isVerbose = isVerbose

    def sendMessage(self, msg):
        """
        Sends the information msg to the server (as String, the character \0
        (ASCII 0) serves as end of string indicator, it is transparently added
        and removed).
        @param msg: the message to send
        """
        BTClient.debug("sendMessage() with msg = " + msg)
        if not self.isClientConnected:
            BTClient.debug("sendMessage(): Connection closed.")
            return
        try:
            self.clientSocket.sendall(msg + "\0")
        except:
            BTClient.debug("sendMessage(): Connection reset by peer.")
            self.disconnect(None)

    def connect(self, serverInfo, timeout):
        """
        Performs a connection trial to the server with given serverInfo. If the connection trial fails,
        it is repeated until the timeout is reached.
        @param serverInfo: a tuple ("nn:nn:nn:nn:nn:nn", channel) with the Bluetooth MAC address string
        (12 hex characters, upper or lower case, separated by :) and  Bluetooth channel (integer),
        e.g. ("B8:27:EB:04:A6:7E", 1)
        """
        maxNbRetries = 10
        try:
            self.stateChanged(BTClient.CONNECTING, serverInfo)
        except Exception as e:
            print("Caught exception in BTClient.CONNECTING:", e)
        nbRetries = 0
        startTime = time.time()
        rc = False
        while (not rc) and time.time() - startTime < timeout and nbRetries < maxNbRetries:
            BTClient.debug("Starting connect #" + str(nbRetries))
            rc = self._connect(serverInfo)
            if rc == False:
                nbRetries += 1
                time.sleep(3)
        BTClient.debug("connect() returned " + str(rc) + " after " + str(nbRetries) + " retries")
        if rc:
            BTClient.debug("Connection established")
            self.isClientConnected = True
            try:
                self.stateChanged(BTClient.CONNECTED, serverInfo)
            except Exception as e:
                print("Caught exception in BTClient.CONNECTED:", e)
            ClientHandler(self)
        else:
            BTClient.debug("Connection failed")
            self.isClientConnected = False
            try:
                self.stateChanged(BTClient.CONNECTION_FAILED, serverInfo)
            except Exception as e:
                print("Caught exception in BTClient.CONNECTION_FAILED:", e)
        return rc

    def _connect(self, serverInfo):
        self.macAddress = serverInfo[0]
        self.channel = serverInfo[1]
        self.clientSocket = BluetoothSocket(RFCOMM)
        try:
            self.clientSocket.connect((self.macAddress, self.channel))
        except:
            BTClient.debug("Exception from clientSocket.connect(). \n      Msg: " + str(sys.exc_info()[0]) +
                           str(sys.exc_info()[1]))
            return False
        return True

    def findServer(self, serverName, timeout):
        """
        Perform a device inquiry for the given server name.
        The Bluetooth channel is not inquired, always assumed to be 1.
        @param timeout: the maximum time in seconds to search
        @return: a tuple with the Bluetooth MAC address and the Bluetooth channel 1; None if inquiry failed
        """
        self.serverName = serverName
        nbRetries = 0
        startTime = time.time()
        rc = None
        while rc == None and time.time() - startTime < timeout:
            BTClient.debug("Starting inquire #" + str(nbRetries))
            rc = self._inquireMAC()
            if rc == None:
                nbRetries += 1
                time.sleep(2)
        BTClient.debug("findServer returned() " + str(rc) + " after " + str(nbRetries) + " retries")
        return rc

    def _inquireMAC(self):
        BTClient.debug("Calling discover_devices()")
        devices = discover_devices(duration=10, lookup_names=True)
        BTClient.debug("discover_devices() returned: " + str(devices))
        for device in devices:
            if device[1] == self.serverName:
                return (device[0], 1)
        return None

    def findService(self, serviceName, timeout):
        """
        Perform a service inquiry for the given service name.
        @param timeout: the maximum time in seconds to search
        @return: a tuple with the Bluetooth MAC address and the Bluetooth channel; None if inquiry failed
        """
        self.serviceName = serviceName
        nbRetries = 0
        startTime = time.time()
        rc = None
        while rc == None and time.time() - startTime < timeout:
            BTClient.debug("Client: trying to inquire #" + str(nbRetries))
            rc = self._inquireService()
            if rc == None:
                nbRetries += 1
                time.sleep(2)
        return rc

    def _inquireService(self):
        BTClient.debug("Calling find_service() with service name: " + self.serviceName)
        services = find_service(name=self.serviceName, uuid=SERIAL_PORT_CLASS)
        if services == []:
            BTClient.debug("find_service() failed to detect service")
            return None
        BTClient.debug("find_service() returned: " + str(services))
        for i in range(len(services)):  # More than one device could expose same service name
            service = services[i]
            self.macAddress = service["host"]
            self.channel = service["port"]
            BTClient.debug("Inquiry returned successfully with server: " +
                           self.macAddress + ", service name: " + self.serviceName + " at channel " + str(self.channel))
            return self.macAddress, self.channel
        return None

    def disconnect(self, endOfTransmission=""):
        """
        Closes the connection with the server. The endOfTransmission message is sent to the
        server to notify disconnection.
        @param endOfTransmission: the message sent to the server (appended by \0)
        Default: "", None: no notification sent
        """
        if self.inCallback:  # two threads may call in rapid sequence
            return
        self.inCallback = True
        BTClient.debug("Client.disconnect()")
        if not self.isClientConnected:
            BTClient.debug("Connection already closed")
            return
        if endOfTransmission != None:
            self.sendMessage(endOfTransmission)
        self.isClientConnected = False
        BTClient.debug("Closing socket")
        self.clientSocket.close()
        try:
            self.stateChanged(BTClient.DISCONNECTED, "")
        except Exception as e:
            print("Caught exception in BTClient.DISCONNECTED:", e)
        self.inCallback = False

    def isConnected(self):
        """
        Returns True of client is connnected to the server.
        @return: True, if the connection is established
        """
        return self.isClientConnected

    def getMacAddress(self):
        """
        Returns the Bluetooth MAC address in format "nn:nn:nn:nn:nn::nn"
        """
        return self.macAddress

    def getChannel(self):
        """
        Returns the Bluetooth channel.
        """
        return self.channel

    @staticmethod
    def debug(msg):
        if BTClient.isVerbose:
            print("   BTClient-> " + msg)

    @staticmethod
    def getVersion():
        """
        Returns the library version.
        @return: the current version of the library
        """
        return TCPCOM_VERSION


# -------------------------------- class ClientHandler ---------------------------
class ClientHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.start()

    def run(self):
        BTClient.debug("ClientHandler thread started")
        bufSize = 4096
        try:
            data = bytearray()
            while True:
                inBlock = True
                while inBlock:
                    reply = self.client.clientSocket.recv(bufSize)
                    data.extend(reply)
                    if b'\0' in data:
                        junk = data.split(b'\0')  # more than 1 message may be received if
                        # transfer is fast. data: xxxx\0yyyyy\0zzz\0
                        for i in range(len(junk) - 1):
                            BTClient.debug("Received message: " + str(junk[i]) + " len: " + str(len(junk[i])))
                            if len(junk[i]) > 0:
                                try:
                                    self.client.stateChanged(BTServer.MESSAGE, str(junk[i]))
                                except Exception as e:
                                    print("Caught exception in BTClient.MESSAGE:", e)
                        inBlock = False
                        data = bytearray(junk[len(junk) - 1])  # remaining bytes
        except:  # Happens if client is disconnecting
            BTClient.debug("Exception from blocking conn.recv(), Msg: " + str(sys.exc_info()[0]))
            self.client.disconnect()
        BTClient.debug("ClientHandler thread finished")
