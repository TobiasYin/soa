<template>
    <div>
        <a-card title="Log"/>
        <a-row>
            <a-col :span="24">
                <a-select
                        placeholder="Please select a Type of log"
                        @change="getLog"
                        style="width: 100%"
                >
                    <a-select-option value="employee">Employee Log</a-select-option>
                    <a-select-option value="project">Project Log</a-select-option>
                </a-select>
            </a-col>
        </a-row>
        <employee-log v-if="page === 0"/>
        <project-log v-if="page === 1"/>
    </div>
</template>

<script>
    import ProjectLog from "./ProjectLog"
    import EmployeeLog from "./EmployeeLog"
    export default {
        components:{
            ProjectLog,
            EmployeeLog
        },
        name: "Log",
        data(){
            return{
                status:false,
                data:[],
                page:-1
            }
        },
        computed: {
            url() {
                return this.$store.state.url
            }
        },
        methods: {
            getLog(value) {
                if (value === 'employee') {
                    this.page = 0

                }else {
                    this.page = 1
                }
            }
        }
    }
</script>

<style scoped>

</style>