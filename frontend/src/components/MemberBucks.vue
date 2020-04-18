<template>
  <q-table
    :data="memberBucksTransactions"
    :columns="[{ name: 'description', label: 'Description', field: 'description', sortable: true },
               { name: 'amount',
                 label: 'Amount',
                 field: 'amount',
                 sortable: true,
               },
               { name: 'date',
                 label: 'When',
                 field: 'date',
                 sortable: true, format: (val) => this.formatWhen(val)
               },
    ]"
    row-key="id"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
  >
    <template v-slot:top-left>
      <q-btn
        color="accent"
        :icon="icons.add"
        :label="$t('memberbucks.addFunds')"
        @click="addFunds()"
        class="q-mb-sm q-mr-sm"
      />

      <q-btn
        color="accent"
        :icon="icons.billing"
        :label="$t('memberbucks.manageBilling')"
        @click="manageBilling()"
        class="q-mb-sm q-mr-md"
      />

      <q-input
        v-if="$q.screen.xs"
        outlined
        dense
        debounce="300"
        v-model="filter"
        placeholder="Search"
        style="margin-top: -3px;"
      >
        <template v-slot:append>
          <q-icon :name="icons.search" />
        </template>
      </q-input>
    </template>

    <template
      v-if="$q.screen.gt.xs"
      v-slot:top-right
    >
      <q-input
        outlined
        dense
        debounce="300"
        v-model="filter"
        placeholder="Search"
        style="margin-top: -3px;"
      >
        <template v-slot:append>
          <q-icon :name="icons.search" />
        </template>
      </q-input>
    </template>

    <template v-slot:body-cell-amount="props">
      <q-td>
        <div :class="{ credit: props.value > 0, debit: props.value < 0 }">
          ${{ props.value }}
        </div>
      </q-td>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import MemberBucksAddFunds from 'components/MemberBucksAddFunds';
import MemberBucksManageBilling from 'components/MemberBucksManageBilling';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';

export default {
  name: 'MemberBucks',
  mixins: [formatMixin],
  props: {
    dialog: {
      type: String,
      default: 'transactions',
    },
  },
  data() {
    return {
      filter: '',
      loading: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 12,
      },
      testDialog: '',
    };
  },
  methods: {
    ...mapActions('tools', ['getMemberBucksTransactions', 'getMemberBucksBalance']),
    closeBothDialogs() {
      this.$router.push({ name: 'memberbucks', params: { dialog: 'transactions' } })
        .catch(() => {});
    },
    openAddFundsDialog() {
      this.$q.dialog({
        component: MemberBucksAddFunds,
        parent: this,
      });
    },
    openManageBillingDialog() {
      this.$q.dialog({
        component: MemberBucksManageBilling,
        parent: this,
      });
    },
    addFunds() {
      this.$router.push({ name: 'memberbucks', params: { dialog: 'add' } })
        .catch((error) => {
          if (error.name === 'NavigationDuplicated') {
            this.openAddFundsDialog();
          } else {
            throw error;
          }
        });
    },
    manageBilling() {
      this.$router.push({ name: 'memberbucks', params: { dialog: 'billing' } })
        .catch((error) => {
          if (error.name === 'NavigationDuplicated') {
            this.openManageBillingDialog();
          } else {
            throw error;
          }
        });
    },
  },
  mounted() {
    this.loading = true;
    Promise.all([this.getMemberBucksBalance(), this.getMemberBucksTransactions()]).finally(() => {
      this.loading = false;
    });
    if (this.dialog === 'add') {
      this.openAddFundsDialog();
    } else if (this.dialog === 'billing') {
      this.openManageBillingDialog();
    }
  },
  watch: {
    dialog(dialog) {
      if (dialog === 'add') {
        this.openAddFundsDialog();
      } else if (dialog === 'billing') {
        this.openManageBillingDialog();
      } else {
        this.closeBothDialogs();
      }
    },
  },
  computed: {
    ...mapGetters('tools', ['memberBucksTransactions', 'memberBucksBalance']),
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
