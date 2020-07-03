<template>
  <q-table
    :data="doors"
    :columns="[
      { name: 'name', label: 'Name', field: 'name', sortable: true },
      { name: 'ipAddress', label: 'IP', field: 'ipAddress', sortable: true },
      { name: 'lastSeen',
        label: 'Last Seen',
        field: 'lastSeen',
        sortable: true,
        format: (val, row) => this.formatDate(val)
      },
    ]"
    row-key="id"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
    :no-data-label="$t('doors.nodata')"
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

    <!--    <template v-slot:header="props">-->
    <!--      <q-tr :props="props">-->
    <!--        <q-th auto-width />-->
    <!--        <q-th-->
    <!--          v-for="col in props.cols"-->
    <!--          :key="col.name"-->
    <!--          :props="props"-->
    <!--        >-->
    <!--          {{ col.label }}-->
    <!--        </q-th>-->
    <!--        <q-th auto-width>-->
    <!--          {{ $t('edit') }}-->
    <!--        </q-th>-->
    <!--        <q-th auto-width>-->
    <!--          {{ $t('delete') }}-->
    <!--        </q-th>-->
    <!--      </q-tr>-->
    <!--    </template>-->
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import icons from '../../icons';
import formatMixin from '../../mixins/formatMixin';

export default {
  name: 'DoorsList',
  mixins: [formatMixin],
  data() {
    return {
      loading: false,
      filter: '',
      pagination: {
        sortBy: 'lastSeen',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 2 : 12,
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getDoors']),
  },
  mounted() {
    this.loading = true;
    this.getDoors()
      .finally(() => {
        this.loading = false;
      });
  },
  computed: {
    ...mapGetters('adminTools', ['doors']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="stylus" scoped>
  @media (max-width: $breakpoint-xs-max)
    .access-list
      width: 100%;
</style>
