def create_var():
    print('creating')
    return 2


class A():
    def __init__(self):
        self.servo = 1
        self.__servo = create_var()


class B(A):
    def __init__(self):
        super(B, self).__init__()


a = A()
b = B()
print(a.__servo)

