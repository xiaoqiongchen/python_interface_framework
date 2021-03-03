import hashlib
import re
import requests
from Config.StaticVars import get_unique_number_value, global_vars, info
from Util.Excel import Excel
from Util.api_request import api_request
from Config.interface import  *
from Config.ProjConfigVar import *

def md5(s):
    m5 = hashlib.md5()
    m5.update(s.encode("utf-8"))
    md5_value = m5.hexdigest()
    return md5_value

#将请求数据中包含的${变量名}的字符串部分，替换为唯一数或者全局变量字典中对应的全局变量
def data_handler(data):

    #if条件为True时候，将请求数据中包含的${unique_numxx}的字符串部分替换为框架中生成的唯一数字
    if re.search(r"\$\{unique_num\d+\}",data):
        var_name  = re.search(r"\$\{(unique_num\d+)\}",data).group(1)
        var_value = get_unique_number_value(var_name)
        data = re.sub(r"\$\{unique_num\d+\}",str(var_value),data)
        var_name = var_name.split("_")[1]
        global_vars[var_name]= var_value

    if re.search(r'\$\{md5\(\w+\)\}',data):
        str_value  = re.search(r'\$\{md5\((\w+)\)\}',data).group(1)
        md5_value = md5(str_value)
        print("替换前 data:", data, )
        data = re.sub(r'\$\{md5\(\w+\)\}',md5_value,data)
        print("替换后 data:", data, )
        global_vars["md5"]= md5_value

    # if条件为True时候，将请求数据中包含的${global_xxx}的字符串部分替换为全局变量字典中对应的全局变量
    if re.search(r"\$\{(\w+)\}",data):
        print("all",re.findall(r"\$\{(\w+)\}",data))
        for var_name in re.findall(r"\$\{(\w+)\}",data):
            print("替换前 data:",data,)
            data = re.sub(r"\$\{%s\}" %var_name, str(global_vars[var_name]), data)
            print("替换后 data:", data, )

    return data

#发送接口请求数据到接口的服务器 url 地址
def send_request(interface_name,data,regx=None):
    data = data_handler(data)
    try:
        response =api_request(eval(interface_name)[1],eval(interface_name)[0],eval(data))
        return response,data
    except Exception as e:
        print("调用接口的函数参数出错，调用的参数为%s:%s" %(interface_name,data),"\n错误信息:",e)
        return None,data

def set_var_from_response(response,var_name,regx=None):
    if regx is None:
        return False

    if not isinstance(response, requests.models.Response):
        info("传递的接口响应结果对象类型不对，现传入的response的类型是%s" %type(response))
        return False

    try:
        if re.search(regx,response.text):
            var_value = re.search(regx, response.text).group(1)
            global_vars[var_name] = var_value
            return True
    except Exception as e:
        info("从影响结果提取变量值失败，response:%s\n，var_name:%s,regx:%s" %(response,var_name,regx))
        return False

def get_test_case_sheet_names(test_data_excel_path):
    # 读取行号和需要执行的测试用例sheet名字
    test_cases_wb = Excel(test_data_excel_path)
    test_cases_wb.set_sheet_by_index(1)
    test_case_to_br_run_sheet_names = []
    for row in test_cases_wb.get_row_values():
        if row[test_case_test_step_sheet_name_col_no] is not None and row[test_case_is_executed_col_no].lower() == "y":
            #1个序号和1个测试用例sheet名称组成一个元组
            #多个元组放入到列表中，组成一个测试用例sheet的集合列表
            test_case_to_br_run_sheet_names.append((row[test_case_row_no_clo_no],row[test_case_test_step_sheet_name_col_no]))
    return test_case_to_br_run_sheet_names


def test_cases_from_test_data_sheet(test_data_excel_path,test_data_sheet_name):
    test_cases_wb = Excel(test_data_excel_path)
    test_cases_wb.set_sheet_by_name(test_data_sheet_name)
    info("设定的测试用例sheet名称为：%s" %test_data_sheet_name)
    # 读取所有的接口测试用例
    test_cases = []
    for row in test_cases_wb.get_row_values():
        if row[test_data_is_executed_col_no] is not None and row[test_data_is_executed_col_no].lower() == "y":
            test_case = row[test_data_row_no_col_no], row[test_data_interface_name_col_no], row[test_data_request_data_col_no],row[test_data_assert_word_col_no],row[test_data_correlate_regx_col_no]
            test_cases.append(test_case)
    #print(test_cases)
    return test_cases
