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
        @click="$router.push({ name: 'memberbucks', params: { dialog: 'add' } })"
        class="q-mb-sm q-mr-sm"
      />

      <q-btn
        color="accent"
        :icon="icons.billing"
        :label="$t('memberbucks.manageBilling')"
        @click="$router.push({ name: 'memberbucks', params: { dialog: 'billing' } })"
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

      <q-dialog
        v-model="addFunds"
      >
        HI
      </q-dialog>

      <q-dialog
        v-model="manageBilling"
      >
        HI
      </q-dialog>
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
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';

export default {
  name: 'MemberBucks',
  mixins: [formatMixin],
  props: {
    dialog: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      filter: '',
      loading: false,
      addFunds: false,
      manageBilling: false,
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
  },
  mounted() {
    this.loading = true;
    Promise.all([this.getMemberBucksBalance(), this.getMemberBucksTransactions()]).finally(() => {
      this.loading = false;
    });
  },
  watch: {
    dialog(value) {
      this.testDialog = value;
      if (value === 'add') {
        console.log('add');
        this.manageBilling = false;
        this.addFunds = true;
      } else if (value === 'billing') {
        this.manageBilling = true;
        this.addFunds = false;
      } else {
        this.manageBilling = false;
        this.addFunds = false;
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
