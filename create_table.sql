drop table if exists pro_log;
drop table if exists pro_employee;
drop table if exists project;
drop table if exists employee_log;
drop table if exists dept_manager;
drop table if exists check_in;
drop table if exists employee;
drop table if exists department;
CREATE TABLE department
(
    dept_name VARCHAR(20) not null,
    PRIMARY KEY (dept_name)
);
CREATE TABLE employee
(
    id        INTEGER(11) AUTO_INCREMENT,
    name      VARCHAR(20)    not null,
    dept_name VARCHAR(20)    not null,
    level     integer(1)     not null,
    salary    DECIMAL(11, 2) not null,
    password  varchar(20)    not null default '123456',
    state     boolean                 default true,
    PRIMARY KEY (id),
    FOREIGN KEY (dept_name) references department (dept_name)
);

CREATE TABLE dept_manager
(
    dept_name  VARCHAR(20) not null,
    manager_id INTEGER(11) not null,
    FOREIGN KEY (dept_name) REFERENCES department (dept_name),
    FOREIGN KEY (manager_id) REFERENCES employee (id),
    PRIMARY KEY (dept_name)
);
CREATE TABLE employee_log
(
    id        INTEGER(11) not null,
    operation VARCHAR(20) not null,
    old       VARCHAR(20),
    new       VARCHAR(20) not null,
    date_time DATETIME default now(),
    foreign key (id) references employee (id)
);
CREATE TABLE check_in
(
    date      TIMESTAMP   not null default CURRENT_TIMESTAMP,
    person_id INTEGER(11) not null,
    primary key (date, person_id)
);
CREATE TABLE project
(
    pro_id      INTEGER(11) auto_increment not null,
    pro_name    VARCHAR(20)                not null,
    leader      INTEGER(11) default null,
    create_date TIMESTAMP   default CURRENT_TIMESTAMP,
    state       BOOLEAN     default false,
    primary key (pro_id),
    foreign key (leader) references employee (id)
);
CREATE TABLE pro_employee
(
    pro_id      INTEGER(11) not null,
    employee_id INTEGER(11) not null,
    primary key (pro_id, employee_id),
    foreign key (pro_id) references project (pro_id),
    foreign key (employee_id) references employee (id)
);
CREATE TABLE pro_log
(
    pro_id    INTEGER(11) not null,
    operation VARCHAR(20) not null,
    info      VARCHAR(40),
    date_time DATETIME default now(),
    foreign key (pro_id) references project (pro_id)
);

drop trigger if exists employee_add_check;
CREATE TRIGGER employee_add_check
    AFTER INSERT
    on employee
    FOR EACH ROW
BEGIN
    IF NEW.level > 10 THEN update employee set level = 10 where id = new.id; end if;
    INSERT into employee_log (id, operation, old, new) values (new.id, 'ADD', null, new.name);
end;

drop trigger if exists employee_change_check;
CREATE TRIGGER employee_change_check
    AFTER UPDATE
    on employee
    FOR EACH ROW
BEGIN
    IF NEW.level > 10 THEN update employee set level = 10 where id = new.id; end if;
    IF NEW.name != old.name then
        INSERT into employee_log (id, operation, old, new) values (new.id, 'change name', old.name, new.name);
    end if;
    IF NEW.dept_name != old.dept_name then
        INSERT into employee_log (id, operation, old, new)
        values (new.id, 'change department', old.dept_name, new.dept_name);
    end if;
    IF NEW.level != old.level then
        IF old.level >= 10 and new.level < 10 then
            delete from dept_manager where manager_id = new.id;
        end if;
        IF old.level >= 7 and NEW.level < 7 then
            update project set leader = NULL where leader = NEW.id;
        end if;
        INSERT into employee_log (id, operation, old, new) values (new.id, 'change level', old.level, new.level);
    end if;
    IF NEW.salary != old.salary then
        INSERT into employee_log (id, operation, old, new) values (new.id, 'change salary', old.salary, new.salary);
    end if;
    IF new.state = false then
        delete from dept_manager where manager_id = new.id;
        delete from pro_employee where employee_id = new.id;
        update project set leader = NULL where leader = new.id;
        insert into employee_log (id, operation, old, new) VALUES (new.id, 'Fire a employ', old.state, new.state);
    end if;
end;

drop trigger if exists project_create;
CREATE TRIGGER project_create
    BEFORE INSERT
    on project
    FOR EACH ROW
BEGIN
    if NEW.leader is not null then
        set @id = (select level from employee where employee.id = NEW.leader);
        if @id < 7 then
            SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT = 'This level has no access to lead a project';
        end if;
    end if;
end;

drop trigger if exists project_create_log;
CREATE TRIGGER project_create_log
    AFTER INSERT
    on project
    FOR EACH ROW
BEGIN
    insert into pro_log (pro_id, operation, info) values (new.pro_id, 'CREATE Project', new.pro_name);
end;

drop trigger if exists project_change;
CREATE TRIGGER project_change
    BEFORE UPDATE
    on project
    FOR EACH ROW
BEGIN
    IF NEW.leader != OLD.leader or old.leader is null or new.leader is null then
        IF NEW.leader is not NULL then
            set @id = (select level from employee where employee.id = NEW.leader);
            if @id < 7 then
                SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT = 'This level has no access to lead a project';
            end if;
            insert into pro_log (pro_id, operation, info)
            values (new.pro_id, 'change leader',
                    concat('old leader: ', IFNULL(OLD.leader, 'NULL'), ', new leader: ', IFNULL(NEW.leader, 'NULL')));
        else
            insert into pro_log (pro_id, operation, info) values (new.pro_id, 'delete leader', old.leader);
        end if;
    end if;
    IF new.pro_name != old.pro_name then
        insert into pro_log (pro_id, operation, info)
        values (new.pro_id, 'change name', concat('old name: ', OLD.pro_name, ', new name: ', NEW.pro_name));
    end if;
end;

drop trigger if exists dept_manager_check;
CREATE TRIGGER dept_manager_check
    before insert
    on dept_manager
    FOR EACH ROW
BEGIN
    set @id = (select level from employee where employee.id = NEW.manager_id);
    if @id < 10 then
        SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT =
                'This level can\'t be a manager of a department, should bigger than 10';
    end if;
    update employee set dept_name = NEW.dept_name where employee.id = new.manager_id;
end;

drop trigger if exists dept_manager_update_check;
CREATE TRIGGER dept_manager_update_check
    before update
    on dept_manager
    FOR EACH ROW
BEGIN
    set @id = (select level from employee where employee.id = NEW.manager_id);
    if @id < 10 then
        SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT =
                'This level can\'t be a manager of a department, should bigger than 10';
    end if;
    update employee set dept_name = NEW.dept_name where employee.id = new.manager_id;
end;

drop trigger if exists employee_project_check;
CREATE TRIGGER employee_project_check
    before insert
    on pro_employee
    FOR EACH ROW
BEGIN
    set @count = (select count(*) from pro_employee where pro_employee.employee_id = new.employee_id);
    if @count >= 3 then
        SIGNAL SQLSTATE 'TX000' SET MESSAGE_TEXT = 'A employee can\'t do more than three project at the same time';
    end if;
    insert into pro_log (pro_id, operation, info) values (new.pro_id, 'add employee', new.employee_id);
end;

drop trigger if exists employee_pro_delete_check;
CREATE TRIGGER employee_pro_delete_check
    before delete
    on pro_employee
    FOR EACH ROW
BEGIN
    insert into pro_log (pro_id, operation, info) values (OLD.pro_id, 'delete employee', old.employee_id);
end;