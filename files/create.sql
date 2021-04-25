create TABLE person(
    ID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    check(length(ID) in (5, 6, 10))
);
create TABLE teacher(
    ID VARCHAR(10) PRIMARY KEY,
    age int NOT NULL,
    rank VARCHAR(20),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 6)
);
create TABLE student(
    ID VARCHAR(10) PRIMARY KEY,
    enrolmentdt DATE NOT NULL,
    class VARCHAR(20) NOT NULL,
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 10)
);
create TABLE others(
    ID VARCHAR(10) PRIMARY KEY,
    work VARCHAR(20) NOT NULL,
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    check(length(ID) = 5)
);
create TABLE domitory(
    dno INT PRIMARY KEY,
    dadmin VARCHAR(10) NOT NULL,
    dtel VARCHAR(11) NOT NULL,
    dfloor INT NOT NULL
);
create TABLE card(
    ID VARCHAR(10),
    remainingsum NUMERIC(10, 2) DEFAULT 0,
    carddate TIMESTAMP DEFAULT now(),
    cdno INT DEFAULT null,
    valid INT DEFAULT 0,
    PRIMARY KEY(ID, carddate),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(cdno) REFERENCES domitory(dno) ON DELETE
    SET DEFAULT ON UPDATE CASCADE
);
create TABLE canteen(
    wno INT PRIMARY KEY,
    wname VARCHAR(20) NOT NULL,
    wadmin VARCHAR(10) NOT NULL,
    wtel VARCHAR(11) NOT NULL
);
create TABLE gate(
    gno INT PRIMARY KEY,
    gname VARCHAR(20) NOT NULL,
    gadmin VARCHAR(10) NOT NULL,
    gtel VARCHAR(11) NOT NULL
);
create TABLE consume(
    wno INT NOT NULL,
    ID VARCHAR(10) NOT NULL,
    consumetm TIMESTAMP DEFAULT now(),
    cuisineid INT NOT NULL,
    amount numeric(10, 2) NOT NULL,
    PRIMARY KEY(wno, ID, consumetm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(wno) REFERENCES canteen(wno) ON DELETE CASCADE ON UPDATE CASCADE
);
create TABLE record(
    ID VARCHAR(10) NOT NULL,
    gno INT NOT NULL,
    recordtm TIMESTAMP DEFAULT now(),
    inout VARCHAR(3) NOT NULL,
    PRIMARY KEY(ID, gno, recordtm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(gno) REFERENCES gate(gno) ON DELETE CASCADE ON UPDATE CASCADE,
    check(inout in('in', 'out'))
);
create TABLE access(
    ID VARCHAR(10) NOT NULL,
    dno int NOT NULL,
    accesstm TIMESTAMP DEFAULT now(),
    PRIMARY KEY(ID, dno, accesstm),
    foreign key(ID) REFERENCES person(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key(dno) REFERENCES domitory(dno) ON DELETE CASCADE ON UPDATE CASCADE
);
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
    where valid = 1
);
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
    where valid = 1
);
create view v_access as(
    select ID,
        name,
        dno,
        accesstm
    from person
        natural join card
        natural join access
    where valid = 1
);
create or replace function charge(fID varchar(10), famount numeric(10, 2)) returns numeric as $$ begin
update card
set remainingsum = remainingsum + famount
where fID = card.ID
    and card.valid = 1;
return (
    select remainingsum
    from card
    where fID = card.ID
        and card.valid = 1
);
end;
$$ language plpgsql;
create or replace procedure eat(
        in pID varchar(10),
        in pwno int,
        in pcuisineid int,
        in pamount numeric(10, 2)
    ) as $$ begin if pID not in(
        select ID
        from card
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
create or replace function valid_trigger() returns trigger as $$ begin
update card
set valid = 0
where card.ID = new.ID;
return new;
end;
$$ language plpgsql;
create trigger update_valid before
insert on card for each row execute procedure valid_trigger();