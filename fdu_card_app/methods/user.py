# 此函数不应被前端调用，如有后端需要，其中权限问题将由后端依据实际情况完善
def create_user(cursor, db, usr, password):
    sql1 = "create user \"{}\" with password '{}'".format(usr, password)
    cursor.execute(sql1)
    sql2 = "grant all privileges on database {} to \"{}\"".format(db, usr)
    cursor.execute(sql2)
    return cursor.rowcount
