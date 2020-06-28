<template>
  <q-table
    :data="members"
    :columns="[{ name: 'name',
                 label: 'Name', field: (row) => row.name.full,
                 sortable: true,
                 format: (val, row) => `${val} (${row.screenName})` },
               { name: 'email',
                 label: 'Email',
                 field: 'email', },
               { name: 'memberType',
                 label: 'Member Type',
                 field: (row) => row.memberType.name,
                 sortable: true },
               { name: 'groups',
                 label: 'Groups',
                 field: 'groups',
                 sortable: true,
                 format: (val, row) => row.groups.map((val => val.name)).join(', ') },
               { name: 'status',
                 label: 'Status',
                 field: 'state', },
    ]"
    row-key="email"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
  >
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

export default {
  name: 'MembersList',
  components: {},
  mixins: [formatMixin],
  data() {
    return {
      members: [],
      filter: '',
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
  },
  mounted() {
    this.getMembers();
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
