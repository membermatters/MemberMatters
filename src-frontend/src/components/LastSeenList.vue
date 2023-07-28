<template>
  <div>
    <q-table
      :rows="humanLastSeen"
      :columns="[
        { name: 'user', label: 'User', field: 'user', sortable: true },
        { name: 'lastSeen', label: 'Last Seen', field: 'date', sortable: true },
      ]"
      row-key="id"
      :filter="filter"
      v-model:pagination="pagination"
      :loading="loading"
    >
      <template v-slot:top-right>
        <q-input
          v-model="filter"
          outlined
          dense
          debounce="300"
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
import icons from '../icons';
import RefreshDataDialog from '@components/RefreshDataDialog.vue';
import formatMixin from 'src/mixins/formatMixin';

export default {
  name: 'LastSeenList',
  components: { RefreshDataDialog },
  mixins: [formatMixin],
  data() {
    return {
      filter: '',
      loading: false,
      errorLoading: false,
      updateInterval: null,
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 5 : 10,
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
  unmounted() {
    clearInterval(this.updateInterval);
  },
  computed: {
    ...mapGetters('tools', ['lastSeen']),
    icons() {
      return icons;
    },
    humanLastSeen() {
      return this.lastSeen.map((value) => {
        return {
          id: value.id,
          user: value.user,
          date: this.formatDateSimple(value.date),
          never: value.never,
        };
      });
    },
  },
};
</script>

<style lang="sass" scoped>
@media (max-width: $breakpoint-xs-max)
  .access-list
    width: 100%
</style>
