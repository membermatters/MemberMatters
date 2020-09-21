<template>
  <div
    class="q-pa-md"
  >
    <q-tabs
      v-model="tab"
      dense
      class="text-grey"
      active-color="primary"
      indicator-color="primary"
      align="justify"
    >
      <q-tab
        name="groups"
        label="Groups"
      />
      <q-tab
        name="members"
        label="Members"
      />
    </q-tabs>

    <q-separator />

    <q-tab-panels
      v-model="tab"
      animated
    >
      <q-tab-panel name="members">
        <div class="row flex content-start justify-center">
          <q-table
            :data="memberList"
            :columns="[{ name: 'member',
                         label: $t('member'),
                         field: 'member',
                         sortable: true },
                       { name: 'groups',
                         label: $t('groups'),
                         field: 'groups',
                         sortable: true,
                         format: formatCsvList,
                       }]"
            row-key="key"
            :filter="memberFilter"
            :pagination.sync="groupPagination"
            :dense="$q.screen.lt.md"
            :grid="$q.screen.xs"
            class="table"
            :loading="loading"
          >
            <template v-slot:top-right>
              <q-input
                outlined
                dense
                debounce="300"
                v-model="memberFilter"
                placeholder="Search"
              >
                <template v-slot:append>
                  <q-icon :name="icons.search" />
                </template>
              </q-input>
            </template>
          </q-table>
        </div>
      </q-tab-panel>

      <q-tab-panel name="groups">
        <div class="row flex content-start justify-center">
          <q-table
            :data="groupList"
            :columns="[{ name: 'group', label: $t('group'), field: 'name', sortable: true },
                       { name: 'activeMembers',
                         label: $t('memberGroups.activeMembers'),
                         field: 'activeMembers',
                         sortable: true
                       },
                       { name: 'quorum',
                         label: $t('memberGroups.quorum'),
                         field: 'quorum',
                         sortable: true
                       },
            ]"
            row-key="key"
            :filter="groupFilter"
            :pagination.sync="memberPagination"
            :dense="$q.screen.lt.md"
            :grid="$q.screen.xs"
            :loading="loading"
          >
            <template v-slot:top-right>
              <q-input
                outlined
                dense
                debounce="300"
                v-model="groupFilter"
                placeholder="Search"
              >
                <template v-slot:append>
                  <q-icon :name="icons.search" />
                </template>
              </q-input>
            </template>
          </q-table>
        </div>
      </q-tab-panel>
    </q-tab-panels>

    <refresh-data-dialog v-model="errorLoading" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';
import RefreshDataDialog from './RefreshDataDialog';

export default {
  name: 'MemberGroups',
  components: { RefreshDataDialog },
  mixins: [formatMixin],
  data() {
    return {
      tab: 'groups',
      loading: false,
      errorLoading: false,
      memberFilter: '',
      groupFilter: '',
      memberPagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 3 : 8,
      },
      groupPagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 4 : 8,
      },
    };
  },
  methods: {
    ...mapActions('tools', ['getMemberGroups']),
  },
  mounted() {
    this.loading = true;
    this.getMemberGroups()
      .catch(() => {
        this.errorLoading = true;
      })
      .then(() => {
        this.loading = false;
      });
  },
  computed: {
    ...mapGetters('tools', ['groupList', 'memberList']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
  .table
    max-width: $maxWidthMedium
</style>
