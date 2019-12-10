#main方法 调用相关函数
import datetime
from Functions import GenerateReport
def main(DataFolderPath):
    """

    :param DataFolderPath: csv文件夹绝对路径
    :return:
    """
    GenerateReport.GenerateReport(DataFolderPath)

if __name__ == '__main__':
    start_time=datetime.datetime.now()
    main(DataFolderPath=r"E:\InsightDataParsingToolTesting\Data")
    end_time=datetime.datetime.now()
    print(u"报表已生成，耗時:", (end_time - start_time).seconds, u"秒")