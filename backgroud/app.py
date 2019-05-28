from flask import Flask, jsonify, request, g, session, redirect, url_for, render_template
from db import DbSystem
import os, pymysql
from flask_cors import *

db_manager = DbSystem()
app = Flask(__name__)
app.config['SECRET_KEY'] = "abcderf"
CORS(app, supports_credentials=True)


@app.before_request
def get_request():
    user_id = session.get('user_id')
    if user_id:
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from employee where id = {}".format(user_id))
        data = cursor.fetchone()
        cursor.fetchall()
        if data:
            description = [i[0] for i in cursor.description]
            user = {i: j for i, j in zip(description, data)}
            g.user = user
        else:
            redirect(url_for('login'))


@app.context_processor
def send_user():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {'user': None}


@app.route('/')
def hello_world():
    return render_template("index.html")


# 登录 {‘user_id’(int), 'password','remember'(bool)}
@app.route('/api/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')
    cursor = db_manager.get_read_only_cursor()
    cursor.execute("select password,level,name from employee where id = {}".format(int(user_id)))
    data_base_pass, level, name = cursor.fetchone()
    if data_base_pass:
        if data_base_pass == request.json.get('password'):
            session['user_id'] = user_id
            if request.json.get('remember'):
                session.permanent = True
            return jsonify({
                'status': True,
                'userID': user_id,
                'level': level,
                'name': name
            })
    return jsonify(data={'status': False, 'failCode': 'ID或密码错误'})


@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({'status': True})


# 是否登陆
@app.route('/api/islogin', methods=['GET'])
def islogin():
    if hasattr(g, 'user'):
        return jsonify(
            {"status": True, "level": g.user.get("level"), "name": g.user.get("name"), "id": g.user.get("id")})
    return jsonify({"status": False, "code": "请登陆"})


# 添加员工，{'name', 'dept_name', 'level'(int) , 'salary'(float)} level > 7
@app.route('/api/add_employee', methods=['POST'])
def add_employee():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("insert into employee (name, dept_name, level, salary) values('{}', '{}', {}, {});".format(
                request.json.get('name'),
                request.json.get('dept_name'),
                int(request.json.get('level')),
                float(request.json.get('salary'))))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "code": "权限不足"})
    return jsonify({"status": False, "code": "请登陆"})


# 开除员工, {'id'}, level > 7
@app.route('/api/fire_employee', methods=['POST'])
def fire_employee():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("update employee set state = false where id = {}".format(int(request.json.get('id'))))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "code": "权限不足"})
    return jsonify({"status": False, "code": "请登陆"})


# 获取, {'id'(int)}
@app.route('/api/get_one_employee', methods=['POST'])
def get_one_employee():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select id, name, dept_name, level, salary, state from employee where  id = {}".format(
            int(request.json.get("id"))))
        data = cursor.fetchone()
        description = [i[0] for i in cursor.description]
        res = {i: j for i, j in zip(description, data)}
        res["salary"] = float(res["salary"])
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 选择员工, {'all'(bool), 'dept_name', 'fired'(bool)}
@app.route('/api/get_employee', methods=['POST'])
def get_employee():
    if hasattr(g, 'user'):
        cursor = db_manager.get_cursor()
        if request.json.get('all'):
            sql = 'select id, name, dept_name, level, salary, state  from employee where state = {}'.format(
                int(not request.json.get("fired")))
        else:
            sql = "select id, name, dept_name, level, salary, state  from employee where dept_name = '{}' and state = {}".format(
                request.json.get('dept_name'), int(not request.json.get("fired")))
        cursor.execute(sql)
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        db_manager.push_back_cursor(cursor)
        res = [{i: j for i, j in zip(description, line)} for line in data]
        for i in res:
            i["salary"] = float(i["salary"])
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 修改密码, {'old_pwd', 'new_pwd'}
@app.route('/api/change_password', methods=['POST'])
def change_password():
    if hasattr(g, 'user'):
        if g.user["password"] == request.json.get('old_pwd'):
            cursor = db_manager.get_cursor()
            cursor.execute(
                "update employee set password = '{}' where id = {}".format(request.json.get('new_pwd'), g.user['id']))
            g.user['password'] = request.json.get('new_pwd')
            db_manager.push_back_cursor(cursor)
            return jsonify({'status': True})
        else:
            return jsonify({"status": False, "code": "旧密码输入错误"})
    return jsonify({"status": False, "code": "请登陆"})


