<template>
    <div>
        <div v-if="ulevel > 7">
            <a-card title="添加项目"/>
            <a-form
                    id="add"
                    :form="add"
                    class="add"
                    @submit="addProject"
                    style="margin-top: 20px">
                <a-row justify="space-around" align="middle">
                    <a-col :span="10">
                        <a-form-item class="add-e">
                            <a-input
                                    v-decorator="['name',{ rules: [{ required: true, message: 'Level is needed' }] }]"
                                    placeholder="Project Name">
                                <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                            </a-input>
                        </a-form-item>
                    </a-col>
                    <a-col :span="4">
                        <a-form-item class="add-e">
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
                                v-decorator="[ 'ID',{ rules: [{ required: true, message: 'Please input the ID you want to search!' }] }]"
                                placeholder="Project ID"
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
                <a-col :span="6">项目名: {{pro_name}}</a-col>
                <a-col :span="6">项目主管：{{leader}}</a-col>
                <a-col :span="6">创建时间: {{create_date}}</a-col>
                <a-col :span="6">是否完成: {{state?"是":"否"}}</a-col>
            </a-row>
            <table class="table">
                <tr v-for="item in people" :key="item" class="content">
                    <td class="cell">
                        {{item.id}}
                    </td>
                    <td class="cell" style="min-width: 300px">
                        {{item.name}}
                    </td>
                    <td class="cell">
                        <a-button v-on:click="deletes(item.id)" style="width: auto">delete</a-button>
                    </td>
                </tr>
            </table>
            <div v-if="ulevel > 7">
                <a-row>
                    <a-form id="salary" :form="addemployee" class="change-salary" @submit="addEmployee"
                            style="margin-top: 20px">
                        <a-col :span="8">
                            <a-form-item>
                                <a-input
                                        v-decorator="['id',{ rules: [{ required: true, message: 'id is needed' }] }]"
                                        placeholder="Employee id">
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
                            :form="changeleader"
                            class="change-level" style="margin-top: 20px"
                            @submit="changeLeader">
                        <a-col :span="8">
                            <a-form-item>
                                <a-input
                                        v-decorator="['leader',{ rules: [{ required: true, message: 'id is needed' }] }]"
                                        placeholder="Leader ID">
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
                <a-form
                        id="finish"
                        :form="manager"
                        class="mana" style="margin-top: 20px"
                        @submit="finish">
                    <a-col :span="8">
                        <a-form-item>
                            <a-button type="primary" class="login-form-button" html-type="submit">Finish</a-button>
                        </a-form-item>
                    </a-col>
                </a-form>
            </div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "ProjectSetting",
        computed: {
            url() {
                return this.$store.state.url
            },
            ulevel() {
                return this.$store.state.level
            },
        },
        data() {
            return {
                pro_name: "",
                pro_id: 0,
                leader: null,
                create_date: 0,
                state: 0,
                status: false,
                people: []
            }
        },
        beforeCreate() {
            this.form = this.$form.createForm(this);
            this.addemployee = this.$form.createForm(this);
            this.changeleader = this.$form.createForm(this);
            this.add = this.$form.createForm(this);
        },
        methods: {
            deletes(v) {
                this.axios.post(this.url + "/api/del_employee_pro", {
                    'pro_id': this.pro_id,
                    'employee_id': v
                }).then((resp) => {
                    if (resp.data.status) {
                        alert("成功");
                        let i = -1;
                        for (let index in this.people) {
                            if (this.people[index]['id'] === v) {
                                i = index;
                                break;
                            }
                        }
                        if (i > -1) {
                            this.people.splice(i, 1);
                        }
                    } else {
                        this.$notification.error({
                            message: '查找失败',
                            description: resp.data.code,
                        });
                    }
                });
            },
            handleSubmit(e) {
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/get_project", {
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
                        });
                        this.axios.post(this.url + "/api/get_pro_employee", {
                            'id': values.ID,
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.status = true;
                                this.people = resp.data.data;
                            } else {
                                this.$notification.error({
                                    message: '查找失败',
                                    description: resp.data.code,
                                });
                            }
                        });
                    }
                });
            },
            addEmployee(e) {
                e.preventDefault();
                this.addemployee.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/add_project_employee", {
                            'pro_id': this.pro_id,
                            'emp_id': values.id
                        }).then((resp) => {
                            if (resp.data.status) {
                                alert("成功!")
                                this.handleSubmit({preventDefault(){},})
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
            changeLeader(e) {
                e.preventDefault();
                this.changeleader.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/add_project_leader", {
                            'pro_id': this.pro_id,
                            'leader': values.leader
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.leader = values.leader;
                                this.handleSubmit({preventDefault(){},})
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
            finish(e) {
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    values
                    if (!err) {
                        this.axios.post(this.url + "/api/set_pro_finish", {
                            'pro_id': this.pro_id,
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.state = 1;
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
            },
            addProject(e) {
                e.preventDefault();
                this.add.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/add_project", {
                            'project_name': values.name,
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
    .table {
        width: 100%;
        text-align: center;
    }

    .title {
        font-weight: bolder;
        font-size: 16px;
    }

    .table, .cell, .title, .content {
        border: 1px solid #d9f0f7;
    }
</style>