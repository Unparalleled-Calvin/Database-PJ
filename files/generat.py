with open(r"./stu.sql", "w") as f:
    with open(r"./info.csv", "r") as ff:
        info = ff.readlines()
        for each in info:
            stu = each.split(',')
            f.write("insert into person values('{}', '{}');\n".format(stu[0], stu[1][:-1]))
            f.write("insert into card values('{}', '{}', '{}', '{}', {}, '{}');\n".format(stu[0], 0, 'now()', '000000', '2', 1))
            f.write("insert into student values('{}', '{}', '{}');\n\n".format(stu[0], '2019-9-1', '19计算机科学与技术'))

