# 判断登录的用户名与密码是否正确
def check_identity(cursor, id, passwd):
    sql = "select ID, passwd from person natural join card where ID = '{}' and passwd = '{}' and valid <> 0".format(
        id, passwd)
    cursor.execute(sql)
    return cursor.rowcount


#根据id查询用户名
def select_v_name(cursor, id):
    sql = "select name from person natural join card where ID = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# 查询食堂消费信息
def select_v_consume(cursor, id, start, end):
    sql = "select * from v_consume where ID = '{}' and consumetm between '{}' and '{}'".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询校门进出信息
def select_v_record(cursor, id, start, end):
    sql = "select * from v_record where ID = '{}' and recordtm between '{}' and '{}'".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询宿舍门禁信息
def select_v_access(cursor, id, start, end):
    sql = "select * from v_access where ID = '{}' and accesstm between '{}' and '{}'".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询所在宿舍信息
def select_dormitory(cursor, id):
    sql = "select dno, dadmin, dtel, dfloor from domitory, card where domitory.cno = card.cdno and card.ID = '{}'".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询各餐厅信息
def select_canteen(cursor):
    sql = "select * from canteen"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询各校门信息
def select_gate(cursor):
    sql = "select * from gate"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询一卡通信息
def select_information(cursor, id):
    sql = "select * from person natural join card where valid <> 0 and ID = '{}'".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 以下功能仅提供给admin

# 查询所有教师信息
def select_teacher(cursor):
    sql = "select * from person natural join teacher"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询所有学生信息
def select_student(cursor):
    sql = "select * from person natural join student"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询所有其他人员信息
def select_others(cursor):
    sql = "select * from person natural join others"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


# 查询各餐厅营业额
def select_profit(cursor, start, end):
    sql = "select wno, wname, sum(amount) as profit from canteen natural join consume where consumetm between '{}' and '{}' group by wno, wname".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
