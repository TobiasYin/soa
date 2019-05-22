import Vue from "vue";
import App from "./App";
import Vuex from 'vuex'
import axios from 'axios'
import VueAxios from 'vue-axios'
import store from './vuex'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'

Vue.config.productionTip = false
Vue.use(Vuex)
Vue.use(VueAxios, axios);
Vue.use(Antd)


new Vue({
    render: h => h(App),
    store
}).$mount('#app')
