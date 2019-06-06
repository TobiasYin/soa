<template>
    <a-layout id="components-layout-demo-top-side-2">
        <a-layout-header class="header">
            <div class="logo"/>
            <div style="color: white;font-size:30px">欢迎使用企业管理系统</div>
            <div style="position: absolute; right:3%;top: 0; z-index: 10;color: white">
                <button style="background: none;border: none;" v-on:click="logout">退出</button>
            </div>
        </a-layout-header>
        <a-layout>
            <a-layout-sider width="200" style="background: #fff"
            >
                <a-menu
                        theme="dark"
                        mode="inline"
                        :defaultSelectedKeys="['1']"
                        :style="{ height: '100%', borderRight: 0 }"
                        @select="select"
                >
                    <a-menu-item key="1">
                        <a-icon type="desktop"/>
                        <span v-if="collapsed">总览</span>
                    </a-menu-item>
                    <a-menu-item key="2">
                        <a-icon type="user"/>
                        <span v-if="collapsed">员工</span>
                    </a-menu-item>
                    <a-menu-item key="3">
                        <a-icon type="cluster" />
                        <span v-if="collapsed">部门</span>
                    </a-menu-item>
                    <a-menu-item key="4">
                        <a-icon type="team"/>
                        <span v-if="collapsed">项目</span>
                    </a-menu-item>
                    <a-menu-item key="5">
                        <a-icon type="solution" />
                        <span v-if="collapsed">Log</span>
                    </a-menu-item>
                    <a-menu-item key="6" v-if="level > 7">
                        <a-icon type="code"/>
                        <span v-if="collapsed">数据库管理器</span>
                    </a-menu-item>
                </a-menu>
            </a-layout-sider>
            <a-layout style="padding: 0 24px 24px;margin-top: 20px;min-height: 700px">
                <a-layout-content :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }">
                    <div v-if="selected==='1'">
                        <a-card class="content-header">
                            你好, {{this.name}}, 亲爱的{{this.level}}级员工, 新的一天到了, <span
                                v-if="!isCheck">从签到开始新的一天吧!</span><span v-else>又是好好工作的一天</span>
                            <a-button type="primary" class="check-in" @click="checkin" v-if="!isCheck">Check in
                            </a-button>
                        </a-card>
                        <div v-if="level > 7" style="margin-top: 20px">
                            <a-card title="这是今天还没签到的人"/>
                            <UncheckedList/>
                        </div>
                    </div>
                    <employee-setting v-if="selected === '2'"/>
                    <department v-if="selected === '3'"/>
                    <project v-if="selected === '4'"/>
                    <log v-if="selected === '5'"/>
                    <super-user v-if="selected === '6'"/>
                </a-layout-content>
            </a-layout>
        </a-layout>
    </a-layout>
</template>


<script>
    import UncheckedList from './UncheckedList'
    import EmployeeSetting from './EmployeeSetting'
    import Department from './Department'
    import Log from './Log'
    import SuperUser from './SuperUser'
    import Project from './Project'
    export default {
        name: "Index",
        data() {
            return {
                collapsed: true,
                isCheck: false,
                selected: '1'
            }
        },
        components: {
            UncheckedList,
            EmployeeSetting,
            Department,
            Log,
            SuperUser,
            Project
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
                    this.isCheck = resp.data.status;
                    if (!this.isCheck) {
                        this.$notification.error({
                            message: '签到失败',
                            description: resp.data.status.code,
                        });
                    }
                })
            },
            logout() {
                this.axios.get(this.url + '/api/logout').then((resp) => {
                    if (resp.data.status) {
                        location.reload()
                    }
                })
            },
            select(item) {
                this.selected = item.key
            }

        },
        beforeMount() {
            this.axios.get(this.url + "/api/is_check_in").then((resp) => {
                this.isCheck = resp.data.status;
            });
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