# 辅助函数
def dict(keylist, val):
    ret = {}
    for i in range(len(keylist)):
        ret[keylist[i]] = val[i]
    return ret


def ret(keylist, rows):
    data = []
    for row in rows:
        data.append(dict(keylist, row))
    return data


# 查询id
def select_id(cursor, id):
    sql = "select * from card where ID = '{}'".format(id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# 今日已用
def select_amount(cursor, id):
    sql = "select sum(amount) from v_consume where ID = '{}' and consumetm::date = now()::date".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows[0][0] == None:
        return 0
    else:
        return rows[0][0]


# 判断登录的用户名与密码是否正确
def check_identity(cursor, id, passwd):
    sql = "select ID, passwd from person natural join card where ID = '{}' and passwd = '{}' and valid <> 0".format(
        id, passwd)
    cursor.execute(sql)
    return cursor.rowcount


# 根据id查询用户名
def select_v_name(cursor, id):
    sql = "select name from person where ID = '{}'".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows[0][0]


# 查询食堂消费信息
def select_v_consume(cursor, id, start, end):
    sql = "select * from v_consume where ID = '{}' and consumetm::date between '{}' and '{}' order by consumetm".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'wname', 'cuisineid', 'consumetm', 'amount']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '餐厅', '菜肴', '时间', '金额']
    return (heads, [keylist], [data])


# 查询校门进出信息
def select_v_record(cursor, id, start, end):
    sql = "select * from v_record where ID = '{}' and recordtm::date between '{}' and '{}' order by recordtm".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'gname', 'recordtm', 'inout']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '校门', '时间', '进/出']
    return (heads, [keylist], [data])


# 查询宿舍门禁信息
def select_v_access(cursor, id, start, end):
    sql = "select * from v_access where ID = '{}' and accesstm::date between '{}' and '{}' order by recordtm".format(
        id, start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'dno', 'accesstm']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '宿舍', '时间']
    return (heads, [keylist], [data])


# 查询所在宿舍信息
def check_dormitory(cursor, id):
    sql = "select dno, dadmin, dtel, dfloor from domitory, card where domitory.cno = card.cdno and card.ID = '{}'".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['dno', 'dadmin', 'dtel', 'dfloor']
    data = ret(keylist, rows)
    heads = ['宿舍', '负责人', '电话', '层数']
    return (heads, [keylist], [data])


# 查询各宿舍信息
def select_dormitory(cursor):
    sql = "select dno, dadmin, dtel, dfloor from domitory"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['dno', 'dadmin', 'dtel', 'dfloor']
    data = ret(keylist, rows)
    heads = ['宿舍', '负责人', '电话', '层数']
    return (heads, [keylist], [data])


# 查询各餐厅信息
def select_canteen(cursor):
    sql = "select * from canteen"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['wno', 'wname', 'wadmin', 'wtel']
    data = ret(keylist, rows)
    heads = ['餐厅号', '餐厅', '负责人', '电话']
    return (heads, [keylist], [data])


# 查询各校门信息
def select_gate(cursor):
    sql = "select * from gate"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['gno', 'gname', 'gadmin', 'gtel']
    data = ret(keylist, rows)
    heads = ['校门号', '校门', '负责人', '电话']
    return (heads, [keylist], [data])


# 查询一卡通信息
def select_information(cursor, id):
    sql = "select id, name, remainingsum, carddate, cdno, valid from person natural join card where valid <> 0 and ID = '{}'".format(
        id)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'remainingsum', 'carddate', 'cdno', 'valid']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '余额', '开卡日期', '宿舍', '有效状态']
    return (heads, [keylist], [data])


# 以下功能仅提供给admin

# 查询所有教师信息
def select_teacher(cursor):
    sql = "select * from person natural join teacher"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'birthday', 'rank']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '出生日期', '职称']
    return (heads, [keylist], [data])


# 查询所有学生信息
def select_student(cursor):
    sql = "select * from person natural join student"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'enrolmentdt', 'class']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '入学日期', '班级']
    return (heads, [keylist], [data])


# 查询所有其他人员信息
def select_others(cursor):
    sql = "select * from person natural join others"
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['id', 'name', 'work']
    data = ret(keylist, rows)
    heads = ['学工号', '姓名', '工作']
    return (heads, [keylist], [data])


# 查询各餐厅营业额
def select_profit(cursor, start, end):
    sql = "select wno, wname, sum(amount) as profit from canteen natural join consume where consumetm between '{}' and '{}' group by wno, wname".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['wno', 'wname', 'profit']
    data = ret(keylist, rows)
    heads = ['餐厅号', '餐厅', '营业额']
    return (heads, [keylist], [data])


# 查询各校门进出次数
def select_record(cursor, start, end):
    sql = "select gno, gname, inout, count(inout) as times from gate natural join record where recordtm between '{}' and '{}' group by gno, gname, inout".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['gno', 'gname', 'inout', 'times']
    data = ret(keylist, rows)
    heads = ['校门号', '校门', '进/出', '次数']
    return (heads, [keylist], [data])


# 查询各寝室门禁次数
def select_access(cursor, start, end):
    sql = "select dno, count(*) as times from domitory natural join access where accesstm between '{}' and '{}' group by dno".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    keylist = ['dno', 'times']
    data = ret(keylist, rows)
    heads = ['宿舍号', '次数']
    return (heads, [keylist], [data])
