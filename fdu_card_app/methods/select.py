def select_with_cid(cursor, cid):
    sql = "select * from course where cid = \'{}\'".format(cid)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows