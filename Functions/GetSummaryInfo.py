#从CSV文件和数据库中获取Summary子报表所需信息
import pandas as pd
from Database import ConnectDataBase
import os
import datetime

def GetSummaryInfo(DataFolderPath):
    """
    从CSV文件和数据库中获取Summary子报表所需信息
    :param DataFolderPath: 存放CSV的文件夹绝对路径
    :return: Summary_Info:（二维列表包含Summary报表的信息 每个子列表是每行信息）
    """
    Summary_Info=[]#用于写Summary子表 二维列表
    for (dirpath, dirnames, filenames) in os.walk(DataFolderPath):
        for filename in filenames:
            # 分离文件名和后缀
            portion = os.path.splitext(filename)
            if portion[1] == '.csv':
                #调用数据库函数获取查询结果
                SQL_CountRecord ="select count(1) from ins_test_record tr where tr.file_name='"+filename+"'"
                #获取不同数据库的记录数
                D53_DB_Total=ConnectDataBase.ConnectDataBase_154(SQL_CountRecord)[0][0]
                D54_DB_Total=ConnectDataBase.ConnectDataBase_155(SQL_CountRecord)[0][0]
                #使用 usecols可以加快加载速度并降低内存消耗
                #low_memory:分块加载到内存，再低内存消耗中解析。但是可能出现类型混淆。确保类型不被混淆需要设置为False
                df=pd.read_csv(dirpath + '\\' + filename,usecols=[1],low_memory=False,header=None)
                #将Product列取出保存为列表用于计算归属D53和D54的数量
                Product_info=list(df[1])
                D53_ShouldBeTotal=0#初始化0 遍历Product_info 发现+1
                D54_ShouldBeTotal=0
                for i in Product_info:
                    i=str(i).upper()#先转为大写好判断 避免大小不一致的数据
                    if 'D53' in i:
                        D53_ShouldBeTotal+=1
                    elif 'D54' in i:
                        D54_ShouldBeTotal+=1
                #文件和数据库两边数据分别相等 Result等于PASS 否则FAIL
                if D53_ShouldBeTotal==D53_DB_Total and D54_ShouldBeTotal==D54_DB_Total:
                    Result='PASS'
                else:
                    Result='FAIL'
                #将每个文件对应的数据保存到列表中，后续写入Excel
                Summary_Info.append([filename,D53_ShouldBeTotal,D53_DB_Total,D54_ShouldBeTotal,D54_DB_Total,Result])
            else:
                #若遍历到别的格式文件则continue 进行下一步循环
                continue
    print(Summary_Info)
    return Summary_Info
# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     GetSummaryInfo(r"E:\InsightDataParsingToolTesting\Data")
#     end_time = datetime.datetime.now()
#     print(u"耗時:", (end_time - start_time).seconds, u"秒")