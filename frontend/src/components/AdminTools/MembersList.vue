<template>
  <div style="max-width: 100%">
    <q-table
      :rows="displayMemberList"
      :no-data-label="$t('adminTools.noMembers')"
      :columns="columns"
      row-key="email"
      :filter="filter"
      v-model:pagination="pagination"
      :loading="loading"
      :grid="$q.screen.lt.md"
      class="full-width"
      @row-click="
        (evt, row) => {
          $router.push({
            name: 'manageMember',
            params: { memberId: row.id },
          });
        }
      "
    >
      <template v-slot:top-left>
        <div class="row flex items-start">
          <template v-if="$q.screen.lt.md">
            <div class="full-width">
              <q-btn-dropdown
                class="q-mb-sm"
                color="primary"
                :label="$t('adminTools.exportOptions')"
              >
                <q-list>
                  <q-item v-close-popup clickable @click="exportCsv">
                    <q-item-section>
                      <q-item-label>{{
                        $t("adminTools.exportCsv")
                      }}</q-item-label>
                    </q-item-section>
                  </q-item>

                  <q-item
                    v-close-popup
                    clickable
                    @click="copyEmailsToClipboard"
                  >
                    <q-item-section>
                      <q-item-label>{{
                        $t("adminTools.emailAddresses")
                      }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
            </div>
            <div class="full-width">
              <q-select
                v-model="memberState"
                class="q-mb-sm"
                outlined
                emit-value
                :options="filterOptions"
                :label="$t('adminTools.filterOptions')"
                dense
              />
            </div>
          </template>

          <template v-else>
            <q-btn
              class="q-mr-sm q-mb-sm"
              color="primary"
              :icon="icons.export"
              :label="$t('adminTools.exportCsv')"
              @click="exportCsv"
            />
            <q-btn
              class="q-mr-sm q-mb-sm"
              color="primary"
              :icon="icons.email"
              :label="$t('adminTools.emailAddresses')"
              @click="copyEmailsToClipboard"
            />
          </template>
        </div>
      </template>
      <template v-slot:top-right>
        <q-select
          v-if="$q.screen.gt.sm"
          v-model="memberState"
          class="q-mr-sm"
          style="min-width: 100px"
          outlined
          emit-value
          :options="filterOptions"
          :label="$t('adminTools.filterOptions')"
          dense
        />

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
  </div>
</template>

<script lang="ts">
import { copyToClipboard } from "quasar";
import icons from "@icons";
import formatMixin from "@mixins/formatMixin";
import { exportFile } from "quasar";
import { stringify } from "csv-stringify";
import { mapGetters } from "vuex";
import { MemberProfile } from "types/member";

export default {
  name: "MembersList",
  mixins: [formatMixin],
  data() {
    return {
      members: [],
      filter: "",
      memberState: "Active",
      loading: false,
      pagination: {
        sortBy: "date",
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 10,
      },
    };
  },
  computed: {
    ...mapGetters("config", ["features"]),
    displayMemberList() {
      if (this.memberState === "All") return this.members;
      return this.members.filter(
        (member: MemberProfile) => member.state === this.memberState
      );
    },
    memberEmails() {
      return this.displayMemberList
        .filter((member: MemberProfile) => !member.excludeFromEmailExport)
        .map((member: MemberProfile) => member.email)
        .join(",");
    },
    icons() {
      return icons;
    },
    filterOptions() {
      return [
        { label: this.$t("adminTools.all"), value: "All" },
        { label: this.$t("adminTools.active"), value: "Active" },
        { label: this.$t("adminTools.inactive"), value: "Inactive" },
        { label: this.$t("adminTools.new"), value: "Needs Induction" },
        { label: this.$t("adminTools.accountOnly"), value: "Account Only" },
      ];
    },
    columns() {
      return [
        {
          name: "name",
          label: this.$t("tableHeading.name"),
          field: (row: MemberProfile) => row.name.full,
          sortable: true,
          format: (val: string, row: MemberProfile) =>
            `${val} (${row.screenName})`,
        },
        {
          name: "rfid",
          label: this.$t("tableHeading.rfid"),
          field: "rfid",
          sortable: true,
        },
        {
          name: "email",
          label: this.$t("tableHeading.email"),
          field: "email",
          sortable: true,
        },
        // this is weird syntax, but cleanest way to do it
        ...(this.features?.signup?.collectVehicleRegistrationPlate
          ? [
              {
                name: "vehicleRegistration",
                label: this.$t("form.vehicleRegistrationPlate"),
                field: "vehicleRegistrationPlate",
                sortable: true,
              },
            ]
          : []),
        {
          name: "subscriptionStatus",
          label: this.$t("tableHeading.subscriptionStatus"),
          field: "subscriptionStatus",
          sortable: true,
        },
        {
          name: "status",
          label: this.$t("tableHeading.status"),
          field: "state",
          sortable: true,
        },
      ];
    },
  },
  mounted() {
    this.getMembers();
  },
  methods: {
    getMembers() {
      this.loading = true;
      this.$axios
        .get("/api/admin/members/")
        .then((response) => {
          this.members = response.data;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    exportCsv() {
      stringify(
        this.displayMemberList,
        {
          columns: ["name.full", "email", "state"],
        },
        (err, output) => {
          const status = exportFile("member-export.csv", output, "text/csv");

          if (status !== true) {
            this.$q.notify({
              message: this.$t("error.downloadFailed"),
              color: "negative",
              icon: "warning",
            });
          }
        }
      );
    },
    copyEmailsToClipboard() {
      copyToClipboard(this.memberEmails)
        .then(() => {
          this.$q.dialog({
            dark: true,
            title: this.$t("adminTools.copyEmailListSuccess", {
              count: this.displayMemberList.length,
            }),
            message: this.$t("adminTools.copyEmailListSuccessDescription", {
              excludedCount:
                this.displayMemberList.length -
                this.displayMemberList.filter(
                  (member: MemberProfile) => !member.excludeFromEmailExport
                ).length,
            }),
          });
        })
        .catch(() => {
          this.$q.dialog({
            dark: true,
            title: this.$t("error.copyToClipboard"),
            message: this.$t("error.copyToClipboardDescription"),
          });
        });
    },
  },
};
</script>

<style scoped lang="scss">
.td {
  padding: 0;
}
</style>
