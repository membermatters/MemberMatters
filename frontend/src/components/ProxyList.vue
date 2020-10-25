<template>
  <q-table
    :data="proxies"
    :columns="[{ name: 'name', label: 'Proxy Name', field: 'name', sortable: true },
               { name: 'date',
                 label: 'Date',
                 field: 'date',
                 sortable: true,
                 format: (val, row) => this.formatDate(val)
               },
               { name: 'type', label: 'Meeting Type', field: 'type', sortable: true },
    ]"
    row-key="id"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
  >
    <template #top-left>
      <q-btn
        color="accent"
        :icon="icons.add"
        :label="$t('proxyForm.newProxy')"
        class="q-mb-sm"
        @click="newProxy = true"
      />

      <q-dialog
        v-model="newProxy"
      >
        <proxy-form @close-form="proxySubmitted()" />
      </q-dialog>
    </template>

    <template #top-right>
      <q-input
        v-model="filter"
        outlined
        dense
        debounce="300"
        placeholder="Search"
      >
        <template #append>
          <q-icon :name="icons.search" />
        </template>
      </q-input>
    </template>

    <template #header="props">
      <q-tr :props="props">
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.label }}
        </q-th>
        <q-th auto-width>
          Delete
        </q-th>
      </q-tr>
    </template>

    <template #body="props">
      <q-tr :props="props">
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.value }}
        </q-td>
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            :icon="icons.delete"
            @click="confirmDelete(props.row.id)"
          />
        </q-td>
      </q-tr>
    </template>

    <template #item="props">
      <div
        class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
        :style="props.selected ? 'transform: scale(0.95);' : ''"
      >
        <q-card :class="props.selected ? 'bg-grey-2' : ''">
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
            <q-item>
              <q-btn
                size="sm"
                color="accent"
                :icon="icons.delete"
                class="q-mb-sm"
                @click="confirmDelete(props.row.id)"
              >
                Delete
              </q-btn>
            </q-item>
          </q-list>
        </q-card>
      </div>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';
import ProxyForm from './ProxyForm';

export default {
  name: 'ProxyList',
  components: { ProxyForm },
  mixins: [formatMixin],
  data() {
    return {
      filter: '',
      loading: false,
      newProxy: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 4 : 12,
      },
    };
  },
  methods: {
    ...mapActions('tools', ['getProxies']),
    proxySubmitted() {
      this.newProxy = false;
      this.getProxies();
    },
    confirmDelete(id) {
      this.$q.dialog({
        title: this.$t('proxyForm.deleteTitle'),
        message: this.$t('proxyForm.delete'),
        persistent: true,
        ok: {
          label: this.$t('button.ok'),
          color: 'primary',
        },
        cancel: {
          label: this.$t('button.cancel'),
          color: 'primary',
          flat: true,
        },
      }).onOk(() => {
        this.$axios.delete(`api/proxies/${id}/`)
          .then(() => {
            this.getProxies();
          });
      });
    },
  },
  mounted() {
    this.loading = true;
    this.getProxies()
      .finally(() => {
        this.loading = false;
      });
  },
  computed: {
    ...mapGetters('tools', ['proxies']),
    icons() {
      return icons;
    },
  },
};
</script>
