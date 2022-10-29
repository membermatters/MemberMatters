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
          {{ $t("button.actions") }}
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
              v-for="col in props.cols.filter((col) => col.name !== 'desc')"
              :key="col.name"
            >
              <q-item-section>
                <q-item-label>{{ col.label }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label caption>
                  {{ col.value }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item class="q-mt-sm row justify-center">
              <template v-if="deviceChoice === 'doors'">
                <q-btn
                  :loading="deviceLoading[props.row.id]?.unlock"
                  class="q-mr-sm"
                  size="sm"
                  color="accent"
                  @click.stop="unlockDoor(props.row.id)"
                >
                  <q-icon :name="icons.unlock" />
                  <q-tooltip>
                    {{ $t("button.unlockDoor") }}
                  </q-tooltip>
                </q-btn>
              </template>

              <q-btn
                :loading="deviceLoading[props.row.id]?.reboot"
                class="q-mr-sm"
                size="sm"
                color="accent"
                @click.stop="rebootDevice(props.row.id)"
              >
                <q-icon :name="icons.reboot" />
                <q-tooltip>
                  {{ $t("button.rebootDevice") }}
                </q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="accent"
                @click.stop="manageDevice(props.row.id)"
              >
                <q-icon :name="icons.settings" />
                <q-tooltip>
                  {{ $t("button.manage") }}
                </q-tooltip>
              </q-btn>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          :class="{
            offline: props.row.offline && col.name === 'lastSeen',
          }"
        >
          {{ col.value }}
        </q-td>

        <q-td auto-width>
          <template v-if="deviceChoice === 'doors'">
            <q-btn
              :loading="deviceLoading[props.row.id]?.unlock"
              class="q-mr-sm"
              size="sm"
              color="accent"
              @click.stop="unlockDoor(props.row.id)"
            >
              <q-icon :name="icons.unlock" />
              <q-tooltip>
                {{ $t("button.unlockDoor") }}
              </q-tooltip>
            </q-btn>
          </template>

          <q-btn
            :loading="deviceLoading[props.row.id]?.sync"
            class="q-mr-sm"
            size="sm"
            color="accent"
            @click.stop="syncDevice(props.row.id)"
          >
            <q-icon :name="icons.sync" />
            <q-tooltip>
              {{ $t("button.syncDevice") }}
            </q-tooltip>
          </q-btn>

          <q-btn
            :loading="deviceLoading[props.row.id]?.reboot"
            class="q-mr-sm"
            size="sm"
            color="accent"
            @click.stop="rebootDevice(props.row.id)"
          >
            <q-icon :name="icons.reboot" />
            <q-tooltip>
              {{ $t("button.rebootDevice") }}
            </q-tooltip>
          </q-btn>

          <q-btn
            size="sm"
            color="accent"
            @click.stop="manageDevice(props.row.id)"
          >
            <q-icon :name="icons.settings" />
            <q-tooltip>
              {{ $t("button.manage") }}
            </q-tooltip>
          </q-btn>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import icons from "../../icons";
import formatMixin from "src/mixins/formatMixin";

export default {
  props: {
    deviceChoice: {
      type: String,
    },
    tableData: {
      type: Array,
    },
  },
  name: "DevicesList",
  mixins: [formatMixin],
  data() {
    return {
      loading: false,
      filter: "",
      pagination: {
        sortBy: "lastSeen",
        descending: true,
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
            unlock: false,
          };
        });
      },
      deep: true,
    },
  },
  computed: {
    columnI18n() {
      let columns = [];
      if (this.deviceChoice === "doors") {
        columns = [
          {
            name: "id",
            label: this.$t("tableHeading.id"),
            field: "id",
            sortable: true,
          },
          { name: "name", label: "Name", field: "name", sortable: true },
          {
            name: "ipAddress",
            label: "IP",
            field: "ipAddress",
            sortable: true,
          },
          {
            name: "lastSeen",
            label: this.$t("access.lastSeen"),
            field: "lastSeen",
            sortable: true,
            format: (val) => this.formatDate(val),
          },
          {
            name: "usage",
            label: this.$t("access.usage"),
            field: "usage",
            sortable: true,
          },
        ];
      } else {
        columns = [
          { name: "id", label: "ID", field: "id", sortable: true },
          { name: "name", label: "Name", field: "name", sortable: true },
          {
            name: "ipAddress",
            label: "IP",
            field: "ipAddress",
            sortable: true,
          },
          {
            name: "lastSeen",
            label: "Last Seen",
            field: "lastSeen",
            sortable: true,
            format: (val) => this.formatDate(val),
          },
          {
            name: "usage",
            label: "Logged Time",
            field: "usage",
            sortable: true,
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
      this.$emit("openDevice", deviceId, this.deviceChoice);
    },
    rebootDevice(deviceId) {
      if (this.deviceLoading[deviceId])
        this.deviceLoading[deviceId].reboot = true;
      else
        this.deviceLoading[deviceId] = {
          reboot: true,
          unlock: false,
          sync: false,
        };

      this.$axios
        .post(`/api/access/${this.deviceChoice}/${deviceId}/reboot/`)
        .then((res) => {
          if (res?.success) this.$q.notify(this.$t("success"));
          else this.$q.notify(this.$t("error.requestFailed"));
        })
        .catch(() => {
          this.$q.notify(this.$t("error.requestFailed"));
        })
        .finally(() => {
          this.deviceLoading[deviceId].reboot = false;
        });
    },
    syncDevice(deviceId) {
      if (this.deviceLoading[deviceId])
        this.deviceLoading[deviceId].sync = true;
      else
        this.deviceLoading[deviceId] = {
          sync: true,
          reboot: false,
          unlock: false,
        };

      this.$axios
        .post(`/api/access/${this.deviceChoice}/${deviceId}/sync/`)
        .then((res) => {
          if (res?.success) this.$q.notify(this.$t("success"));
          else this.$q.notify(this.$t("error.requestFailed"));
        })
        .catch(() => {
          this.$q.notify(this.$t("error.requestFailed"));
        })
        .finally(() => {
          this.deviceLoading[deviceId].sync = false;
        });
    },
    unlockDoor(doorId) {
      if (this.deviceLoading[doorId]) this.deviceLoading[doorId].unlock = true;
      else
        this.deviceLoading[doorId] = {
          unlock: true,
          reboot: false,
          sync: false,
        };

      this.$axios
        .post(`/api/access/doors/${doorId}/unlock/`)
        .then((res) => {
          if (res?.success) this.$q.notify(this.$t("success"));
          else this.$q.notify(this.$t("error.requestFailed"));
        })
        .catch(() => {
          this.$q.notify(this.$t("error.requestFailed"));
        })
        .finally(() => {
          this.deviceLoading[doorId].unlock = false;
        });
    },
  },
};
</script>

<style lang="sass" scoped>
@keyframes pulsate
    0%
      background-color: orange

    50%
      background-color: red

    100%
      background-color: orange

.offline
  background-color: red
  color: white
  animation: pulsate 2s ease-out
  animation-iteration-count: infinite

@media (max-width: $breakpoint-xs-max)
  .access-list
    width: 100%
</style>
