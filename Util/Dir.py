import os
import os.path
from Util.GetTime import *


def make_date_dir(dir_path):
    if os.path.exists(dir_path):
        cur_date = get_current_date()
        path = os.path.join(dir_path, cur_date)
        if not os.path.exists(path):
            os.mkdir(path)
        return cur_date
    else:
        raise Exception("dir path does not exist!")
    return


def make_time_dir(dir_path):
    if os.path.exists(dir_path):
        cur_time = get_current_time()
        path = os.path.join(dir_path, cur_time)
        if not os.path.exists(path):
            os.mkdir(path)
            return cur_time
    else:
        raise Exception("dir path does not exist!")
    return


if __name__ == "__main__":
    try:
        make_date_dir("e:\\testman")
    except:
        print("创建目录失败")
