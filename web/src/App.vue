<template>
    <div>
        <div v-if="isLogin">
            hello
        </div>
        <div v-else>
            no
        </div>
    </div>
</template>
<script>
    export default {
        name: 'app',
        data() {
            return {
                collapsed: false,

            }
        },
        computed:{
            isLogin() {
                return this.$store.state.isLogin
            }
        },
        components: {},
        beforeMount() {
            this.axios.get(this.$store.state.url + '/api/islogin')
                .then((resp) => {
                    let temp = resp.data;
                    if (temp.isLogin) {
                        this.$store.commit('login');
                        this.$store.commit('setName', temp.name);
                        this.$store.commit('setUserID', temp.userID);
                    }
                });
        }
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }

    #components-layout-demo-custom-trigger .trigger {
        font-size: 18px;
        line-height: 64px;
        padding: 0 24px;
        cursor: pointer;
        transition: color .3s;
    }

    #components-layout-demo-custom-trigger .trigger:hover {
        color: #1890ff;
    }

    #components-layout-demo-custom-trigger .logo {
        height: 32px;
        background: rgba(255, 255, 255, .2);
        margin: 16px;
    }
</style>
