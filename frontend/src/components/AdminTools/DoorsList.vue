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

    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.label }}
        </q-th>
        <q-th auto-width>
          Manage
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr
        :props="props"
      >
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.value }}
        </q-td>
        <q-td auto-width>
          <q-btn
            :ref="`${props.row.id}-unlock`"
            class="q-mr-sm"
            size="sm"
            color="accent"
            @click="unlockDoor(props.row.id)"
          >
            <q-icon :name="icons.unlock" />
            <q-tooltip>
              {{ $t('button.unlockDoor') }}
            </q-tooltip>
          </q-btn>

          <q-btn
            :ref="`${props.row.id}-reboot`"
            class="q-mr-sm"
            size="sm"
            color="accent"
            @click="rebootDoor(props.row.id)"
          >
            <q-icon :name="icons.reboot" />
            <q-tooltip>
              {{ $t('button.rebootDevice') }}
            </q-tooltip>
          </q-btn>

          <q-btn
            size="sm"
            color="accent"
            :to="{name: 'manageDoor', params: {doorId: String(props.row.id)}}"
          >
            <q-icon :name="icons.settings" />
            <q-tooltip>
              {{ $t('button.manage') }}
            </q-tooltip>
          </q-btn>
        </q-td>
      </q-tr>
    </template>
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
    rebootDoor(doorId) {
      this.$refs[`${doorId}-reboot`].loading = true;
      this.$axios.post(`/api/access/doors/${doorId}/reboot/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        }).finally(() => {
          this.$refs[`${doorId}-reboot`].loading = false;
        });
    },
    unlockDoor(doorId) {
      this.$refs[`${doorId}-unlock`].loading = true;
      this.$axios.post(`/api/access/doors/${doorId}/unlock/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        }).finally(() => {
          this.$refs[`${doorId}-unlock`].loading = false;
        });
    },
  },
  beforeMount() {
    this.getDoors()
      .then(() => {
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
