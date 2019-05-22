set names utf8;
set names utf8;
insert into department
values ('开发部');
insert into department
values ('市场部');
insert into department
values ('人力资源部');
insert into department
values ('产品部');

insert into employee (name, dept_name, level, salary)
values ('唐家阳', '人力资源部', 1, 200);
insert into employee (name, dept_name, level, salary)
values ('尹瑞涛', '开发部', 10, 200000);
insert into employee (name, dept_name, level, salary)
values ('康智信', '开发部', 7, 200000);
insert into employee (name, dept_name, level, salary)
values ('a', '开发部', 7, 200000);
insert into employee (name, dept_name, level, salary)
values ('b', '开发部', 7, 200000);
insert into employee (name, dept_name, level, salary)
values ('c', '开发部', 7, 200000);
insert into dept_manager
values ('人力资源部', 2);


select *
from employee;
select *
from employee_log;
select *
from dept_manager;
update employee
set level = 7
where id = 2;
insert into project (pro_name, leader)
values ('Test Project', 3);
update employee
set level = 3
where id = 3;
insert into project (pro_name)
values ('New Test');
update project
set leader = 2
where pro_id = 1;
update project
set leader = null
where pro_id = 1;
insert into project (pro_name)
values ('New Test 2');

insert into project (pro_name)
values ('New Test 3');
insert into project (pro_name)
values ('New Test 4');

insert into pro_employee
values (1, 1);
insert into pro_employee
values (2, 2);
insert into pro_employee
values (3, 1);
insert into pro_employee
values (4, 1);
insert into pro_employee
values (2, 1);
insert into pro_employee
values (5, 1);

delete
from pro_employee
where employee_id = 1
  and pro_id = 3;