<template>
  <q-table
    :data="displayMemberList"
    :columns="columns"
    row-key="email"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
  >
    <template v-slot:top-left>
      <div class="row flex items-start">
        <q-btn
          class="q-mr-sm"
          color="primary"
          :icon="icons.export"
          :label="$t('adminTools.exportCsv')"
          @click="exportCsv"
        />
        <q-btn
          color="primary"
          :icon="icons.email"
          :label="$t('adminTools.emailAddresses')"
          @click="exportEmails"
        />
        <q-option-group
          v-model="memberState"
          inline
          class="q-mb-md"
          :options="[
            { label: $t('adminTools.all'), value: 'All' },
            { label: $t('adminTools.active'), value: 'Active' },
            { label: $t('adminTools.inactive'), value: 'Inactive' },
            { label: $t('adminTools.new'), value: 'New' },
          ]"
        />
      </div>
    </template>
    <template v-slot:top-right>
      <q-input
        outlined
        dense
        debounce="300"
        v-model="filter"
        placeholder="Search"
      >
        <template v-slot:append>
          <q-icon :name="icons.search" />
        </template>
      </q-input>
    </template>

    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th auto-width />
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr
        :props="props"
        @click="props.expand = !props.expand"
      >
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            @click.stop="props.expand = !props.expand"
            :icon="props.expand ? icons.down : icons.up"
          />
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.value }}
        </q-td>
      </q-tr>
      <q-tr
        v-show="props.expand"
        :props="props"
      >
        <q-td colspan="100%">
          Hello
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import icons from '@icons';
import formatMixin from '@mixins/formatMixin';
import { exportFile } from 'quasar';
import stringify from 'csv-stringify';

export default {
  name: 'MembersList',
  components: {},
  mixins: [formatMixin],
  data() {
    return {
      members: [],
      filter: '',
      memberState: 'Active',
      loading: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 2 : 12,
      },
    };
  },
  methods: {
    getMembers() {
      this.loading = true;
      this.$axios.get('/api/admin/members/')
        .then((response) => {
          this.members = response.data;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    exportCsv() {
      stringify(this.displayMemberList, {
        columns: ['name.full', 'email', 'state'],
      }, (err, output) => {
        const status = exportFile(
          'member-export.csv',
          output,
          'text/csv',
        );

        if (status !== true) {
          this.$q.notify({
            message: 'Browser denied file download...',
            color: 'negative',
            icon: 'warning',
          });
        }
      });
    },
    exportEmails() {
      this.$q.dialog({
        dark: true,
        title: `${this.displayMemberList.length} Email Addresses`,
        message: this.memberEmails,
      });
    },
  },
  mounted() {
    this.getMembers();
  },
  computed: {
    displayMemberList() {
      if (this.memberState === 'All') return this.members;
      return this.members.filter((member) => member.state === this.memberState);
    },
    memberEmails() {
      return this.displayMemberList.map((member) => member.email).join(',');
    },
    icons() {
      return icons;
    },
    columns() {
      return [{
        name: 'name',
        label: 'Name',
        field: (row) => row.name.full,
        sortable: true,
        format: (val, row) => `${val} (${row.screenName})`,
      },
      {
        name: 'email',
        label: 'Email',
        field: 'email',
        sortable: true,
      },
      {
        name: 'memberType',
        label: 'Member Type',
        field: (row) => row.memberType.name,
        sortable: true,
      },
      {
        name: 'groups',
        label: 'Groups',
        field: 'groups',
        sortable: true,
        format: (val, row) => row.groups.map(((group) => group.name)).join(', '),
      },
      {
        name: 'status',
        label: 'Status',
        field: 'state',
        sortable: true,
      },
      ];
    },
  },
};
</script>
