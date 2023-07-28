<template>
  <q-table
    :rows="kiosks"
    :columns="[
      {
        name: 'authorised',
        label: 'Authorised',
        field: 'authorised',
        sortable: true,
        format: (val, row) => this.capitaliseFirst(val),
      },
      { name: 'name', label: 'Name', field: 'name', sortable: true },
      {
        name: 'lastSeen',
        label: 'Last Seen',
        field: 'lastSeen',
        sortable: true,
        format: (val, row) => this.formatDate(val),
      },
    ]"
    row-key="id"
    :filter="filter"
    v-model:pagination="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
    :no-data-label="$t('kiosk.nodata')"
    class="q-mx-sm"
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
        <q-th auto-width />
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
          {{ col.label }}
        </q-th>
        <q-th auto-width>
          {{ $t('edit') }}
        </q-th>
        <q-th auto-width>
          {{ $t('delete') }}
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
              <q-btn size="sm" color="accent" :icon="icons.edit" disable />
            </q-item>
          </q-list>
        </q-card>
      </div>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            :icon="props.expand ? icons.down : icons.up"
            @click="props.expand = !props.expand"
          />
        </q-td>
        <q-td v-for="col in props.cols" :key="col.name" :props="props">
          {{ col.value }}
        </q-td>

        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            :icon="icons.edit"
            @click="editKiosk(props.row.id)"
          />

          <q-dialog v-model="editKioskDialog">
            <q-card>
              <q-card-section
                class="row items-center q-pb-none dialog-close-button"
              >
                <q-space />
                <q-btn v-close-popup :icon="icons.close" flat round dense />
              </q-card-section>

              <q-card-section>
                <kiosk-form :kiosk-id="editKioskId" />
              </q-card-section>
            </q-card>
          </q-dialog>
        </q-td>

        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            :icon="icons.delete"
            @click="deleteKiosk(props.row.id)"
          />
        </q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props">
        <q-td colspan="100%">
          <kiosk-details :kiosk="props.row" />
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import KioskForm from '@components/KioskForm.vue';
import KioskDetails from '@components/KioskDetails.vue';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';

export default {
  name: 'KioskList',
  components: { KioskForm, KioskDetails },
  mixins: [formatMixin],
  data() {
    return {
      loading: false,
      filter: '',
      editKioskId: '',
      editKioskDialog: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 10,
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getKiosks']),
    deleteKiosk(id) {
      this.$q
        .dialog({
          title: 'Confirm',
          message: this.$t('kiosk.delete'),
          cancel: {
            color: 'primary',
            flat: true,
            label: this.$t('button.cancel'),
          },
          ok: {
            color: 'primary',
            label: this.$t('button.ok'),
          },
          persistent: true,
        })
        .onOk(() => {
          this.$axios
            .delete(`/api/kiosks/${id}/`, this.form)
            .then(() => {
              this.getKiosks();
            })
            .catch(() => {
              this.$q.dialog({
                title: this.$t('error.error'),
                message: this.$t('error.requestFailed'),
              });
            });
        });
    },
    editKiosk(id) {
      this.editKioskId = id;
      this.editKioskDialog = true;
    },
  },
  mounted() {
    this.loading = true;
    this.getKiosks().finally(() => {
      this.loading = false;
    });
  },
  computed: {
    ...mapGetters('adminTools', ['kiosks']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
@media (max-width: $breakpoint-xs-max)
  .access-list
    width: 100%
</style>
