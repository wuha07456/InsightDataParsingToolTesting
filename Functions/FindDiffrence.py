def FindDiffrence(File_TestItemList,DB_TestItem):
    """
    找出两个列表中的相同元素和不同元素 以及A有b没有，B有A没有的元素
    :param File_TestItemList:
    :param DB_TestItem:
    :return: Consist_Counter,FileItems_DiffToDB,DbItems_DiffToF
    """
    same_item=[x for x in File_TestItemList if x in DB_TestItem]#相同的元素
    Consist_Counter=len(same_item)#相同元素数量
    different_item=[y for y in (File_TestItemList+DB_TestItem) if y not in same_item]#不同的元素
    #将列表转为集合，分别与different_item取交集则是 我有你没有的
    FileItems_DiffToDB=list(set(File_TestItemList)&set(different_item))
    DbItems_DiffToF=list(set(DB_TestItem)&set(different_item))
    return Consist_Counter,FileItems_DiffToDB,DbItems_DiffToF
# if __name__ == '__main__':
#     a=['TestGroup Failure Action', 'STOP_TESTABLE_DEVICE CHECK_PROCESS_CONTROL']
#     b=['TestGroup Failure Action', '1STOP_TESTABLE_DEVICE CHECK_PROCESS_CONTROL']
#     Consist_Counter, FileItems_DiffToDB, DbItems_DiffToF=FindDiffrence(a,b)
#     print(Consist_Counter, FileItems_DiffToDB, DbItems_DiffToF)
