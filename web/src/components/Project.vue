<template>
    <div>
        <div>
            <a-radio-group defaultValue="all" buttonStyle="solid" @change="change">
                <a-radio-button value="all">所有</a-radio-button>
                <a-radio-button value="det">管理</a-radio-button>
            </a-radio-group>
        </div>
        <div v-if="!more">
            <a-card title="项目"/>
            <a-table :dataSource="data" :columns="columns">
                <a slot="name" slot-scope="text" href="javascript:;">{{text}}</a>
                <div slot="filterDropdown" slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
                     class='custom-filter-dropdown'>
                    <a-input
                            v-ant-ref="c => searchInput = c"
                            :placeholder="`Search ${column.dataIndex}`"
                            :value="selectedKeys[0]"
                            @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
                            @pressEnter="() => handleSearch(selectedKeys, confirm)"
                            style="width: 188px; margin-bottom: 8px; display: block;"
                    />
                    <a-button
                            type='primary'
                            @click="() => handleSearch(selectedKeys, confirm)"
                            icon="search"
                            size="small"
                            style="width: 90px; margin-right: 8px"
                    >Search
                    </a-button>
                    <a-button
                            @click="() => handleReset(clearFilters)"
                            size="small"
                            style="width: 90px"
                    >Reset
                    </a-button>
                </div>
                <a-icon slot="filterIcon" slot-scope="filtered" type='search'
                        :style="{ color: filtered ? '#108ee9' : undefined }"/>
                <template slot="customRender" slot-scope="text">
      <span v-if="searchText">
        <template
                v-for="(fragment, i) in text.toString().split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))">
          <mark v-if="fragment.toLowerCase() === searchText.toLowerCase()" :key="i"
                class="highlight">{{fragment}}</mark>
          <template v-else>{{fragment}}</template>
        </template>
      </span>
                    <template v-else>{{text}}</template>
                </template>
            </a-table>
        </div>
        <div v-else>
            <project-setting/>
        </div>
    </div>
</template>

<script>
    import ProjectSetting from "./ProjectSetting"
    export default {
        name: "Project",
        components:{
            ProjectSetting
        },
        computed: {
            url() {
                return this.$store.state.url
            }
        },
        data(){
            return{
                more:false,
                status:false,
                searchText: '',
                searchInput: null,
                data:[],
                columns: [ {
                    title: 'Project ID',
                    dataIndex: 'pro_id',
                    key: 'pro_id',
                    scopedSlots: {
                        filterDropdown: 'filterDropdown',
                        filterIcon: 'filterIcon',
                        customRender: 'customRender',
                    },
                    onFilter: (value, record) => record.age.toLowerCase().includes(value.toLowerCase()),
                    onFilterDropdownVisibleChange: (visible) => {
                        if (visible) {
                            setTimeout(() => {
                                this.searchInput.focus()
                            })
                        }
                    },
                },{
                    title: 'Project Name',
                    dataIndex: 'pro_name',
                    key: 'pro_name',
                    scopedSlots: {
                        filterDropdown: 'filterDropdown',
                        filterIcon: 'filterIcon',
                        customRender: 'customRender',
                    },
                    onFilter: (value, record) => record.name.toLowerCase().includes(value.toLowerCase()),
                    onFilterDropdownVisibleChange: (visible) => {
                        if (visible) {
                            setTimeout(() => {
                                this.searchInput.focus()
                            }, 0)
                        }
                    },
                }, {
                    title: 'Leader',
                    dataIndex: 'leader',
                    key: 'leader',
                    scopedSlots: {
                        filterDropdown: 'filterDropdown',
                        filterIcon: 'filterIcon',
                        customRender: 'customRender',
                    },
                    onFilter: (value, record) => record.address.toLowerCase().includes(value.toLowerCase()),
                    onFilterDropdownVisibleChange: (visible) => {
                        if (visible) {
                            setTimeout(() => {
                                this.searchInput.focus()
                            })
                        }
                    },
                }, {
                    title: 'Create Date',
                    dataIndex: 'create_date',
                    key: 'create_date',
                    scopedSlots: {
                        filterDropdown: 'filterDropdown',
                        filterIcon: 'filterIcon',
                        customRender: 'customRender',
                    },
                    onFilter: (value, record) => record.address.toLowerCase().includes(value.toLowerCase()),
                    onFilterDropdownVisibleChange: (visible) => {
                        if (visible) {
                            setTimeout(() => {
                                this.searchInput.focus()
                            })
                        }
                    },
                }],
            }
        },
        beforeMount(){
            this.axios.post(this.url + "/api/find_project",{finished:false}).then((resp) => {
                if (resp.data.status) {
                    this.data = resp.data.data;
                    this.status = true;
                } else {
                    this.$notification.error({
                        message: '失败',
                        description: resp.data.code,
                    });
                }
            })
        },
        methods: {
            handleSearch(selectedKeys, confirm) {
                confirm();
                this.searchText = selectedKeys[0]
            },

            handleReset(clearFilters) {
                clearFilters();
                this.searchText = ''
            },
            change(value){
                this.more = value.target.value !== 'all';
            }
        }
    }
</script>

<style scoped>

</style>