# 获取用户日志
@app.route('/api/get_employee_log', methods=['GET'])
def get_employee_log():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from employee_log")
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        for i in res:
            i['date_time'] = i['date_time'].timestamp()
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 更改员工部门, {'id'(int),'dept_name'}, level > 7
@app.route('/api/change_employee_dept', methods=['POST'])
def change_employee_dept():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("update employee set dept_name = '{}' where id = {}".format(request.json.get('dept_name'),
                                                                                       int(request.json.get('id'))))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "code": "权限不足"})
    return jsonify({"status": False, "code": "请登陆"})


# 更改员工工资, {'id'(int),'salary'(float)}, level > 7
@app.route('/api/change_employee_salary', methods=['POST'])
def change_employee_salary():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("update employee set salary = {} where id = {}".format(float(request.json.get('salary')),
                                                                                  int(request.json.get('id'))))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "code": "权限不足"})
    return jsonify({"status": False, "code": "请登陆"})


# 更改员工等级, {'id'(int),'level'(float)}, level > 7
@app.route('/api/change_employee_level', methods=['POST'])
def change_employee_level():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("update employee set level = {} where id = {}".format(float(request.json.get('level')),
                                                                                 int(request.json.get('id'))))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
        else:
            return jsonify({"status": False, "code": "权限不足"})
    return jsonify({"status": False, "code": "请登陆"})


# 签到
@app.route('/api/check_in', methods=['GET'])
def check_in():
    if hasattr(g, 'user'):
        try:
            cursor = db_manager.get_cursor()
            cursor.execute('insert into check_in (person_id, date) values ({}, CURDATE())'.format(g.user['id']))
            db_manager.push_back_cursor(cursor)
        except pymysql.err.IntegrityError:
            return jsonify({'status': False, 'code': '已签到'})
        return jsonify({'status': True})
    return jsonify({"status": False, "code": "请登陆"})


# 查看是否签到
@app.route('/api/is_check_in', methods=['GET'])
def is_check_in():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute(
            'select count(*) from check_in where person_id = {} and  date = curdate()'.format(g.user.get('id')))
        data = cursor.fetchone()
        if data[0] == 0:
            return jsonify({'status': False})
        return jsonify({'status': True})
    return jsonify({"status": False, "code": "请登陆"})


# 查看签到记录,POST {'id'(int)} POST, level > 7
@app.route('/api/check_in_log', methods=['GET', 'POST'])
def check_in_log():
    if hasattr(g, 'user'):
        if request.method == 'GET':
            cursor = db_manager.get_read_only_cursor()
            cursor.execute('select date from check_in where person_id = {}'.format(g.user.get('id')))
            data = cursor.fetchall()
            if data:
                res = ["{}-{}-{}".format(i[0].year, i[0].month, i[0].day) for i in data]
            else:
                res = None
            return jsonify({'status': True, 'data': res})
        else:
            if g.user.get('level') > 7:
                cursor = db_manager.get_read_only_cursor()
                cursor.execute('select date from check_in where person_id = {}'.format(request.json.get('id')))
                data = cursor.fetchall()
                if data:
                    res = ["{}-{}-{}".format(i[0].year, i[0].month, i[0].day) for i in data]
                else:
                    res = None
                return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 查看未签到的人, {'all'(bool), 'dept_name'}
@app.route('/api/get_uncheck_in', methods=['POST'])
def get_uncheck_in():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        if request.json.get('all'):
            sql = 'select id, name, dept_name, level from employee where id not in (select person_id from check_in where date = curdate()) and state = 1'
        else:
            sql = "select id, name, dept_name, level from employee where id not in (select person_id from check_in where date = curdate()) and state = 1 and dept_name = '{}'}".format(
                request.json.get('dept_name'))
        cursor.execute(sql)
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 获取所有部门
@app.route('/api/get_department', methods=['GET'])
def get_dept_name():
    cursor = db_manager.get_read_only_cursor()
    cursor.execute("select * from department")
    data = cursor.fetchall()
    data = [i[0] for i in data]
    return jsonify({'status': True, 'data': data})


