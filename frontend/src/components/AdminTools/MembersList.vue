<template>
  <div style="max-width: 100%">
    <q-table
      :data="displayMemberList"
      :columns="columns"
      row-key="email"
      :filter="filter"
      :pagination.sync="pagination"
      :loading="loading"
      :grid="$q.screen.lt.md"
      class="full-width"
      @row-click="
        (evt, row) => {
          $router.push({ name: 'manageMember', params: { memberId: row.id } });
        }
      "
    >
      <template v-slot:top-left>
        <div class="row flex items-start">
          <template v-if="$q.screen.lt.md">
            <div class="full-width">
              <q-btn-dropdown
                class="q-mb-xs-sm"
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

                  <q-item v-close-popup clickable @click="exportEmails">
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
                class="q-mb-xs-sm"
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
              class="q-mr-sm q-mb-xs-sm"
              color="primary"
              :icon="icons.export"
              :label="$t('adminTools.exportCsv')"
              @click="exportCsv"
            />
            <q-btn
              class="q-mr-sm q-mb-xs-sm"
              color="primary"
              :icon="icons.email"
              :label="$t('adminTools.emailAddresses')"
              @click="exportEmails"
            />
          </template>
        </div>
      </template>
      <template v-slot:top-right>
        <q-select
          v-model="memberState"
          class="q-mr-sm"
          style="min-width: 100px;"
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

<script>
import icons from "@icons";
import formatMixin from "@mixins/formatMixin";
import { exportFile } from "quasar";
import stringify from "csv-stringify";

export default {
  name: "MembersList",
  mixins: [formatMixin],
  data() {
    return {
      manageMemberModal: false,
      manageMemberModalMember: null,
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
    displayMemberList() {
      if (this.memberState === "All") return this.members;
      return this.members.filter((member) => member.state === this.memberState);
    },
    memberEmails() {
      return this.displayMemberList.map((member) => member.email).join(",");
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
        { label: this.$t("adminTools.accountOnly"), value: "Account only" },
      ];
    },
    columns() {
      return [
        {
          name: "name",
          label: "Name",
          field: (row) => row.name.full,
          sortable: true,
          format: (val, row) => `${val} (${row.screenName})`,
        },
        {
          name: "rfid",
          label: "RFID",
          field: "rfid",
          sortable: true,
        },
        {
          name: "email",
          label: "Email",
          field: "email",
          sortable: true,
        },
        {
          name: "memberType",
          label: "Member Type",
          field: (row) => row.memberType.name,
          sortable: true,
        },
        {
          name: "groups",
          label: "Groups",
          field: "groups",
          sortable: true,
          format: (val, row) =>
            row.groups.map((group) => group.name).join(", "),
        },
        {
          name: "status",
          label: "Status",
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
    resetManageMemberModal() {
      this.manageMemberModal = false;
      this.manageMemberModalMember = null;
    },
    openManageMemberModal(member) {
      this.manageMemberModal = true;
      this.manageMemberModalMember = member;
    },
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
              message: "Browser denied file download...",
              color: "negative",
              icon: "warning",
            });
          }
        }
      );
    },
    exportEmails() {
      this.$q.dialog({
        dark: true,
        title: `${this.displayMemberList.length} Email Addresses`,
        message: this.memberEmails,
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
