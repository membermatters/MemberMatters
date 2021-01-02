<template>
  <q-table
    :data="interlocks"
    :columns="[
      { name: 'id', label: 'ID', field: 'id', sortable: true },
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
    :no-data-label="$t('interlocks.nodata')"
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
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
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
              v-for="col in props.cols.filter(col => col.name !== 'desc')"
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
              <q-btn
                :ref="`${props.row.id}-reboot`"
                class="q-mr-sm"
                size="sm"
                color="accent"
                @click="rebootInterlock(props.row.id)"
              >
                <q-icon :name="icons.reboot" />
                <q-tooltip>
                  {{ $t('button.rebootDevice') }}
                </q-tooltip>
              </q-btn>

              <q-btn
                size="sm"
                color="accent"
                :to="{name: 'manageInterlock', params: {interlockId: String(props.row.id)}}"
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
      <q-tr
        :props="props"
      >
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          <router-link
            v-if="col.label === 'Name'"
            :to="{name: 'manageInterlock', params: {interlockId: String(props.row.id)}}"
          >
            {{ col.value }}
          </router-link>
          <template v-else>
            {{ col.value }}
          </template>
        </q-td>
        <q-td auto-width>
          <q-btn
            :ref="`${props.row.id}-reboot`"
            class="q-mr-sm"
            size="sm"
            color="accent"
            @click="rebootInterlock(props.row.id)"
          >
            <q-icon :name="icons.reboot" />
            <q-tooltip>
              {{ $t('button.rebootDevice') }}
            </q-tooltip>
          </q-btn>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import icons from "../../icons";
import formatMixin from "../../mixins/formatMixin";

export default {
  name: "InterlocksList",
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
    };
  },
  computed: {
    ...mapGetters("adminTools", ["interlocks"]),
    icons() {
      return icons;
    },
  },
  mounted() {
    this.getInterlocks();
  },
  methods: {
    ...mapActions("adminTools", ["getInterlocks"]),
    rebootInterlock(interlockId) {
      this.$refs[`${interlockId}-reboot`].loading = true;
      this.$axios.post(`/api/access/interlocks/${interlockId}/reboot/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        }).finally(() => {
          this.$refs[`${interlockId}-reboot`].loading = false;
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
