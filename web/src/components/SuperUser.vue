<template>
    <div>
        <a-card title="数据库管理器"/>
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
          'SQL',
          { rules: [{ required: true, message: 'Please input the SQL' }] }
        ]"
                                placeholder="SQL"
                        >
                            <a-icon
                                    slot="prefix"
                                    type="code"
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
                            Commit
                        </a-button>
                    </a-form-item>
                </a-col>
            </a-row>
        </a-form>
        <table class="table">
            <tr class="title">
                <td v-for="k in des" class="cell">
                    {{k}}
                </td>
            </tr>
            <tr v-for="item in data" :key="item" class="content">
                <td v-for="k in item" class="cell">
                    {{k}}
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
    export default {
        name: "SuperUser",
        data() {
            return {
                data: [],
                status: false,
                des:[]
            }
        },
        computed: {
            url() {
                return this.$store.state.url
            },
        },
        beforeCreate() {
            this.form = this.$form.createForm(this);
        },
        methods: {
            handleSubmit(e) {
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url + "/api/super_user", {
                            'sql': values.SQL,
                        }).then((resp) => {
                            if (resp.data.status) {
                                this.status = true;
                                this.data = resp.data.data;
                                this.des = resp.data.des;
                                console.log(this.data)
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

    .table{
        width: 100%;
        text-align: center;
    }

    .title{
        font-weight: bolder;
        font-size: 16px;
    }

    .table, .cell, .title, .content{
        border: 1px solid #d9f0f7;
    }
</style>