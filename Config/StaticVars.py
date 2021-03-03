import pickle
import os.path
from Config import ProjConfigVar
from Util.Log import *
#初始化框架工程中的全局变量，存储在测试数据中的唯一值数据
#框架工程中若要使用字典中的任意一个变量，则每次使用后，均需要将字典中的value值进行加1操作。
global_vars = {}

def get_unique_number_value(unique_number):
    global global_vars
    data_file = os.path.join(ProjConfigVar.proj_path,"Config\\StaticVarDataFile")
    try:
        with open(data_file,"rb") as fp:
            var = pickle.load(fp)
            data= var[unique_number]
            info("全局唯一数当前生成的值是：%s" %data)
            global_vars[unique_number]=str(data)
            var[unique_number] +=1
        with open(data_file,"wb") as fp:
            pickle.dump(var,fp)
    except Exception as e:
        info("获取测试框架的全局唯一数变量值失败，请求的全局唯一数变量是%s,异常原因如下：%s" %(unique_number,e))
        data = None
    finally:
        return data

if __name__ =="__main__":
    #初始化2个唯一书变量，初始值可以根据数据的使用情况进行自定义
    """
    data={"unique_num1":100,"unique_num2":1000}
    with open("StaticVarDataFile","wb") as fp:
        pickle.dump(data,fp)
    with open("StaticVarDataFile","rb") as fp:
        data=pickle.load(fp)
    print(data)
    print(data["unique_num1"])
    """
    print(get_unique_number_value("unique_num1"))
    print(get_unique_number_value("unique_num2"))