# 获取部门主管, {'all'(bool), 'dept_name}
@app.route('/api/get_dept_manager', methods=['POST'])
def get_dept_manager():
    cursor = db_manager.get_read_only_cursor()
    if request.json.get('all'):
        sql = 'select dept_manager.dept_name, name from dept_manager left join employee e on dept_manager.manager_id = e.id'
    else:
        sql = "select dept_manager.dept_name, name from dept_manager left join employee e on dept_manager.manager_id = e.id where dept_manager.dept_name = '{}'}".format(
            request.json.get('dept_name'))
    cursor.execute(sql)
    data = cursor.fetchall()
    description = [i[0] for i in cursor.description]
    res = [{i: j for i, j in zip(description, line)} for line in data]
    return jsonify({'status': True, 'data': res})


# 添加部门, {'dept_name'}
@app.route('/api/add_dept', methods=['POST'])
def add_dept():
    if hasattr(g, 'user'):
        if g.user.get('level') == 10:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("insert into department values ('{}')".format(request.json.get('dept_name')))
                db_manager.push_back_cursor(cursor)
                return jsonify({"status": True})
            except pymysql.err.IntegrityError:
                return jsonify({'status': False, 'code': '当前部门已存在'})
    return jsonify({"status": False, "code": "权限不足"})


# 添加部门主管, {'dept_name', 'id'(int)}
@app.route('/api/add_dept_manager', methods=['POST'])
def add_dept_manager():
    if hasattr(g, 'user'):
        if g.user.get('level') == 10:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("insert into dept_manager values ('{}',{})".format(request.json.get('dept_name'),
                                                                                  request.json.get('id')))
                db_manager.push_back_cursor(cursor)
                return jsonify({"status": True})
            except pymysql.err.IntegrityError:
                return jsonify({'status': False, 'code': '当前部门已有主管'})
            except pymysql.err.InternalError:
                return jsonify({'status': False, 'code': 'level 大于 10 才能当主管'})
    return jsonify({"status": False, "code": "权限不足"})


# 删除部门主管, {'dept_name'}
@app.route('/api/del_dept_manager', methods=['POST'])
def del_dept_manager():
    if hasattr(g, 'user'):
        if g.user.get('level') == 10:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("delete from dept_manager where dept_name = '{}'".format(request.json.get('dept_name')))
                db_manager.push_back_cursor(cursor)
                return jsonify({"status": True})
            except pymysql.err.InternalError:
                return jsonify({'status': False, 'code': '未找到主管'})
    return jsonify({"status": False, "code": "权限不足"})


# 添加项目, {'project_name'}
@app.route('/api/add_project', methods=['POST'])
def add_project():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("insert into project (pro_name) values ('{}')".format(request.json.get('project_name')))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
    return jsonify({"status": False, "code": "权限不足"})


# 查找项目, {'finished'(bool)}
@app.route('/api/find_project', methods=['POST'])
def find_project():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from project where state = {}".format(int(request.json.get('finished'))))
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        return jsonify({"status": True, "data": res})
    return jsonify({"status": False, "code": "权限不足"})


# 查找项目, {'id'(int)}
@app.route('/api/get_project', methods=['POST'])
def get_project():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from project where pro_id = {}".format(int(request.json.get('id'))))
        data = cursor.fetchone()
        description = [i[0] for i in cursor.description]
        res = {i: j for i, j in zip(description, data)}
        return jsonify({"status": True, "data": res})
    return jsonify({"status": False, "code": "权限不足"})


# 删除项目人员, {'pro_id','employee_id'}
@app.route('/api/del_employee_pro', methods=['POST'])
def del_employee_pro():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("delete from pro_employee where pro_id = {} and employee_id = {} ".format(
                    request.json.get('pro_id'), request.json.get('employee_id')))
                db_manager.push_back_cursor(cursor)
                return jsonify({"status": True})
            except pymysql.err.InternalError:
                return jsonify({'status': False, 'code': '没找到此成员'})
    return jsonify({"status": False, "code": "权限不足"})


