<template>
    <a-table :dataSource="unchecked" :columns="columns">
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
</template>

<script>
    export default {
        name: "UncheckedList",
        data() {
            return {
                unchecked: [],
                searchText: '',
                searchInput: null,
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
        methods: {
            handleSearch(selectedKeys, confirm) {
                confirm()
                this.searchText = selectedKeys[0]
            },

            handleReset(clearFilters) {
                clearFilters()
                this.searchText = ''
            },
        },
        beforeMount() {
            this.axios.post(this.$store.state.url + "/api/get_uncheck_in", {'all': true}).then((resp) => {
                if (resp.data.status) {
                    this.unchecked = resp.data.data
                }
            })
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