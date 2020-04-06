<template>
  <div>
    <q-table
      :data="humanLastSeen"
      :columns="[{ name: 'user', label: 'User', field: 'user', sortable: true },
                 { name: 'lastSeen', label: 'Last Seen', field: 'date', sortable: true },]"
      row-key="user"
      :filter="filter"
      :pagination.sync="pagination"
      :loading="loading"
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
    </q-table>

    <refresh-data-dialog v-model="errorLoading" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import Moment from 'moment';
import icons from '../icons';
import RefreshDataDialog from './RefreshDataDialog';

export default {
  name: 'LastSeenList',
  components: { RefreshDataDialog },
  data() {
    return {
      filter: '',
      loading: false,
      errorLoading: false,
      updateInterval: null,
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 8 : 12,
      },
    };
  },
  methods: {
    ...mapActions('tools', ['getLastSeen']),
  },
  mounted() {
    this.loading = true;
    this.getLastSeen()
      .catch(() => {
        this.errorLoading = true;
      })
      .finally(() => {
        this.loading = false;
      });
    this.updateInterval = setInterval(() => {
      this.getLastSeen();
    }, 30000);
  },
  destroyed() {
    clearInterval(this.updateInterval);
  },
  computed: {
    ...mapGetters('tools', ['lastSeen']),
    icons() {
      return icons;
    },
    humanLastSeen() {
      return this.lastSeen.map((value) => {
        const humanReadable = Moment.utc(value.date).local().format('Do MMM YYYY, h:mm a');
        return { user: value.user, date: humanReadable, never: value.never };
      });
    },
  },
};
</script>

<style lang="stylus" scoped>
  @media (max-width: $breakpoint-xs-max)
    .access-list
      width: 100%;
</style>
