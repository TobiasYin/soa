<template>
    <div>
        <a-card :title="dept"/>
        <a-row>
            <a-col :span="24">
                <a-select
                        placeholder="Please select new Department"
                        @change="getEmployees"
                        style="width: 100%"
                >
                    <a-select-option v-for="i in depts" :value="i" v-bind:key="i">
                        {{i}}
                    </a-select-option>
                </a-select>
            </a-col>
        </a-row>
        <div v-if="status">
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
    </div>
</template>

<script>
    import ACol from "ant-design-vue/es/grid/Col";
    import ARow from "ant-design-vue/es/grid/Row";

    export default {
        name: "Deparment",
        components: {ARow, ACol},
        data() {
            return {
                depts: [],
                searchText: '',
                searchInput: null,
                status: false,
                data: [],
                dept:"选择部门",
                columns: [{
                    title: 'Name',
                    dataIndex: 'name',
                    key: 'name',
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
                }, {
                    title: '部门',
                    dataIndex: 'dept_name',
                    key: 'dept_name',
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
                    title: 'Level',
                    dataIndex: 'level',
                    key: 'level',
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
            },
            ulevel() {
                return this.$store.state.level
            },
        },
        beforeCreate() {
            this.form = this.$form.createForm(this);
        },
        beforeMount() {
            this.axios.get(this.url + "/api/get_department")
                .then((resp) => {
                    if (resp.data.status) {
                        this.depts = resp.data.data;
                    }
                })
        },
        methods: {
            getEmployees(value) {
                this.axios.post(this.url + "/api/get_employee", {
                    'all': false,
                    'dept_name': value,
                    'fired': false
                }).then((resp) => {
                    if (resp.data.status) {
                        this.dept = value;
                        this.data = resp.data.data;
                        this.status = true;
                        if (this.data.length === 0)  {
                            alert("此部门暂时没有员工")
                        }
                    } else {
                        this.$notification.error({
                            message: '失败',
                            description: resp.data.code,
                        });
                    }
                })
            },
            handleSearch(selectedKeys, confirm) {
                confirm();
                this.searchText = selectedKeys[0]
            },

            handleReset(clearFilters) {
                clearFilters();
                this.searchText = ''
            },
        }
    }
</script>

<style scoped>

</style>