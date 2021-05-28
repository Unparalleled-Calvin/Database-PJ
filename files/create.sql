--author：叶俊杰 19307130140
--
--内容：数据库表格建立（共11张）、视图（共3张）、函数（共1个）、过程（共2个）、触发器（共2个）
--
--
--人员信息表
create TABLE person(
    ID VARCHAR(11) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    photo VARCHAR(50) DEFAULT 'g',
    check(length(ID) in (5, 6, 11))
);
--教师信息表
create TABLE teacher(
    ID VARCHAR(11) PRIMARY KEY,
    birthday DATE NOT NULL,
    rank VARCHAR(20),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 6)
);
--学生信息表
create TABLE student(
    ID VARCHAR(11) PRIMARY KEY,
    enrolmentdt DATE NOT NULL,
    class VARCHAR(20) NOT NULL,
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 11)
);
--其他人员信息表
create TABLE others(
    ID VARCHAR(11) PRIMARY KEY,
    work VARCHAR(20) NOT NULL,
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 5)
);
--宿舍信息表
create TABLE domitory(
    dno INT PRIMARY KEY,
    dadmin VARCHAR(50) NOT NULL,
    dtel VARCHAR(11) NOT NULL,
    dfloor INT NOT NULL
);
--一卡通信息表
create TABLE card(
    ID VARCHAR(11),
    remainingsum NUMERIC(10, 2) DEFAULT 0,
    carddate TIMESTAMP DEFAULT now(),
    passwd VARCHAR(50) DEFAULT '000000',
    cdno INT DEFAULT null,
    valid INT DEFAULT 1,
    PRIMARY KEY(ID, carddate),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(cdno) REFERENCES domitory(dno) ON DELETE
    SET DEFAULT ON UPDATE CASCADE
);
--餐厅信息表
create TABLE canteen(
    wno INT PRIMARY KEY,
    wname VARCHAR(50) NOT NULL,
    wadmin VARCHAR(50) NOT NULL,
    wtel VARCHAR(11) NOT NULL
);
--校门信息表
create TABLE gate(
    gno INT PRIMARY KEY,
    gname VARCHAR(50) NOT NULL,
    gadmin VARCHAR(50) NOT NULL,
    gtel VARCHAR(11) NOT NULL
);
--消费信息表
create TABLE consume(
    wno INT NOT NULL,
    ID VARCHAR(11) NOT NULL,
    consumetm TIMESTAMP DEFAULT now(),
    cuisineid INT NOT NULL,
    amount numeric(10, 2) NOT NULL,
    PRIMARY KEY(wno, ID, consumetm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(wno) REFERENCES canteen(wno) ON DELETE CASCADE ON UPDATE CASCADE
);
--进出校记录表
create TABLE record(
    ID VARCHAR(11) NOT NULL,
    gno INT NOT NULL,
    recordtm TIMESTAMP DEFAULT now(),
    inout VARCHAR(3) NOT NULL,
    PRIMARY KEY(ID, gno, recordtm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(gno) REFERENCES gate(gno) ON DELETE CASCADE ON UPDATE CASCADE,
    check(inout in('in', 'out'))
);
--门禁信息表
create TABLE access(
    ID VARCHAR(11) NOT NULL,
    dno int NOT NULL,
    accesstm TIMESTAMP DEFAULT now(),
    PRIMARY KEY(ID, dno, accesstm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(dno) REFERENCES domitory(dno) ON DELETE CASCADE ON UPDATE CASCADE
);
--视图：消费信息
create view v_consume as(
    select ID,
        name,
        wname,
        cuisineid,
        consumetm,
        amount
    from person
        natural join card
        natural join canteen
        natural join consume
    where valid <> 0
);
--视图：进出校记录
create view v_record as(
    select ID,
        name,
        gname,
        recordtm,
        inout
    from person
        natural join card
        natural join gate
        natural join record
    where valid <> 0
);
--视图：门禁记录
create view v_access as(
    select ID,
        name,
        dno,
        accesstm
    from person
        natural join card
        natural join access
    where valid <> 0
);
--函数：一卡通余额充值
create or replace function charge(fID varchar(11), famount numeric(10, 2)) returns numeric as $$ begin
update card
set remainingsum = remainingsum + famount
where fID = card.ID
    and card.valid <> 0;
return (
    select remainingsum
    from card
    where fID = card.ID
        and card.valid <> 0
);
end;
$$ language plpgsql;
--过程：食堂就餐
create or replace procedure eat(
        in pID varchar(11),
        in pwno int,
        in pcuisineid int,
        in pamount numeric(10, 2)
    ) as $$ begin if pID not in(
        select ID
        from card
        where valid = 1
    ) then raise notice 'Failed. The ID is error.';
elsif pwno not in(
    select wno
    from canteen
) then raise notice 'Failed. The wno is error.';
elsif pamount > (
    select remainingsum
    from card
    where card.ID = pID
        and card.valid = 1
) then raise notice 'Failed. The balance is not enough.';
else
insert into consume(wno, ID, cuisineid, amount)
values(pwno, pID, pcuisineid, pamount);
end if;
end;
$$ language plpgsql;
--过程：进出校门
create or replace procedure in_and_out(
        in pID varchar(11),
        in pgno int,
        in pinout varchar(3)
    ) as $$ begin if pID not in(
        select ID
        from card
        where valid = 1
    ) then raise notice 'Failed. The ID is error.';
elsif pgno not in(
    select gno
    from gate
) then raise notice 'Failed. The gno is error.';
elsif pinout not in('in', 'out') then raise notice 'Failed. The inout is wrong.';
else
insert into record(ID, gno, inout)
values(pID, pgno, pinout);
end if;
end;
$$ language plpgsql;
--过程：回寝
create or replace procedure back(
        in pID varchar(11),
        in pdno int
    ) as $$ begin if pID not in(
        select ID
        from card
        where valid = 1
    ) then raise notice 'Failed. The ID is error.';
elsif pdno not in(
    select dno
    from domitory
) then raise notice 'Failed. The dno is error.';
elsif pdno not in(
    select cdno
    from card
    where card.ID = pID
        and card.valid = 1
)
or (
    select cdno
    from card
    where card.ID = pID
        and card.valid = 1
) is null then raise notice 'Failed. The ID can not access to the gno.';
else
insert into access(ID, dno)
values(pID, pdno);
end if;
end;
$$ language plpgsql;
--触发器：消费后及时更新余额
create or replace function consume_trigger() returns trigger as $$ begin
update card
set remainingsum = remainingsum - new.amount
where card.ID = new.ID
    and card.valid = 1;
return new;
end;
$$ language plpgsql;
create trigger consume_update
after
insert on consume for each row execute procedure consume_trigger();
--触发器：卡挂失后及时将原卡置为无效
create or replace function valid_trigger() returns trigger as $$ begin
update card
set valid = 0
where card.ID = new.ID;
return new;
end;
$$ language plpgsql;
create trigger update_valid before
insert on card for each row execute procedure valid_trigger();
--插入管理员用户
insert INTO person
VALUES('admin', 'admin');
insert into others
VALUES('admin', 'admin');
insert into card(ID)
VALUES('admin')