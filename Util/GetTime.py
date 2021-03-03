import time


def get_current_date():
    timeTup = time.localtime()
    currentDate = str(timeTup.tm_year) + "年" + \
                  str(timeTup.tm_mon) + "月" + str(timeTup.tm_mday) + "日"
    return currentDate


def get_current_time():
    timeTup = time.localtime()
    currentTime = str(timeTup.tm_hour) + "时" + \
                  str(timeTup.tm_min) + "分" + str(timeTup.tm_sec) + "秒"
    return currentTime


def get_current_datetime():
    return get_current_date() + " " + get_current_time()


if __name__ == "__main__":
    print(get_current_date())
    print(get_current_datetime())
    print(get_current_time())
