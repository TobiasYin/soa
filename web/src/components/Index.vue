<template>
    <a-layout id="components-layout-demo-top-side-2">
        <a-layout-header class="header">
            <div class="logo"/>
            <a-menu
                    theme="dark"
                    mode="horizontal"
                    :defaultSelectedKeys="['2']"
                    :style="{ lineHeight: '64px' }"
            >
                <a-menu-item key="1">nav 1</a-menu-item>
                <a-menu-item key="2">nav 2</a-menu-item>
                <a-menu-item key="3">nav 3</a-menu-item>
            </a-menu>
            <div style="position: absolute; right:3%;top: 0; z-index: 10;color: white"><button style="background: none;border: none;" v-on:click="logout">退出</button></div>
        </a-layout-header>
        <a-layout>
            <a-layout-sider width="200" style="background: #fff">
                <a-menu
                        theme="dark"
                        mode="inline"
                        :defaultSelectedKeys="['1']"
                        :defaultOpenKeys="['sub1']"
                        :style="{ height: '100%', borderRight: 0 }"
                >
                    <a-sub-menu key="sub1">
                        <span slot="title"><a-icon type="user"/>subnav 1</span>
                        <a-menu-item key="1">option1</a-menu-item>
                        <a-menu-item key="2">option2</a-menu-item>
                        <a-menu-item key="3">option3</a-menu-item>
                        <a-menu-item key="4">option4</a-menu-item>
                    </a-sub-menu>
                    <a-sub-menu key="sub2">
                        <span slot="title"><a-icon type="laptop"/>subnav 2</span>
                        <a-menu-item key="5">option5</a-menu-item>
                        <a-menu-item key="6">option6</a-menu-item>
                        <a-menu-item key="7">option7</a-menu-item>
                        <a-menu-item key="8">option8</a-menu-item>
                    </a-sub-menu>
                    <a-sub-menu key="sub3">
                        <span slot="title"><a-icon type="notification"/>subnav 3</span>
                        <a-menu-item key="9">option9</a-menu-item>
                        <a-menu-item key="10">option10</a-menu-item>
                        <a-menu-item key="11">option11</a-menu-item>
                        <a-menu-item key="12">option12</a-menu-item>
                    </a-sub-menu>
                </a-menu>
            </a-layout-sider>
            <a-layout style="padding: 0 24px 24px">
                <a-breadcrumb style="margin: 16px 0">
                    <a-breadcrumb-item>Home</a-breadcrumb-item>
                    <a-breadcrumb-item>List</a-breadcrumb-item>
                    <a-breadcrumb-item>App</a-breadcrumb-item>
                </a-breadcrumb>
                <a-layout-content :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }">
                    <div>
                        <a-card class="content-header">
                            你好, {{this.name}}, 亲爱的{{this.level}}级员工, 新的一天到了, <span
                                v-if="!isCheck">从签到开始新的一天吧!</span><span v-else>又是好好工作的一天</span>
                            <a-button type="primary" class="check-in" @click="checkin" v-if="!isCheck">Check in
                            </a-button>
                        </a-card>
                        <div v-if="level > 7" style="margin-top: 20px">
                            <a-card title="这是今天还没签到的人"/>
                            <UncheckedList/>
                            <tr  v-for="item in unchecked" v-bind:key="item.id">
                                <td>{{item.id}}</td>
                                <td>{{item.name}}</td>
                                <td>{{item.level}}</td>
                                <td>{{item.dept_name}}</td>
                            </tr>
                        </div>
                    </div>
                </a-layout-content>
            </a-layout>
        </a-layout>
    </a-layout>
</template>


<script>
    import UncheckedList from './UncheckedList'
    export default {
        name: "Index",
        data() {
            return {
                collapsed: false,
                isCheck: false,
            }
        },
        components:{
            UncheckedList
        },
        computed: {
            level() {
                return this.$store.state.level
            },
            name() {
                return this.$store.state.name
            },
            url() {
                return this.$store.state.url
            }
        },
        methods: {
            checkin() {
                this.axios.get(this.url + "/api/check_in").then((resp) => {
                    this.isCheck = resp.data.status
                    if (!this.isCheck) {
                        this.$notification.error({
                            message: '签到失败',
                            description: resp.data.status.code,
                        });
                    }
                })
            },
            logout() {
                this.axios.get(this.url + '/api/logout').then((resp)=>{
                    if (resp.data.status){
                        location.reload()
                    }
                })
            }
        },
        beforeMount() {
            this.axios.get(this.url + "/api/is_check_in").then((resp) => {
                this.isCheck = resp.data.status;
            });
            if (this.level > 7) {
                this.axios.post(this.$store.state.url + "/api/get_uncheck_in", {'all': true}).then((resp) => {

                })
            }
        }
    }
</script>

<style scoped>
    #components-layout-demo-top-side-2 .logo {
        width: 120px;
        height: 31px;
        background: rgba(255, 255, 255, .2);
        margin: 16px 28px 16px 0;
        float: left;
    }

    .check-in {
        float: right;
    }

    .content-header {
        background: aliceblue;
        overflow: auto;
        padding: 10px;
        line-height: 32px;
    }
</style>