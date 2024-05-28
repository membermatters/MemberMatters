<template>
  <q-table
    :rows="tableData"
    :columns="columnI18n"
    row-key="id"
    :filter="filter"
    v-model:pagination="pagination"
    :grid="$q.screen.xs"
    :no-data-label="$t(`${deviceChoice}.nodata`)"
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

    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          {{ col.label }}
        </q-th>
        <q-th auto-width>
          {{ $t('button.actions') }}
        </q-th>
      </q-tr>
    </template>

    <template v-slot:item="props">
      <div
        class="q-pa-sm col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
      >
        <q-card class="q-py-sm">
          <q-list dense>
            <q-item
              v-for="col in props.cols.filter(
                (col) => col.name !== 'desc' && col.name !== 'id'
              )"
              :key="col.name"
            >
              <q-item-section>
                <q-item-label>{{ col.label }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label caption>
                  <div
                    class="text-warning"
                    v-if="col.name === 'lastSeen' && props.row.offline"
                  >
                    {{ col.value }}
                  </div>
                  <div v-else>
                    {{ col.value }}
                  </div>
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item class="q-mt-sm row justify-center">
              <template v-if="deviceChoice === 'doors'">
                <q-btn
                  :loading="deviceLoading[props.row.id]?.bump"
                  :disabled="props.row.offline"
                  class="q-mr-sm"
                  size="sm"
                  color="accent"
                  @click.stop="bumpDoor(props.row.id)"
                >
                  <q-icon :name="icons.bump" />
                  <q-tooltip>
                    {{ $t('doors.bump') }}
                  </q-tooltip>
                </q-btn>
              </template>

              <q-btn
                size="sm"
                color="accent"
                @click.stop="manageDevice(props.row.id)"
              >
                <q-icon :name="icons.settings" />
                <q-tooltip>
                  {{ $t('button.manage') }}
                </q-tooltip>
              </q-btn>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
          <div
            class="text-warning"
            v-if="col.name === 'lastSeen' && props.row.offline"
          >
            {{ col.value }}
          </div>
          <div v-else>
            {{ col.value }}
          </div>
        </q-td>
        <q-td auto-width>
          <template v-if="deviceChoice === 'doors'">
            <q-btn
              :loading="deviceLoading[props.row.id]?.bump"
              class="q-mr-sm"
              size="sm"
              color="accent"
              @click.stop="bumpDoor(props.row.id)"
              :disabled="props.row.offline"
            >
              <q-icon :name="icons.bump" />
              <q-tooltip v-if="props.row.offline">
                {{ $t('device.offlineStatus') }}
              </q-tooltip>
              <q-tooltip v-else>
                {{ $t('doors.bump') }}
              </q-tooltip>
            </q-btn>
          </template>

          <q-btn
            size="sm"
            color="accent"
            @click.stop="manageDevice(props.row.id)"
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
import icons from '../../icons';
import formatMixin from 'src/mixins/formatMixin';
import { mapGetters } from 'vuex';

export default {
  props: {
    deviceChoice: {
      type: String,
    },
    tableData: {
      type: Array,
    },
  },
  name: 'DevicesList',
  mixins: [formatMixin],
  data() {
    return {
      loading: false,
      filter: '',
      pagination: {
        sortBy: 'lastSeen',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 3 : 10,
      },
      deviceLoading: {},
    };
  },
  watch: {
    tableData: {
      handler(newRows) {
        newRows.forEach((row) => {
          this.deviceLoading[row.id] = {
            reboot: false,
            bump: false,
          };
        });
      },
      deep: true,
    },
  },
  computed: {
    ...mapGetters('config', ['siteLocaleCurrency']),
    columnI18n() {
      let columns = [];
      if (this.deviceChoice === 'doors') {
        columns = [
          {
            name: 'id',
            label: this.$t('tableHeading.id'),
            field: 'id',
            sortable: true,
          },
          {
            name: 'name',
            label: this.$t('form.name'),
            field: 'name',
            sortable: true,
          },
          {
            name: 'lastSeen',
            label: this.$t('access.lastSeen'),
            field: 'lastSeen',
            sortable: true,
            format: (val) => this.formatDate(val),
          },
          {
            name: 'totalSwipes',
            label: this.$t('access.totalSwipes'),
            field: 'totalSwipes',
            sortable: true,
          },
        ];
      } else if (this.deviceChoice === 'interlocks') {
        columns = [
          {
            name: 'id',
            label: this.$t('tableHeading.id'),
            field: 'id',
            sortable: true,
          },
          {
            name: 'name',
            label: this.$t('tableHeading.name'),
            field: 'name',
            sortable: true,
          },
          {
            name: 'lastSeen',
            label: this.$t('access.lastSeen'),
            field: 'lastSeen',
            sortable: true,
            format: (val) => this.formatDate(val),
          },
          {
            name: 'totalTime',
            label: this.$t('access.totalTime'),
            field: 'totalTimeSeconds',
            sortable: true,
            format: (val) => this.humanizeDurationOfSeconds(val),
          },
        ];
      } else if (this.deviceChoice === 'memberbucks-devices') {
        columns = [
          {
            name: 'id',
            label: this.$t('tableHeading.id'),
            field: 'id',
            sortable: true,
          },
          {
            name: 'name',
            label: this.$t('tableHeading.name'),
            field: 'name',
            sortable: true,
          },
          {
            name: 'lastSeen',
            label: this.$t('access.lastSeen'),
            field: 'lastSeen',
            sortable: true,
            format: (val) => this.formatDate(val),
          },
          {
            name: 'totalPurchases',
            label: this.$t('memberbucks-devices.totalPurchases'),
            field: 'totalPurchases',
            sortable: true,
          },
          {
            name: 'totalVolume',
            label: this.$t('memberbucks-devices.totalVolume'),
            field: 'totalVolume',
            sortable: true,
            format: (val) => this.$n(val, 'currency', this.siteLocaleCurrency),
          },
        ];
      }
      return columns;
    },
    icons() {
      return icons;
    },
  },
  methods: {
    manageDevice(deviceId) {
      this.$emit('openDevice', deviceId, this.deviceChoice);
    },
    bumpDoor(doorId) {
      if (this.deviceLoading[doorId]) this.deviceLoading[doorId].bump = true;
      else this.deviceLoading[doorId] = { bump: true, reboot: false };

      this.$axios
        .post(`/api/access/doors/${doorId}/bump/`)
        .then(() => {
          this.$q.notify({
            message: this.$t('device.bumped'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('device.requestFailed'),
          });
        })
        .finally(() => {
          this.deviceLoading[doorId].bump = false;
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
