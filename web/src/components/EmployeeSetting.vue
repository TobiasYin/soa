<template>
    <div>
        <div v-if="ulevel > 7">
            <a-card title="添加员工"/>
            <a-form
                    id="add"
                    :form="add"
                    class="add"
                    @submit="addEmployee"
                    style="margin-top: 20px">
                <a-row justify="space-around" align="middle">
                    <a-col :span="5">
                        <a-form-item class="add-e">
                            <a-input
                                    v-decorator="['name',{ rules: [{ required: true, message: 'name is needed' }] }]"
                                    placeholder="name">
                                <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                            </a-input>
                        </a-form-item>
                    </a-col>
                    <a-col :span="5">
                        <a-form-item  class="add-e">
                            <a-select
                                    v-decorator="['dept',{rules: [{ required: true, message: 'Please select a department!' }]}]"
                                    placeholder="Please select a department!"
                            >
                                <a-select-option v-for="i in depts" :value="i" v-bind:key="i">
                                    {{i}}
                                </a-select-option>
                            </a-select>
                        </a-form-item>
                    </a-col>
                    <a-col :span="5">
                        <a-form-item  class="add-e">
                            <a-input
                                    v-decorator="['level',{ rules: [{ required: true, message: 'Level is needed' }] }]"
                                    placeholder="Level">
                                <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                            </a-input>
                        </a-form-item>
                    </a-col>
                    <a-col :span="5">
                        <a-form-item  class="add-e">
                            <a-input
                                    v-decorator="['salary',{ rules: [{ required: true, message: 'Salary is needed' }] }]"
                                    placeholder="Salary">
                                <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                            </a-input>
                        </a-form-item>
                    </a-col>
                    <a-col :span="4">
                        <a-form-item  class="add-e">
                            <a-button type="primary" class="add-b" html-type="submit">Add</a-button>
                        </a-form-item>
                    </a-col>
                </a-row>
            </a-form>
        </div>
        <a-card title="搜索"/>
        <a-form
                id="login_form"
                :form="form"
                class="login-form"
                @submit="handleSubmit"
                style="margin-top: 20px"
        >
            <a-row>
                <a-col :span="20">
                    <a-form-item>
                        <a-input
                                v-decorator="[
          'ID',
          { rules: [{ required: true, message: 'Please input the ID you want to search!' }] }
        ]"
                                placeholder="ID"
                        >
                            <a-icon
                                    slot="prefix"
                                    type="user"
                                    style="color: rgba(0,0,0,.25)"
                            />
                        </a-input>
                    </a-form-item>
                </a-col>
                <a-col :span="4">
                    <a-form-item>
                        <a-button
                                type="primary"
                                html-type="submit"
                                class="login-form-button"
                        >
                            Search
                        </a-button>
                    </a-form-item>
                </a-col>
            </a-row>
        </a-form>
        <div v-if="status">
            <a-row>
                <a-col :span="4">姓名: {{name}}</a-col>
                <a-col :span="4">部门: {{dept_name}}</a-col>
                <a-col :span="4">薪水: {{salary}} 元/月</a-col>
                <a-col :span="4">等级: {{level}}</a-col>
                <a-col :span="4">是否离职: {{state?"否":"是"}}</a-col>
            </a-row>
            <div v-if="ulevel > 7">
                <a-row>
                    <a-form id="salary" :form="changesalary" class="change-salary" @submit="changeSalary"
                            style="margin-top: 20px">
                        <a-col :span="8">
                            <a-form-item>
                                <a-input
                                        v-decorator="['salary',{ rules: [{ required: true, message: 'Salary is needed' }] }]"
                                        placeholder="Salary">
                                    <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                                </a-input>
                            </a-form-item>
                        </a-col>
                        <a-col :span="4">
                            <a-form-item>
                                <a-button type="primary" html-type="submit" class="login-form-button">Commit</a-button>
                            </a-form-item>
                        </a-col>
                    </a-form>
                    <a-form
                            id="level"
                            :form="changelevel"
                            class="change-level" style="margin-top: 20px"
                            @submit="changeLevel">
                        <a-col :span="8">
                            <a-form-item>
                                <a-input
                                        v-decorator="['level',{ rules: [{ required: true, message: 'Level is needed' }] }]"
                                        placeholder="Level">
                                    <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                                </a-input>
                            </a-form-item>
                        </a-col>
                        <a-col :span="4">
                            <a-form-item>
                                <a-button type="primary" class="login-form-button" html-type="submit">Commit
                                </a-button>
                            </a-form-item>
                        </a-col>
                    </a-form>
                </a-row>

                <a-row>
                    <a-form id="salary" :form="changedepartment" class="change-salary" @submit="changeDepartment"
                            style="margin-top: 20px">
                        <a-col :span="8">
                            <a-form-item>
                                <a-select
                                        v-decorator="['dept',{rules: [{ required: true, message: 'Please select new Department!' }]}]"
                                        placeholder="Please select new Department"
                                        labelInValue :defaultValue="{ key: this.dept_name }"
                                >
                                    <a-select-option v-for="i in depts" :value="i" v-bind:key="i">
                                        {{i}}
                                    </a-select-option>
                                </a-select>
                            </a-form-item>
                        </a-col>
                        <a-col :span="4">
                            <a-form-item>
                                <a-button type="primary" html-type="submit" class="login-form-button">Commit</a-button>
                            </a-form-item>
                        </a-col>
                    </a-form>
                    <a-form
                            id="mana"
                            :form="manager"
                            class="mana" style="margin-top: 20px"
                            @submit="setManager"
                            v-if="level===10">
                        <a-col :span="8">
                            <a-form-item>
                                <a-button type="primary" class="login-form-button" html-type="submit">设为主管</a-button>
                            </a-form-item>
                        </a-col>
                    </a-form>
                    <a-form
                            id="fire"
                            :form="manager"
                            class="mana" style="margin-top: 20px"
                            @submit="fire">
                        <a-col :span="8">
                            <a-form-item>
                                <a-button type="primary" class="login-form-button" html-type="submit">Fire</a-button>
                            </a-form-item>
                        </a-col>
                    </a-form>
                </a-row>
            </div>
        </div>

    </div>