# 设置项目主管, {'pro_id'(int), 'leader'(int)}
@app.route('/api/add_project_leader', methods=['POST'])
def add_project_leader():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("update project set leader = {} where pro_id = {};".format(request.json.get('leader'),
                                                                                          request.json.get('pro_id')))
                db_manager.push_back_cursor(cursor)
            except pymysql.err.InternalError as e:
                return jsonify({'status': False, 'code': 'level 大于 7 才能当leader'})
            return jsonify({"status": True})
    return jsonify({"status": False, "code": "权限不足"})


# 标记项目完成, {'pro_id'(int)}
@app.route('/api/set_pro_finish', methods=['POST'])
def set_pro_finish():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            cursor = db_manager.get_cursor()
            cursor.execute("update project set state = TRUE where pro_id = {}".format(request.json.get('pro_id')))
            db_manager.push_back_cursor(cursor)
            return jsonify({"status": True})
    return jsonify({"status": False, "code": "权限不足"})


# 给项目安排员工, {'pro_id'(int), 'emp_id'(int)}
@app.route('/api/add_project_employee', methods=['POST'])
def add_project_employee():
    if hasattr(g, 'user'):
        if g.user.get('level') > 7:
            try:
                cursor = db_manager.get_cursor()
                cursor.execute("insert into pro_employee values ({},{})".format(request.json.get('pro_id'),
                                                                                request.json.get('emp_id')))
                db_manager.push_back_cursor(cursor)
            except pymysql.err.InternalError as e:
                print(e)
                return jsonify({'status': False, 'code': '一个员工最多参加三个项目'})
        return jsonify({"status": True})
    return jsonify({"status": False, "code": "权限不足"})


# 获取员工参加的项目, {'emp_id'(int)}
@app.route('/api/get_employee_pro', methods=['POST'])
def get_employee_pro():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute(
            "select  pro_employee.pro_id, pro_name from pro_employee left join project on pro_employee.pro_id = project.pro_id where employee_id = {}".format(
                request.json.get('emp_id')))
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "权限不足"})


# 获取项目的成员, {'id'(int)}
@app.route('/api/get_pro_employee', methods=['POST'])
def get_pro_employee():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute(
            "select name, id from (select pro_employee.pro_id, pro_name, employee_id from pro_employee left join project on pro_employee.pro_id = project.pro_id where project.pro_id = {}) as T left join employee on employee_id = id".format(
                request.json.get('id')))
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "权限不足"})


# 获取项目日志, {'pro_id'(int)}
@app.route('/api/get_pro_log', methods=['POST'])
def get_pro_log():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from pro_log where pro_id = {}".format(request.json.get('pro_id')))
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        for i in res:
            i['date_time'] = i['date_time'].timestamp()
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 获取所有项目日志
@app.route('/api/get_project_log', methods=['GET'])
def get_project_log():
    if hasattr(g, 'user'):
        cursor = db_manager.get_read_only_cursor()
        cursor.execute("select * from pro_log")
        data = cursor.fetchall()
        description = [i[0] for i in cursor.description]
        res = [{i: j for i, j in zip(description, line)} for line in data]
        for i in res:
            i['date_time'] = i['date_time'].timestamp()
        return jsonify({'status': True, 'data': res})
    return jsonify({"status": False, "code": "请登陆"})


# 超级权限!!!, 可执行一切SQL, 慎用!!!, {'sql'}, level = 10
@app.route('/api/super_user', methods=['POST'])
def super_user():
    if hasattr(g, 'user'):
        if g.user.get('level') == 10:
            sql = request.json.get('sql')
            res = []
            description = []
            try:
                cursor = db_manager.get_cursor()
                if cursor.execute(sql):
                    res = [[j for j in i] for i in cursor.fetchall()]
                    description = [i[0] for i in cursor.description]
                db_manager.push_back_cursor(cursor)
            except Exception as e:
                res.append(e.args)
            print(res)
            for i in res:
                for index, j in enumerate(i):
                    if str(type(j)) == "<class 'decimal.Decimal'>":
                        i[index] = float(j)
                    elif str(type(j)) == "<class 'datetime.datetime'>":
                        i[index] = j.timestamp()
            return jsonify({"status": True, "data": res, "des": description})
    return jsonify({"status": False, "code": "权限不足"})


if __name__ == '__main__':
    app.debug = True
    app.run()
