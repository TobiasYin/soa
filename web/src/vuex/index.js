import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        isLogin: false,
        name: '',
        userID: '',
        url: 'http://127.0.0.1:5000',
    },
    mutations: {
        login(state) {
            state.isLogin = true
        },
        logout(state) {
            state.isLogin = false;
            state.username = '';
            state.userID = ''
        },
        setUrl(state, url) {
            state.url = url
        },
        setName(state, username) {
            state.username = username
        },
        setUserID(state, ID) {
            state.userID = ID
        },
    }
});