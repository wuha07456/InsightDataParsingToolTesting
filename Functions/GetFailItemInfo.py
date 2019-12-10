import pandas as pd
from Database import ConnectDataBase
import os,datetime
from Functions import FindDiffrence

def GetFailItemInfo(DataFolderPath):
    """
    获取FailItem报表的信息
    :param DataFolderPath: csv文件夹绝对路径
    :return:FailItem_Info
    """
    FailItem_Info=[]#用于保存FailItem信息
    #每次循环都用到的变量都定义在for循环里面
    for (dirpath,dirnames,filenames) in os.walk(DataFolderPath):
        for filename in filenames:
            #分离文件名和后缀
            record_info_list = []  # 保存csv拼接的record_info
            portion=os.path.splitext(filename)
            first_part = str(filename).split('_')[0]  # 截取record_info第一部分
            if portion[1]=='.csv':
                # 找到Parametric的位置 列号
                First_row = list(pd.read_csv(dirpath + '\\' + filename, skiprows=0, nrows=1))
                StationName = First_row[0]  # 获取工站名
                # 工站名 并去掉中线
                StationName = StationName.split('-')
                StationName = StationName[0] + StationName[1]
                #找到List of Failing Tests的位置 列号
                Second_row=list(pd.read_csv(dirpath+'\\' + filename,skiprows=1,nrows=2))
                FailItem_index=Second_row.index('List of Failing Tests')#位置 列号
                Test_Result_index=Second_row.index('Test Pass/Fail Status')
                #跳过第一行再读一次csv
                # 第一行Parametric后面的列没有分隔符，跳过该行读取，不然找不到后面的列
                df = pd.read_csv(dirpath + '\\' + filename, skiprows=1, nrows=100000000,
                                 low_memory=False, header=None)
                # 将所有空格填为None
                df.fillna('None', inplace=True)
                product = list(df[1])  # 取产品名称
                sn = list(df[2])  # 取SN
                testtime = list(df[8])  # 取测试开始时间
                failitem = list(df[FailItem_index])  # 取FailItem
                testresult=list(df[Test_Result_index])#取测试结果 Fail才有FailItem
                for i in range(len(sn)):
                    #拼接Record_info
                    record_info=first_part+'_'+str(i+2)+'_'+str(sn[i])+'_'+str(testtime[i])
                    record_info_list.append(record_info)
                for j in range(len(record_info_list)):
                    if j>=6:#第七行开始有效数据
                        #文件操作
                        ShouldBeCounter=0
                        FileFailItems_DiffToDB = '-'
                        DbFailItems_DiffToF = '-'
                        Result=''
                        #测试结果为Fail的才有FailItem 所有只遍历Fail的行
                        if testresult[j]=='FAIL' and failitem[j]!='None':
                            # 数据库操作
                            SQL_QueryFailItem = "select fv.item_name from ins_" + StationName + "_fa_vl fv join ins_test_record tr on tr.record_info=fv.record_info where tr.file_name='" + filename + "' and tr.record_info='" + \
                                                record_info_list[j] + "'"
                            if 'D53' in product[j]:
                                DB_FailItem = ConnectDataBase.ConnectDataBase_154(SQL_QueryFailItem)
                                DB_Counter = len(DB_FailItem)
                            elif 'D54' in product[j]:
                                DB_FailItem = ConnectDataBase.ConnectDataBase_155(SQL_QueryFailItem)
                                DB_Counter = len(DB_FailItem)
                            DB_FailItem_list = []  # 将DB_FailItem里的元素拆出来保存为字符串类型的列表
                            for dbf in range(len(DB_FailItem)):
                                b = ''.join(DB_FailItem[dbf])
                                DB_FailItem_list.append(''.join(b))
                            #遍历所有字符，没有';'则File_Item_Total=1 有1个则加1
                            for c in failitem[j]:
                                count=failitem[j].count(';')
                            if count==0:#没有逗号说明只有一个FailItem
                                File_Item_Total=1
                                failitem_list = [str(failitem[j])]
                                # 该FailItem是否存在Second_row 存在则ShouldBeCounter+1
                                if failitem[j] in Second_row:
                                    ShouldBeCounter+=1
                                else:
                                    ShouldBeCounter=0
                                #比较异同
                                if DB_FailItem_list==failitem_list:
                                    Consist_Counter = File_Item_Total
                                    FileFailItems_DiffToDB = '-'
                                    DbFailItems_DiffToF = '-'
                                    Result = 'PASS'
                                else:
                                    #不相等则调用FindDifference找不同
                                    Consist_Counter,FileFailItems_DiffToDB,DbFailItems_DiffToF=FindDiffrence.FindDiffrence([failitem[j]],DB_FailItem_list)
                                    Result = 'FAIL'
                            else:
                                File_Item_Total = count + 1
                                #按分号切割保存在列表中
                                failitem_list=str(failitem[j]).split(';')
                                for fail in range(len(failitem_list)):
                                    if failitem_list[fail] in Second_row:
                                        ShouldBeCounter+=1
                                    else:
                                        ShouldBeCounter=0
                                #比较异同
                                if failitem_list==DB_FailItem_list:
                                    Consist_Counter = File_Item_Total
                                    FileFailItems_DiffToDB = '-'
                                    DbFailItems_DiffToF = '-'
                                    Result = 'PASS'
                                else:
                                    Consist_Counter, FileFailItems_DiffToDB, DbFailItems_DiffToF = FindDiffrence.FindDiffrence(failitem_list,DB_FailItem_list)
                                    Result = 'FAIL'
                            FailItem_Info.append([product[j],filename,record_info_list[j],File_Item_Total,ShouldBeCounter,DB_Counter,Consist_Counter,FileFailItems_DiffToDB,DbFailItems_DiffToF,Result])
                    j+=1
            else:
                # 若遍历到别的格式文件则continue 进行下一步循环
                continue
    print(FailItem_Info)
    return FailItem_Info

# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     GetFailItemInfo(DataFolderPath=r"E:\InsightDataParsingToolTesting\Data")
#     end_time = datetime.datetime.now()
#     print(u"耗時:", (end_time - start_time).seconds, u"秒")