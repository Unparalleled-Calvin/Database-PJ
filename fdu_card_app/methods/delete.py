# 删除人员信息
def delete_person(cursor, id):
    sql = "delete from person where ID = '{}'".format(id)
    cursor.execute(sql)
    return cursor.rowcount


# 删除宿舍
def delete_dormitory(cursor, dno):
    sql = "delete from domitory where dno = '{}'".format(dno)
    cursor.execute(sql)
    return cursor.rowcount


# 删除餐厅
def delete_canteen(cursor, wno):
    sql = "delete from canteen where wno = '{}'".format(wno)
    cursor.execute(sql)
    return cursor.rowcount


# 删除校门
def delete_gate(cursor, gno):
    sql = "delete from gate where gno = '{}'".format(gno)
    cursor.execute(sql)
    return cursor.rowcount
