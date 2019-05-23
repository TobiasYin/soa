<template>
    <div id = "app">
        <div v-if="isLogin">
            <Index/>
        </div>
        <div v-else>
            <Login/>
        </div>
    </div>
</template>
<script>
    import Login from './components/Login'
    import Index from './components/Index'
    export default {
        name: 'app',
        data() {
            return {
            }
        },
        computed:{
            isLogin() {
                return this.$store.state.isLogin
            }
        },
        components: {
            Index,
            Login
        },
        beforeMount() {
            this.axios.defaults.xsrfCookieName = 'session';
            this.axios.defaults.timeout = 2500;
            this.axios.defaults.headers = {"X-Requested-With": "XMLHttpRequest"};
            this.axios.defaults.withCredentials = true;
            this.axios.get(this.$store.state.url + '/api/islogin')
                .then((resp) => {
                    let temp = resp.data;
                    if (temp.status) {
                        this.$store.commit('login');
                        this.$store.commit('setName', temp.name);
                        this.$store.commit('setUserID', temp.userID);
                        this.$store.commit('setLevel', temp.level)
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
        color: #2c3e50;
    }
</style>
