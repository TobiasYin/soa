<template>
    <div>
        <a-table :dataSource="data" :columns="columns">
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
</template>

<script>
    export default {
        name: "EmployeeLog",
        data(){
            return{
                status:false,
                data:[],
                searchText: '',
                searchInput: null,
                columns: [ {
                    title: 'ID',
                    dataIndex: 'id',
                    key: 'id',
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
                    title: 'Operation',
                    dataIndex: 'operation',
                    key: 'operation',
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
                    title: 'Old',
                    dataIndex: 'old',
                    key: 'old',
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
                },{
                    title: 'New',
                    dataIndex: 'new',
                    key: 'new',
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
                    title: 'Time',
                    dataIndex: 'date_time',
                    key: 'date_time',
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
        computed: {
            url() {
                return this.$store.state.url
            }
        },
        beforeMount() {
            this.axios.get(this.url + "/api/get_employee_log",).then((resp) => {
                if (resp.data.status) {
                    this.data = resp.data.data;
                    for(let i in this.data){
                        this.data[i].date_time = this.getTime(this.data[i].date_time)
                    }
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
            getTime(t){
                return new Date(parseInt(t) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ')
            }
        }
    }
</script>

<style scoped>
    .custom-filter-dropdown {
        padding: 8px;
        border-radius: 4px;
        background: #fff;
        box-shadow: 0 2px 8px rgba(0, 0, 0, .15);
    }

    .highlight {
        background-color: rgb(255, 192, 105);
        padding: 0px;
    }
</style>