import pandas as pd
from Database import ConnectDataBase
from Functions import FindDiffrence
import os,datetime

def GetTestItemInfo(DataFolderPath):
    """
    获取TestItem报表的信息
    :param DataFolderPath: csv文件夹绝对路径
    :return:TestItem_Info
    """
    TestItem_Info=[]#用于保存TestItem信息
    #每次循环都用到的变量都定义在for循环里面
    for (dirpath,dirnames,filenames) in os.walk(DataFolderPath):
        for filename in filenames:
            #分离文件名和后缀
            record_info_list = []  # 保存csv拼接的record_info
            portion=os.path.splitext(filename)
            First_part = str(filename).split('_')[0]  # 截取record_info第一部分
            if portion[1]=='.csv':
                # 找到Parametric的位置 列号
                First_row = list(pd.read_csv(dirpath + '\\' + filename,skiprows=0, nrows=1))
                # 工站名 并去掉中线
                StationName = First_row[0].split('-')
                StationName = StationName[0] + StationName[1]
                Parametric_index = First_row.index('Parametric')  # 位置
                #第二行 列名
                Second_row=list(pd.read_csv(dirpath+'\\' + filename,skiprows=1,nrows=2))
                #最后一个测试项列名的列号
                last_testitem_index=Second_row.index(Second_row[-1])
                #文件中的测试项总数
                TestItem_Total=last_testitem_index-Parametric_index+1
                #获取测试项列号
                testitem_column_index =[]#保存测试项的列号
                for index in range(Parametric_index,last_testitem_index+1):
                    testitem_column_index.append(index)
                usecols=[1,2,8]+testitem_column_index
                #再按usecols读取内容
                #第一行Parametric后面的列没有分隔符，跳过该行读取，不然找不到后面的列
                df = pd.read_csv(dirpath + '\\' + filename,skiprows=1,nrows=10000000,usecols=usecols,low_memory=False,header=None)
                #将所有空格填为None
                df.fillna('None',inplace=True)
                product=list(df[1])#取产品名称
                sn=list(df[2])#取SN
                testtime=list(df[8])#取测试开始时间
                for i in range(len(sn)):
                    #拼接Record_info
                    record_info=First_part+'_'+str(i+2)+'_'+str(sn[i])+'_'+str(testtime[i])
                    record_info_list.append(record_info)
                for j in range(len(record_info_list)):
                    if j>=6:#第八行开始有效数据
                        #文件操作
                        NoneValueCount=0#每行开始前初始化为0 没有值的统计
                        File_TestItemList=[]
                        for t in testitem_column_index:
                            File_TestItem=(Second_row[t],df.loc[j,t])
                            if df.loc[j,t]!='None':#剔除None值的信息
                                File_TestItemList.append(File_TestItem)
                            # 遍历当前行所有列，如果有单元格为空值则+1 最后总的减掉空的等于实际测试项数量
                            elif df.loc[j, t] == 'None':
                                NoneValueCount += 1
                        Should_Be_Counter=TestItem_Total-NoneValueCount
                        #数据库操作得到DB_Counter
                        SQL_QueryTestItem="select t.item_name,t.item_value from ins_"+StationName+"_Vl t join ins_test_record tr on t.record_info=tr.record_info where tr.file_name='" + filename + "' and t.record_info='" + record_info_list[j] + "'"
                        if 'D53' in product[j]:
                            DB_TestItem = ConnectDataBase.ConnectDataBase_154(SQL_QueryTestItem)
                            DB_Counter=len(DB_TestItem)
                        elif 'D54' in product[j]:
                            DB_TestItem = ConnectDataBase.ConnectDataBase_155(SQL_QueryTestItem)
                            DB_Counter = len(DB_TestItem)
                        #比较File_TestItemList和DB_TestItem 得出Consist Counter
                        if (set(File_TestItemList)==set(DB_TestItem))==True:
                            #用集合形式比较，避免顺序问题导致不一致
                            Consist_Counter=len(File_TestItemList)
                            FileItems_DiffToDB='-'
                            DbItems_DiffToF='-'
                            Result='PASS'
                        else:
                            #调用找不同函数FindDiffrence,返回相同数，不同项
                            Consist_Counter,FileItems_DiffToDB,DbItems_DiffToF=FindDiffrence.FindDiffrence(File_TestItemList,DB_TestItem)
                            Result='FAIL'
                        TestItem_Info.append([product[j],filename,record_info_list[j],TestItem_Total,Should_Be_Counter,DB_Counter,Consist_Counter,FileItems_DiffToDB,DbItems_DiffToF,Result])
                    j+=1
            else:
                # 若遍历到别的格式文件则continue 进行下一步循环
                continue
    print(TestItem_Info)
    return TestItem_Info

# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     GetTestItemInfo(DataFolderPath=r"E:\InsightDataParsingToolTesting\Data")
#     end_time = datetime.datetime.now()
#     print(u"耗時:", (end_time - start_time).seconds, u"秒")