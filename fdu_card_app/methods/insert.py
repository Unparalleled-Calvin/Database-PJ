def insert_person(cursor, id, name):
    sql = "insert into person values('{}', '{}')".format(id, name)
    cursor.execute(sql)
    return cursor.rowcount


def insert_teacher(cursor, id, birthday, rank):
    sql = "insert into teacher values('{}', '{}', '{}')".format(
        id, birthday, rank)
    cursor.execute(sql)
    return cursor.rowcount


def insert_student(cursor, id, enrolmentdt, stuclass):
    sql = "insert into student values('{}', '{}', '{}')".format(
        id, enrolmentdt, stuclass)
    cursor.execute(sql)
    return cursor.rowcount


def insert_others(cursor, id, work):
    sql = "insert into others values('{}', '{}')".format(
        id, work)
    cursor.execute(sql)
    return cursor.rowcount


def insert_domitory(cursor, dno, dadmin, dtel, dfloor):
    sql = "insert into domitory values('{}', '{}', '{}', '{}')".format(
        dno, dadmin, dtel, dfloor)
    cursor.execute(sql)
    return cursor.rowcount


def insert_card(cursor, id, remainingsum=0, carddate='now()', passwd='000000', cdno='null', valid=1):
    sql = "insert into card values('{}', '{}', '{}', '{}', {}, '{}')".format(
        id, remainingsum, carddate, passwd, cdno, valid)
    cursor.execute(sql)
    return cursor.rowcount


def insert_canteen(cursor, wno, wname, wadmin, wtel):
    sql = "insert into canteen values('{}', '{}', '{}', '{}')".format(
        wno, wname, wadmin, wtel)
    cursor.execute(sql)
    return cursor.rowcount


def insert_gate(cursor, gno, gname, gadmin, gtel):
    sql = "insert into gate values('{}', '{}', '{}', '{}')".format(
        gno, gname, gadmin, gtel)
    cursor.execute(sql)
    return cursor.rowcount


def insert_consume(cursor, wno, ID, cuisineid, amount):
    sql = "call eat('{}', '{}', '{}', '{}')".format(
        ID, wno, cuisineid, amount)
    cursor.execute(sql)
    return cursor.rowcount


def insert_record(cursor, ID, gno, inout):
    sql = "call in_and_out('{}', '{}', '{}')".format(
        ID, gno, inout)
    cursor.execute(sql)
    return cursor.rowcount


def insert_access(cursor, ID, dno):
    sql = "call in_and_out('{}', '{}')".format(
        ID, dno)
    cursor.execute(sql)
    return cursor.rowcount
