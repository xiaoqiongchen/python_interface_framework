from Config.ProjConfigVar import proj_path
from Config.StaticVars import get_unique_number_value, global_vars
from Util.DataHandler import get_test_case_sheet_names, test_cases_from_test_data_sheet, send_request
from html_report import report_html
from Util.Excel import *
from Util.Mail import send_mail
from Util.Log import *
import re

import  os
#获取测试数据文件的绝对路径
test_data_excel_path = os.path.join(proj_path,"TestData\\接口测试数据.xlsx")
#print(test_data_excel_path)
test_cases_wb = Excel(test_data_excel_path)
test_results_for_html_report  = []
#遍历执行所有的sheet中的测试用例
for test_sheet_name in get_test_case_sheet_names(test_data_excel_path):
    flag = True
    test_cases_wb.set_sheet_by_name(test_sheet_name[1])
    test_cases = test_cases_from_test_data_sheet(test_data_excel_path,test_sheet_name[1])
    for test_case in test_cases:
        start_time = time.time()
        r,send_data= send_request(test_case[1],test_case[2])
        end_time=time.time()
        info("接口的响应结果是：%s" %r.text)
        test_cases_wb.write_cell_value(int(test_case[0]+1),test_data_response_data_col_no+1,r.text)
        info("断言值为：%s" %test_case[3])
        test_cases_wb.write_current_time(int(test_case[0]+1),test_data_executed_time_col_no+1)
        try:
            if not re.search(test_case[3],r.text): raise AssertionError
            test_cases_wb.write_cell_value(int(test_case[0] + 1), test_data_test_result_col_no+1, "成功")
            test_results_for_html_report.append(
                (r.url, send_data, r.text, int((end_time - start_time) * 1000), test_case[3], "成功"))
        except AssertionError:
            test_cases_wb.write_cell_value(int(test_case[0] + 1),  test_data_test_result_col_no+1,"失败")
            test_results_for_html_report.append(
                (r.url, send_data, r.text, int((end_time - start_time) * 1000), test_case[3], "失败"))
            flag = False
        except:
            test_cases_wb.write_cell_value(int(test_case[0] + 1),  test_data_test_result_col_no+1, "失败")
            test_results_for_html_report.append(
                (r.url, send_data, r.text, int((end_time - start_time) * 1000), test_case[3], "失败"))
            flag = False

        info("接口请求的耗时为%d 毫秒" %((end_time - start_time)*1000))
        test_cases_wb.write_cell_value(int(test_case[0] + 1), test_data_test_elapse_time_col_no+1, str(int((end_time - start_time)*1000)))
        if test_case[4] is not None:
            var_name = test_case[4].split("||")[0]
            regx = test_case[4].split("||")[1]
            if re.search(regx,r.text).group(1):
                var_value = re.search(regx,r.text).group(1)
                exec("global_vars['%s']='%s'" %(var_name,var_value))
                info("从响应中提取的变量名%s，变量值为%s" %(var_name,var_value))
                info("生成全局变量名： global_vars['%s']='%s'" %(var_name,var_value))
        info("-----" * 30)
    test_cases_wb.set_sheet_by_index(1)
    if flag:
        test_cases_wb.write_cell_value(int(test_sheet_name[0]) + 1, test_case_executed_result_col_no, "成功")
    else:
        test_cases_wb.write_cell_value(int(test_sheet_name[0]) + 1, test_case_executed_result_col_no, "失败")
    test_cases_wb.write_current_time(int(test_sheet_name[0]) + 1, test_case_executed_time_col_no)

    info("*"*50)

print()
html_name = '接口测试报告'
report_html(test_results_for_html_report, html_name)
send_mail("接口测试报告.html")


