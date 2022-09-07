import argparse
import pihexa.config as config
import kinematics
from lib import point_rotate_z, matrix_mul
from paths import *


def verify_points(pt):
    angles = kinematics.ik(pt)

    ok = True
    failed = []
    for i, angle in enumerate(angles):
        if angle < config.angleLimitation[i][0] or angle > config.angleLimitation[i][1]:
            ok = False
            failed.append((i, angle))

    return ok, failed


def verify_path(path, params):
    data, mode, _, _ = params
    print("Verifying {}...".format(path))

    all_ok = True
    if mode == "shift":
        # data: float[6][N][3]
        assert (len(data) == 6)

        for i in range(len(data[0])):
            for j in range(6):
                pt = [config.default_position[j][k] - config.mount_position[j][k] + data[j][i][k] for k in range(3)]
                pt = point_rotate_z(pt, config.default_angle[j])
                ok, failed = verify_points(pt)

                if not ok:
                    print("{}, {} failed: {}".format(i, j, failed))
                    all_ok = False

    elif mode == "matrix":
        # data: np.matrix[N]
        for i in range(len(data)):
            for j in range(6):
                pt = matrix_mul(data[i], config.default_position[j])
                for k in range(3):
                    pt[k] -= config.mount_position[j][k]
                pt = point_rotate_z(pt, config.default_angle[j])

                ok, failed = verify_points(pt)

                if not ok:
                    print("{}, {} failed: {}".format(i, j, failed))
                    all_ok = False

    return all_ok


def generate_py_body(path_name, path_params):
    path_array, mode, duration, entries = path_params
    result = "\n{}_paths = [".format(path_name)
    backspace_num = len(result) - 1

    if mode == "shift":
        # path_array: float[6][N][3] (a deque list with length of 6 and shape of (N. 3))
        # out_put path: float[N][6][3]
        assert(len(path_array) == 6)
        count = len(path_array[0])
        for i in range(count):
            num = 0 if i == 0 else backspace_num
            end_str = "]" if (i == count - 1) else "],\n"
            result += " " * num + "[" + ", ".join("(p{idx}_x + {x:.2f}, p{idx}_y + {y:.2f}, p{idx}_z + {z:.2f})".format(x=path_array[j][i][0],
                                                                                                                        y=path_array[j][i][1],
                                                                                                                        z=path_array[j][i][2], idx=j+1) for j in range(6)) + end_str

    elif mode == "matrix":
        print(len(path_array))
        count = len(path_array)
        for i in range(count):
            num = 0 if i == 0 else backspace_num
            end_str = "]" if (i == count - 1) else "],\n"
            result += " " * num + "[" + ", ".join("(p{idx}_x*{e00:.2f} + p{idx}_y*{e01:.2f} + p{idx}_z*{e02:.2f} + {e03:.2f}, p{idx}_x*{e10:.2f} + p{idx}_y*{e11:.2f} + p{idx}_z*{e12:.2f} + {e13:.2f}, p{idx}_x*{e20:.2f} + p{idx}_y*{e21:.2f} + p{idx}_z*{e22:.2f} + {e23:.2f})".format(
                    e00=path_array[i].item((0,0)), e01=path_array[i].item((0,1)), e02=path_array[i].item((0,2)), e03=path_array[i].item((0,3)),
                    e10=path_array[i].item((1,0)), e11=path_array[i].item((1,1)), e12=path_array[i].item((1,2)), e13=path_array[i].item((1,3)),
                    e20=path_array[i].item((2,0)), e21=path_array[i].item((2,1)), e22=path_array[i].item((2,2)), e23=path_array[i].item((2,3)), idx=j+1) for j in range(6)) + end_str

    else:
        raise RuntimeError("Generation mode: {} not supported".format(mode))

    result += "]\n"
    result += "{}_length = {}\n".format(path_name, count)
    result += "{}_duration = {}\n".format(path_name, duration)
    result += "{}_entries = {}\n".format(path_name, entries)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PathTool: auto Hexapod global path generation")
    parser.add_argument('--outPath', metavar='DIR', dest='out_path', default='movement_paths.py')
    args = parser.parse_args()

    # generate all paths
    results = {path: generator() for path, generator in paths_generators.items()}

    # verify all paths is within safe angles
    verified = [1 for path, data in results.items() if not verify_path(path, data)]
    if len(verified) > 0:
        print("There were errors, exit...")
    else:
        # output results
        with open(args.out_path, "w") as f:
            f.write('"""This file is generated, dont directly modify content..."""\n\n')
            f.write("from config import *\n")
            for path, data in results.items():
                f.write(generate_py_body(path, data))
                f.write("\n")
            f.write("\n")
        print("Result written to {}".format(args.out_path))










