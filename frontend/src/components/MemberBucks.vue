<template>
  <div v-if="this.features.enableStripe">
    <q-table
      :rows="memberBucksTransactions"
      :columns="[
        {
          name: 'description',
          label: 'Description',
          field: 'description',
          sortable: true,
        },
        { name: 'amount', label: 'Amount', field: 'amount', sortable: true },
        {
          name: 'date',
          label: 'When',
          field: 'date',
          sortable: true,
          format: (val) => this.formatWhen(val),
        },
      ]"
      row-key="id"
      :filter="filter"
      v-model:pagination="pagination"
      :loading="loading"
      :grid="$q.screen.xs"
    >
      <template v-slot:top-left>
        <div class="row q-pt-sm">
          <q-btn
            color="accent"
            :icon="icons.add"
            :label="$t('memberbucks.addFunds')"
            class="q-mb-sm q-mr-sm"
            @click="addFunds()"
          />

          <q-btn
            color="accent"
            :icon="icons.donate"
            :label="$t('memberbucks.donateFunds')"
            class="q-mb-sm q-mr-sm"
            @click="donateFunds()"
          />

          <q-btn
            color="accent"
            :icon="icons.billing"
            :label="$t('memberbucks.manageBilling')"
            class="q-mb-sm q-mr-md"
            @click="manageBilling()"
          />
          <q-space />

          <q-input
            v-model="filter"
            outlined
            dense
            debounce="300"
            placeholder="Search"
            class="q-mt-none q-pt-none"
          >
            <template v-slot:append>
              <q-icon :name="icons.search" />
            </template>
          </q-input>
        </div>
        <div class="row q-pt-sm">
          {{ $t("memberbucks.currentBalance") }}
          {{ $n(memberBucksBalance, "currency") }}
        </div>
      </template>

      <!--      <template v-if="$q.screen.gt.xs" v-slot:top-right>-->
      <!--        <div class="row">-->
      <!--          -->
      <!--        </div>-->
      <!--      </template>-->

      <template v-slot:body-cell-amount="props">
        <q-td>
          <div :class="{ credit: props.value > 0, debit: props.value < 0 }">
            ${{ props.value }}
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
  <div v-else>
    <q-card flat>
      <q-card-section>
        <div class="text-h6">
          {{ $t("menuLink.memberbucks") }}
        </div>
        <div class="text-subtitle2">
          {{ $t("error.stripeNotConfiguredFeature") }}
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import MemberBucksAddFunds from "components/MemberBucksAddFunds";
import MemberBucksDonateFunds from "components/MemberBucksDonateFunds";
import icons from "../icons";
import formatMixin from "../mixins/formatMixin";

export default {
  name: "MemberBucks",
  mixins: [formatMixin],
  props: {
    dialog: {
      type: String,
      default: "transactions",
    },
  },
  data() {
    return {
      filter: "",
      loading: false,
      pagination: {
        sortBy: "date",
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 12,
      },
      testDialog: "",
    };
  },
  methods: {
    ...mapActions("tools", [
      "getMemberBucksTransactions",
      "getMemberBucksBalance",
    ]),
    closeDialogs() {
      this.$router.push({
        name: "memberbucks",
        params: { dialog: "transactions" },
      });
    },
    openAddFundsDialog() {
      this.$q.dialog({
        component: MemberBucksAddFunds,
      });
    },
    openDonateFundsDialog() {
      this.$q.dialog({
        component: MemberBucksDonateFunds,
      });
    },
    addFunds() {
      this.$router
        .push({ name: "memberbucks", params: { dialog: "add" } })
        .catch((error) => {
          if (error.name === "NavigationDuplicated") {
            this.openAddFundsDialog();
          } else {
            throw error;
          }
        });
    },
    donateFunds() {
      this.$router
        .push({ name: "memberbucks", params: { dialog: "donate" } })
        .catch((error) => {
          if (error.name === "NavigationDuplicated") {
            this.openDonateFundsDialog();
          } else {
            throw error;
          }
        });
    },
    manageBilling() {
      this.$router.push({ name: "billing" });
    },
  },
  watch: {
    dialog(dialog) {
      if (dialog === "add") {
        this.openAddFundsDialog();
      } else if (dialog === "donate") {
        this.openDonateFundsDialog();
      } else {
        this.closeDialogs();
      }
    },
  },
  mounted() {
    this.loading = true;
    Promise.all([
      this.getMemberBucksBalance(),
      this.getMemberBucksTransactions(),
    ]).finally(() => {
      this.loading = false;
    });
    if (this.dialog === "add") {
      this.openAddFundsDialog();
    } else if (this.dialog === "donate") {
      this.openDonateFundsDialog();
    }
  },
  computed: {
    ...mapGetters("tools", ["memberBucksTransactions", "memberBucksBalance"]),
    ...mapGetters("config", ["features"]),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
.credit
  color: green

  .debit
    color: red
</style>
