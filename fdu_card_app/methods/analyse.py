from pyecharts.charts import Bar
from pyecharts import options as opts


# 查询各餐厅营业额
def select_profit(cursor, start, end):
    sql = "select wno, wname, sum(amount) as profit from canteen natural join consume where consumetm::date between '{}' and '{}' group by wno, wname order by wno".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    sql1 = "select wno, wname from canteen except (select wno, wname from canteen natural join consume where consumetm::date between '{}' and '{}')".format(
        start, end)
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    for row in rows1:
        rows.append((row[0:2]+(0,)))
    rows.sort()
    bar = Bar()
    x = []
    y = []
    for row in rows:
        x.append((row[0], row[1]))
        y.append(row[2])
    bar.add_xaxis(x)
    bar.add_yaxis('营业额', y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title='各餐厅营业额'),
                        toolbox_opts=opts.ToolboxOpts(is_show=True))
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    bar.render(r"./graph.html")


# 查询各校门进出次数
def select_record_times(cursor, start, end):
    sql = "select gno, gname, inout, count(inout) as times from gate natural join record where recordtm::date between '{}' and '{}' group by gno, gname, inout order by gno".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    sql1 = "select gno, gname, 'in' from gate except (select gno, gname, inout from gate natural join record where recordtm::date between '{}' and '{}')".format(
        start, end)
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    for row in rows1:
        rows.append((row[0:2]+('in', 0)))
    sql2 = "select gno, gname, 'out' from gate except (select gno, gname, inout from gate natural join record where recordtm::date between '{}' and '{}')".format(
        start, end)
    cursor.execute(sql2)
    rows2 = cursor.fetchall()
    for row in rows2:
        rows.append((row[0:2]+('out', 0)))
    rows.sort()
    bar = Bar()
    x = []
    yin = []
    yout = []
    for row in rows:
        if (row[0], row[1]) not in x:
            x.append((row[0], row[1]))
        if(row[2] == 'in'):
            yin.append(row[3])
        else:
            yout.append(row[3])
    bar.add_xaxis(x)
    bar.add_yaxis('进校', yin)
    bar.add_yaxis('出校', yout)
    bar.set_global_opts(title_opts=opts.TitleOpts(title='各校门进出情况'),
                        toolbox_opts=opts.ToolboxOpts(is_show=True))
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    bar.render(r"./graph.html")


# 查询各寝室门禁次数
def select_access_times(cursor, start, end):
    sql = "select dno, count(*) as times from domitory natural join access where accesstm::date between '{}' and '{}' group by dno order by dno".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    sql1 = "select dno from domitory except (select dno from domitory natural join access where accesstm::date between '{}' and '{}')".format(
        start, end)
    cursor.execute(sql1)
    rows1 = cursor.fetchall()
    for row in rows1:
        rows.append((row[0:1]+(0,)))
    rows.sort()
    bar = Bar()
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    bar.add_xaxis(x)
    bar.add_yaxis('次数', y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title='各宿舍号门禁总数'),
                        toolbox_opts=opts.ToolboxOpts(is_show=True))
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    bar.render(r"./graph.html")


# 查询各菜肴销量
def select_cuisineid_times(cursor, start, end):
    sql = "select cuisineid, count(*) as sell from consume where consumetm::date between '{}' and '{}' group by cuisineid order by cuisineid".format(
        start, end)
    cursor.execute(sql)
    rows = cursor.fetchall()
    rows.sort()
    bar = Bar()
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    bar.add_xaxis(x)
    bar.add_yaxis('销量', y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title='各菜肴销量'),
                        toolbox_opts=opts.ToolboxOpts(is_show=True))
    bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    bar.render(r"./graph.html")
