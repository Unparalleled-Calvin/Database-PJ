# 修改密码
def update_passwd(cursor, id, newpasswd):
    sql = "update card set passwd = '{}' where ID = '{}' and valid <> 0".format(
        newpasswd, id)
    cursor.execute(sql)
    return cursor.rowcount


# 卡充值
def update_remainingsum(cursor, id, amount):
    sql = "select charge('{}', {})".format(id, amount)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# 卡挂失
def update_card(cursor, id, newpasswd):
    sql1 = "select * from card where ID = '{}' and valid <> 0".format(id)
    cursor.execute(sql1)
    if cursor.rowcount == 1:
        rows = cursor.fetchall()
        if rows[0][4] == None:
            cdno = 'null'
        else:
            cdno = rows[0][4]
        sql2 = "insert into card(ID, passwd, cdno, valid) values('{}', '{}', {}, {})".format(
            id, newpasswd, cdno, rows[0][5])
        cursor.execute(sql2)
    return cursor.rowcount


# 以下功能仅提供给admin

# 重置密码
def default_passwd(cursor, id):
    sql = "update card set passwd = '000000' where ID = '{}' and valid <> 0".format(
        id)
    cursor.execute(sql)
    return cursor.rowcount


# 关闭进校权限
def update_valid2(cursor, id):
    sql = "update card set valid = 2 where ID = '{}' and valid = 1".format(id)
    cursor.execute(sql)
    return cursor.rowcount


# 开启进校权限
def update_valid1(cursor, id):
    sql = "update card set valid = 1 where ID = '{}' and valid = 2".format(id)
    cursor.execute(sql)
    return cursor.rowcount


# 分配宿舍
def update_cdno(cursor, id, cdno):
    sql = "update card set cdno = {} where ID = '{}' and valid <> 0".format(
        cdno, id)
    cursor.execute(sql)
    return cursor.rowcount


# 更新教师职称
def update_rank(cursor, id, newrank):
    sql = "update teacher set rank = '{}' where ID = '{}'".format(newrank, id)
    cursor.execute(sql)
    return cursor.rowcount


# 更新学生班级
def update_class(cursor, id, newclass):
    sql = "update student set class = '{}' where ID = '{}'".format(
        newclass, id)
    cursor.execute(sql)
    return cursor.rowcount


# 更新其他人工作
def update_work(cursor, id, newwork):
    sql = "update others set work = '{}' where ID = '{}'".format(newwork, id)
    cursor.execute(sql)
    return cursor.rowcount


# 更新宿舍信息
def update_dormitory(cursor, dno, dadmin, dtel, dfloor):
    sql = "update dormitory set (dadmin, dtel, dfloor) = ('{}', '{}', '{}') where dno = '{}'".format(
        dadmin, dtel, dfloor, dno)
    cursor.execute(sql)
    return cursor.rowcount


# 更新食堂信息
def update_canteen(cursor, wno, wname, wadmin, wtel):
    sql = "update canteen set (wname, wadmin, wtel) = ('{}', '{}', '{}') where wno = '{}'".format(
        wname, wadmin, wtel, wno)
    cursor.execute(sql)
    return cursor.rowcount


# 更新校门信息
def update_gate(cursor, gno, gname, gadmin, gtel):
    sql = "update gate set (gname, gadmin, gtel) = ('{}', '{}', '{}') where gno = '{}'".format(
        gname, gadmin, gtel, gno)
    cursor.execute(sql)
    return cursor.rowcount
