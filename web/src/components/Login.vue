<template>
    <div id = "login">
        <a-card title="登陆"/>
        <a-form
                id="login_form"
                :form="form"
                class="login-form"
                @submit="handleSubmit"
        >
            <a-form-item>
                <a-input
                        v-decorator="[
          'ID',
          { rules: [{ required: true, message: 'Please input your ID!' }] }
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
            <a-form-item>
                <a-input
                        v-decorator="[
          'password',
          { rules: [{ required: true, message: 'Please input your Password!' }] }
        ]"
                        type="password"
                        placeholder="Password"
                >
                    <a-icon
                            slot="prefix"
                            type="lock"
                            style="color: rgba(0,0,0,.25)"
                    />
                </a-input>
            </a-form-item>
            <a-form-item>
                <a-checkbox
                        v-decorator="[
          'remember',
          {
            valuePropName: 'checked',
            initialValue: true,
          }
        ]"
                >
                    Remember me
                </a-checkbox>
                <a
                        class="login-form-forgot"
                        href=""
                >
                    Forgot password
                </a>
                <a-button
                        type="primary"
                        html-type="submit"
                        class="login-form-button"
                >
                    Log in
                </a-button>
            </a-form-item>
        </a-form>
    </div>
</template>

<script>
    export default {
        name: "Login",
        computed: {
            url() {
                return this.$store.state.url + '/api/login'
            }
        },
        beforeCreate() {
            this.form = this.$form.createForm(this);
        },
        methods: {
            handleSubmit(e) {
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    if (!err) {
                        this.axios.post(this.url, {
                            'user_id': values.ID,
                            'password': values.password,
                            'remember': values.remember
                        }).then((resp) => {
                            let temp = resp.data;
                            if (resp.data.status) {
                                this.$store.commit('login');
                                this.$store.commit('setName', temp.name);
                                this.$store.commit('setUserID', temp.userID);
                                this.$store.commit('setLevel', temp.level);
                            } else {
                                this.$notification.error({
                                    message: '登录失败',
                                    description: temp.code,
                                });
                            }
                        })
                    }
                });
            },
        },
    }
</script>

<style scoped>
    #login {
        text-align: center;
        width: 20%;
        min-width: 100px;
        margin: auto;
        padding: 200px 0;
    }
    #login_form{
        margin-top: 50px;
    }

    #login_form .login-form {
        max-width: 300px;
    }

    #login_form .login-form-forgot {
        float: right;
    }

    #login_form .login-form-button {
        width: 100%;
    }
</style>