</template>

<script>
    import ACol from "ant-design-vue/es/grid/Col";

    export default {
        name: "EmployeeSetting",
        components: {ACol},
        data() {
            return {
                status: false,
                id: 0,
                name: "",
                dept_name: "",
                salary: 0.0,
                state: true,
                level: 0,
                depts: []
            }
        },
        computed: {
            url() {
                return this.$store.state.url
            },
            ulevel() {
                return this.$store.state.level
            },
        },
        beforeCreate() {
            this.form = this.$form.createForm(this);
            this.changesalary = this.$form.createForm(this);
            this.changelevel = this.$form.createForm(this);
            this.changedepartment = this.$form.createForm(this);
            this.manager = this.$form.createForm(this);
            this.add = this.$form.createForm(this);
        },
        beforeMount() {
            this.axios.get(this.url + "/api/get_department")
                .then((resp) => {
                    if (resp.data.status) {
                        this.depts = resp.data.data;
                    }
                })
        },
        methods: {
            handleSubmit(e) {
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/get_one_employee", {
                            'id': values.ID,
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.status = true;
                                let i;
                                for (i in resp.data.data) {
                                    this[i] = resp.data.data[i]
                                }
                            } else {
                                this.$notification.error({
                                    message: '查找失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            changeSalary(e) {
                e.preventDefault();
                this.changesalary.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/change_employee_salary", {
                            'id': this.id,
                            'salary': values.salary
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.salary = values.salary;
                            } else {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            changeLevel(e) {
                e.preventDefault();
                this.changelevel.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/change_employee_level", {
                            'id': this.id,
                            'level': values.level
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.level = values.level;
                            } else {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            changeDepartment(e) {
                e.preventDefault();
                this.changedepartment.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/change_employee_dept", {
                            'id': this.id,
                            'dept_name': values.dept
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.dept_name = values.dept;
                            } else {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            setManager(e) {
                e.preventDefault();
                this.manager.validateFields((err, values) => {
                    values
                    if (!err) {
                        this.axios.post(this.url + "/api/add_dept_manager", {
                            'id': this.id,
                            'dept_name': this.dept_name
                        }).then((resp) => {
                            if (!resp.data.status) {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            fire(e) {
                e.preventDefault();
                this.manager.validateFields((err, values) => {
                    values
                    if (!err) {
                        this.axios.post(this.url + "/api/fire_employee", {
                            'id': this.id,
                        }).then((resp) => {
                            if (resp.data.status){
                                this.state = 0;
                                alert("成功")
                            }else {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            },
            addEmployee(e) {
                e.preventDefault();
                this.add.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/add_employee", {
                            'dept_name': values.dept,
                            'name': values.name,
                            'level': values.level,
                            'salary': values.salary
                        }).then((resp) => {
                            if (resp.data.status) {
                                alert("成功")
                            } else {
                                this.$notification.error({
                                    message: '修改失败',
                                    description: resp.data.code,
                                });
                            }
                        })
                    }
                });
            }
        }
    }
</script>

<style scoped>
    #login_form .login-form {
        max-width: 300px;
    }

    #login_form .login-form-forgot {
        float: right;
    }

    #login_form .login-form-button {
        width: 95%;
        float: right;
    }

    #add .add-e{
        width: 95%;
        margin: auto;
    }
    .add-b{
        width: 95%;
    }
</style>