#连接数据库
import cx_Oracle as cx
DataBase_154="INSIGHT/insight@10.175.94.154:1525/orcl"#注意端口要写
DataBase_155="INSIGHT/insight@10.175.94.155:1521/orcl"
def ConnectDataBase_154(sql):
    """
    :param sql: sql语句
    :return:查询结果
    """
    con=cx.connect(DataBase_154)#创建连接
    cur=con.cursor()#创建游标
    cur.execute(sql)#执行SQL语句
    rowdata =cur.fetchall()#抓取全部数据 fetchone 抓单笔数据
    return rowdata
def ConnectDataBase_155(sql):
    con=cx.connect(DataBase_155)#创建连接
    cur=con.cursor()#创建游标
    cur.execute(sql)#执行SQL语句
    rowdata =cur.fetchall()#抓取全部数据 fetchone 抓单笔数据
    return rowdata
if __name__ == '__main__':
#     ConnectDataBase_154('115213004063632_GL_D53-D53P-D54-D54CG_S-COND_2019-11-07-02-00_2019-11-07-04-00.csv')
#     ConnectDataBase_155('115213004063632_GL_D53-D53P-D54-D54CG_S-COND_2019-11-07-02-00_2019-11-07-04-00.csv')
    rowdata=ConnectDataBase_154("select tr.build_info,tr.file_name,tr.record_info,tm.module_name,tm.module_value from ins_test_record tr join ins_test_module tm on tr.unit_id=tm.unit_id where tr.file_name='115213004035146_GL_D53-D53P-D54-D53RCV-D53SPK-D54RCV-D54SPK-D54CG_VIBRATOR_2019-11-05-12-00_2019-11-05-14-00.csv'")
    print(rowdata)