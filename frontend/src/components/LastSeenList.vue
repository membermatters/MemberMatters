<template>
  <div class="q-pl-lg q-pa-md">
    <q-table
      :data="humanLastSeen"
      :columns="[{ name: 'user', label: 'User', field: 'user', sortable: true },
                 { name: 'lastSeen', label: 'Last Seen', field: 'date', sortable: true },]"
      row-key="user"
      :filter="filter"
      :pagination.sync="pagination"
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
    </q-table>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import Moment from 'moment';
import icons from '../icons';

export default {
  name: 'LastSeenList',
  data() {
    return {
      filter: '',
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: 10,
      },
    };
  },
  methods: {
    ...mapActions('tools', ['getLastSeen']),
  },
  mounted() {
    this.getLastSeen();
    setInterval(() => {
      this.getLastSeen();
    }, 30000);
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
