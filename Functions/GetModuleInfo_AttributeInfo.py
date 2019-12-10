import pandas as pd
from Database import ConnectDataBase
import os,datetime

def GetModuleInfo_AttributeInfo(DataFolderPath):
    """
    获取Module和Attribute子报表的信息
    ：:parameter:DataFolderPath: csv文件夹绝对路径
    :return:Module_Info Attribute_Info
    """
    Module_keyword=['BMLB','HSGA','MLB','PEARL','CAM','BTY','CGS']
    Module_Info=[]#用于保存Module信息
    Attribute_Info=[]#用于保存Attribute信息
    #每次循环都用到的变量都定义在for循环里面
    for (dirpath,dirnames,filenames) in os.walk(DataFolderPath):
        for filename in filenames:
            #分离文件名和后缀
            record_info_list = []  # 保存拼接的record_info
            portion=os.path.splitext(filename)
            first_part = str(filename).split('_')[0]  # 截取record_info第一部分
            if portion[1]=='.csv':
                #找到Parametric的位置 列号
                First_row=list(pd.read_csv(dirpath+'\\' + filename,skiprows=0,nrows=1))
                Parametric_index=First_row.index('Parametric')#位置列号
                #将第二行数据保存到列表用于判断有多少列包含Module关键字
                Second_row=list(pd.read_csv(dirpath+'\\' + filename,skiprows=1,nrows=2))
                Module_index=[1,2,8]#用于append Module所在列号
                ModuleDicIndex_Names={}#字典 保存列号和对应名字
                #循环遍历 文件中包含Module关键字的列
                for x in range(len(Module_keyword)):
                    for y in range(Parametric_index):#在Parametric 之前找Module
                        if Module_keyword[x] in Second_row[y]:
                            Module_index.append(y)
                            ModuleDicIndex_Names[y]=Second_row[y]

                #去重排序 Module_index可以作为usercols的参数
                Module_index=list(set(Module_index))
                #给字典排序后变成元素为元组的列表[(a,b)]
                ModuleDicIndex_Names=sorted(ModuleDicIndex_Names.items(),key=lambda x:x[0])
                #再按Module_index读取内容
                df = pd.read_csv(dirpath + '\\' + filename, usecols=Module_index, low_memory=False, header=None)
                #将所有空格填为None
                df.fillna('None',inplace=True)#用于和数据库比较None值
                product=list(df[1])#取产品名称
                sn=list(df[2])#取SN
                testtime=list(df[8])#取测试开始时间
                for i in range(len(sn)):
                    #拼接Record_info
                    record_info=first_part+'_'+str(i+1)+'_'+str(sn[i])+'_'+str(testtime[i])
                    record_info_list.append(record_info)
                #按行循环找需要的信息
                for j in range(len(record_info_list)):
                    if j>=7:#第八行开始有效数据
                        File_Module = {}
                        File_Attributes={}
                        if len(Module_index)<=3:#如果该csv文件没有Module和Attribute
                            File_Module='{}'
                            File_Attributes='{}'
                            Attr_Counter = 0
                        else:
                            for k in range(len(ModuleDicIndex_Names)):
                                #按行取csv文件里的Module信息
                                File_Module[ModuleDicIndex_Names[k][1]]=df.loc[j,ModuleDicIndex_Names[k][0]]
                            File_Module = str(File_Module)#转为字符串格式
                            if Parametric_index-Module_index[-1]==1:#列号相减等于1代表没有Attribute
                                File_Attributes='{}'
                                Attr_Counter=0
                            else:
                                #根据列号范围获得对应的列名
                                Attribute_column_index=[]#保存列号 用于pandas 读取
                                AttributeDicIndex_Names={}
                                for att in range(Module_index[-1]+1,Parametric_index):
                                    Attribute_column_index.append(att)
                                    AttributeDicIndex_Names[att]=Second_row[att]
                                #排序
                                AttributeDicIndex_Names = sorted(AttributeDicIndex_Names.items(), key=lambda x: x[0])
                                df_attribute=pd.read_csv(dirpath + '\\' + filename, usecols=Attribute_column_index, low_memory=False, header=None)
                                # 将所有空格填为None
                                df_attribute.fillna('None', inplace=True)
                                #按行取File_Attributes
                                for q in range(len(AttributeDicIndex_Names)):
                                    File_Attributes[AttributeDicIndex_Names[q][1]]=df_attribute.loc[j,AttributeDicIndex_Names[q][0]]
                                Attr_Counter=len(File_Attributes)
                                File_Attributes=str(File_Attributes)
                        #数据库操作
                        SQL_QueryModule = "select tm.module_name,tm.module_value from ins_test_record tr join ins_test_module tm on tr.unit_id=tm.unit_id " \
                                          "where tr.file_name='" + filename + "'and tr.record_info='" + record_info_list[j] + "'"
                        SQL_QueryAttribute="select ta.attribute_name,ta.attribute_value from ins_test_record tr join ins_test_attribute ta on tr.unit_id=ta.unit_id " \
                                           "and tr.record_id=ta.record_id where tr.file_name='" + filename + "' and tr.record_info='" + record_info_list[j] + "'"
                        if 'D53' in product[j]:
                            #数据库查询Module信息
                            DB_ModuleData = ConnectDataBase.ConnectDataBase_154(SQL_QueryModule)
                            Module_Total=len(DB_ModuleData)
                            DB_ModuleData = dict(DB_ModuleData)
                            for dbm in DB_ModuleData:#将None值转换为'None' 方便比较
                                if DB_ModuleData[dbm]==None:
                                    DB_ModuleData[dbm]='None'
                            #将列表里的module和value 转为字典 再转字符串用于写Excel
                            DB_ModuleData=str(DB_ModuleData)
                            #数据库查询Attribute信息
                            DB_Attributes=ConnectDataBase.ConnectDataBase_154(SQL_QueryAttribute)
                            DB_Attributes=dict(DB_Attributes)
                            for dba in DB_Attributes:#将None值转换为'None' 方便比较
                                if DB_Attributes[dba]==None:
                                    DB_Attributes[dba]='None'
                            DB_Attributes = str(DB_Attributes)
                        elif 'D54' in product[j]:
                            # 数据库查询Module信息
                            DB_ModuleData = ConnectDataBase.ConnectDataBase_155(SQL_QueryModule)
                            Module_Total=len(DB_ModuleData)
                            DB_ModuleData = dict(DB_ModuleData)
                            for dbm in DB_ModuleData:#将None值转换为'None' 方便比较
                                if DB_ModuleData[dbm]==None:
                                    DB_ModuleData[dbm]='None'
                            DB_ModuleData = str(DB_ModuleData)
                            # 数据库查询Attribute信息
                            DB_Attributes = ConnectDataBase.ConnectDataBase_155(SQL_QueryAttribute)
                            DB_Attributes = dict(DB_Attributes)
                            for dba in DB_Attributes:  # 将None值转换为'None' 方便比较
                                if DB_Attributes[dba] == None:
                                    DB_Attributes[dba] = 'None'
                            DB_Attributes = str(DB_Attributes)
                        #判断Result_Module
                        if File_Module==DB_ModuleData:
                            Result_Module='PASS'
                        else:
                            Result_Module='FAIL'

                        # 判断Result_Attributes
                        if File_Attributes == DB_Attributes:
                            Result_Attributes = 'PASS'
                        else:
                            Result_Attributes = 'FAIL'
                        # 添加Module报表所需信息到二维列表中
                        Module_Info.append([product[j],filename,record_info_list[j],Module_Total,File_Module,DB_ModuleData,Result_Module])
                        #添加Attribute报表所需信息到二维列表中
                        Attribute_Info.append([product[j],filename,record_info_list[j],Attr_Counter,File_Attributes,DB_Attributes,Result_Attributes])
                    j+=1
            else:
                # 若遍历到别的格式文件则continue 进行下一步循环
                continue
    print(Module_Info)
    print(Attribute_Info)
    return Module_Info,Attribute_Info
# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     GetModuleInfo_AttributeInfo(DataFolderPath=r"E:\InsightDataParsingToolTesting\Data")
#     end_time = datetime.datetime.now()
#     print(u"耗時:", (end_time - start_time).seconds, u"秒")