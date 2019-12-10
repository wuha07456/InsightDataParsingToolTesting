#生成报告
from Functions import GetSummaryInfo,GetModuleInfo_AttributeInfo
from Functions import Excel_Style,GetFailItemInfo,GetTestItemInfo
import xlwt
def GenerateReport(DataFolderPath):
    """
    生成报表函数
    :param DataFolderPath:存放CSV的文件夹绝对路径
    :return: ReportPath：返回报告绝对路径
    """
    workbook=xlwt.Workbook()#新增空表
    Sheet_Summary=workbook.add_sheet("Summary")#新增sheet
    Sheet_Module = workbook.add_sheet("Module")  # 新增sheet
    Sheet_Attribute = workbook.add_sheet("Attribute")  # 新增sheet
    Sheet_FailItem = workbook.add_sheet("FailItem")
    Sheet_TestItem=workbook.add_sheet("TestItem")
    #设置第一列的宽度
    first_column=Sheet_Summary.col(0)
    first_column.width=256*80

    #调用获取各个报表信息的函数
    Summary_Info=GetSummaryInfo.GetSummaryInfo(DataFolderPath)
    Module_Info,Attribute_Info=GetModuleInfo_AttributeInfo.GetModuleInfo_AttributeInfo(DataFolderPath)
    FailItem_Info=GetFailItemInfo.GetFailItemInfo(DataFolderPath)
    TestItem_Info=GetTestItemInfo.GetTestItemInfo(DataFolderPath)
    # 表头
    Summary_Column_Names = ['FileName', 'D53ShouldBeTotal', 'D53DBTotal', 'D54ShouldBeTotal', 'D54DBTotal', 'Result']
    Module_Column_Names=['Product','FileName','Record Info','Module Total','File Moulde','DB Module','Result']
    Attribute_Column_Names=['Product','FileName','Record Info','Attr Counter','File Attributes','DB Attributes','Result']
    FailItem_Column_Names=['Product','FileName','Record Info','File Item Total','Should Be Counter','DB Counter','Consist Counter','FileFailItems(DiffToDB)','DbFailItems(DiffToF)','Result']
    TestItem_Column_Names=['Product','FileName','Record Info','TestItem Total','Should Be Counter','DB Counter','Consist Counter','FileItems(DiffToDB)','DbItems(DiffToF)','Result']
    # 将表头的列表插入列表Summary_Info成为第一个元素
    Summary_Info.insert(0,Summary_Column_Names)
    Module_Info.insert(0,Module_Column_Names)
    Attribute_Info.insert(0,Attribute_Column_Names)
    FailItem_Info.insert(0,FailItem_Column_Names)
    TestItem_Info.insert(0, TestItem_Column_Names)
    #print(Summary_Info)
    #写Summary报表
    Style=Excel_Style.Excel_Style()#调用样式函数 Style[0]:黄色底色
    #Style[1]:居中无底色 Style[2]:红色底色
    #嵌套循环按行 按列写入Excel
    rows_count_summary=len(Summary_Info)#行数
    columns_count_summary=len(Summary_Info[0])#列数 提前算出来，避免每次循环都算一次
    for i in range(rows_count_summary):#循环行
        # Result Fail的添加黄色底色
        if Summary_Info[i][5] == 'FAIL':
            for j in range(columns_count_summary):#循环列 第一个子列表的长度即为列数
                Sheet_Summary.write(i,j,Summary_Info[i][j],Style[0])
        else:
            for j in range(columns_count_summary):  # 循环列
                Sheet_Summary.write(i, j, Summary_Info[i][j],Style[1])
    # 写Module-info
    rows_count_module = len(Module_Info)  # 行数
    columns_count_module = len(Module_Info[0])  # 列数 提前算出来，避免每次循环都算一次
    for i in range(rows_count_module):  # 循环行
        # Result Fail的添加黄色底色
        if Module_Info[i][6] == 'FAIL':
            for j in range(columns_count_module):  # 循环列 第一个子列表的长度即为列数
                Sheet_Module.write(i, j, Module_Info[i][j], Style[0])
        else:
            for j in range(columns_count_module):  # 循环列
                Sheet_Module.write(i, j, Module_Info[i][j], Style[1])
    #写Attribute-info
    rows_count_attribute = len(Attribute_Info)  # 行数
    columns_count_attribute = len(Attribute_Info[0])  # 列数 提前算出来，避免每次循环都算一次
    for i in range(rows_count_attribute):  # 循环行
        # Result Fail的添加黄色底色
        if Attribute_Info[i][6] == 'FAIL':
            for j in range(columns_count_attribute):  # 循环列 第一个子列表的长度即为列数
                Sheet_Attribute.write(i, j, Attribute_Info[i][j], Style[0])
        else:
            for j in range(columns_count_attribute):  # 循环列
                Sheet_Attribute.write(i, j, Attribute_Info[i][j], Style[1])
    # 写FailItem-info
    rows_count_failitem = len(FailItem_Info)  # 行数
    columns_count_failitem = len(FailItem_Info[0])  # 列数 提前算出来，避免每次循环都算一次
    for i in range(rows_count_failitem):  # 循环行
        # Result Fail的添加黄色底色
        if FailItem_Info[i][9] == 'FAIL':
            for j in range(columns_count_failitem):  # 循环列 第一个子列表的长度即为列数
                Sheet_FailItem.write(i, j, FailItem_Info[i][j], Style[0])
        else:
            for j in range(columns_count_failitem):  # 循环列
                Sheet_FailItem.write(i, j, FailItem_Info[i][j], Style[1])

    # 写TestItem-info
    rows_count_testitem = len(TestItem_Info)  # 行数
    columns_count_testitem = len(TestItem_Info[0])  # 列数 提前算出来，避免每次循环都算一次
    for i in range(rows_count_testitem):  # 循环行
        # Result Fail的添加黄色底色
        if TestItem_Info[i][9] == 'FAIL':
            for j in range(columns_count_testitem):  # 循环列 第一个子列表的长度即为列数
                Sheet_TestItem.write(i, j, TestItem_Info[i][j], Style[0])
        else:
            for j in range(columns_count_testitem):  # 循环列
                Sheet_TestItem.write(i, j, TestItem_Info[i][j], Style[1])
    #保存文档
    ReportPath="E:\InsightDataParsingToolTesting\Report\Report.xls"
    OtherReportPath="E:\InsightDataParsingToolTesting\Report\Report1.xls"
    try:
        workbook.save(ReportPath)
    except PermissionError:
        workbook.save(OtherReportPath)
    finally:
        pass
    return ReportPath

# if __name__ == '__main__':
#     GenerateReport(r"E:\InsightDataParsingToolTesting\Data")