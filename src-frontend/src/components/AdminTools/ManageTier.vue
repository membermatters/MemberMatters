<template>
  <div class="row q-gutter-md">
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm">{{ $t('menuLink.manageTier') }}</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-form ref="formRef" @submit="submitTier()">
          <q-input
            v-model="form.name"
            outlined
            :debounce="debounceLength"
            :label="$t('form.name')"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
          />

          <q-input
            v-model="form.description"
            outlined
            :debounce="debounceLength"
            :label="$t('form.description')"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
          />

          <q-checkbox
            v-model="form.visible"
            :label="$t('form.visibleToMembers')"
          />

          <q-checkbox v-model="form.featured" :label="$t('form.featured')" />

          <q-banner v-if="form.success" class="bg-positive text-white q-my-md">
            {{ $t('form.saved') }}
          </q-banner>

          <q-banner v-if="form.error" class="bg-negative text-white q-my-md">
            {{ $t('form.error') }}
          </q-banner>

          <q-card-actions align="right" class="text-primary">
            <q-btn
              color="negative"
              :label="$t('button.remove')"
              :disable="form.loading"
              @click="removeTier()"
            />
            <q-btn
              color="primary"
              :label="$t('button.submit')"
              :loading="form.loading"
              :disable="form.loading"
              type="submit"
            />
          </q-card-actions>
        </q-form>
      </q-card-actions>
    </q-card>
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm">{{ $t('paymentPlans.title') }}</span>
      </q-card-section>

      <q-card-section class="row items-center q-pt-none">
        <q-table
          flat
          @row-click="managePlan"
          :rows="plans"
          :columns="[
            { name: 'name', label: 'Name', field: 'name', sortable: true },
            {
              name: 'visible',
              label: 'Visible',
              field: 'visible',
              sortable: true,
            },
            {
              name: 'featured',
              label: 'Featured',
              field: 'featured',
              sortable: true,
            },
            {
              name: 'cost',
              label: 'Cost',
              field: 'cost',
              sortable: true,
              format: (val) => `$${val}`,
            },
            {
              name: 'interval',
              label: 'Interval',
              field: 'interval',
              sortable: true,
              format: (val, row) =>
                `${row.intervalCount} ${row.interval}${
                  row.intervalCount > 1 ? 's' : ''
                }`,
            },
          ]"
          row-key="id"
          :filter="filter"
          v-model:pagination="pagination"
          :grid="$q.screen.xs"
          :no-data-label="$t('paymentPlans.nodata')"
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
          <template v-slot:top-left>
            <q-btn
              @click="addPlanDialog = true"
              round
              color="primary"
              :icon="icons.addAlternative"
            >
              <q-tooltip :delay="500">{{ $t('tiers.add') }}</q-tooltip>
            </q-btn>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="addPlanDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">{{ $t('paymentPlans.add') }}</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-form ref="formRef" @submit="submitPlanForm()">
            <div class="row q-col-gutter-sm">
              <q-input
                class="col-sm-6 col-xs-12"
                v-model="planForm.name"
                outlined
                :debounce="debounceLength"
                :label="$t('form.name')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                :disable="form.success"
              />
              <q-input
                class="col-sm-6 col-xs-12"
                v-model="planForm.currency"
                outlined
                :debounce="debounceLength"
                :label="$t('form.currency')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                :disable="form.success"
              />
              <q-input
                class="col-sm-6 col-xs-12"
                v-model="planForm.costString"
                outlined
                :debounce="debounceLength"
                :label="$t('form.cost')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                :disable="form.success"
                prefix="$"
              />

              <q-checkbox
                class="col-sm-6 col-xs-12"
                v-model="planForm.visible"
                :label="$t('form.visibleToMembers')"
              />

              <q-card-section class="col-12">
                <span class="q-ml-sm">{{
                  $t('paymentPlans.recurringDescription')
                }}</span>
              </q-card-section>

              <q-input
                class="col-sm-6 col-xs-12"
                v-model="planForm.intervalCount"
                outlined
                :debounce="debounceLength"
                :label="$t('form.intervalCount')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                :disable="form.success"
              />
              <q-select
                outlined
                class="col-sm-6 col-xs-12"
                v-model="planForm.interval"
                :debounce="debounceLength"
                :label="$t('form.interval')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                :disable="form.success"
                :options="intervalOptions"
                emit-value
                options-dense
                map-options
              />
            </div>

            <q-banner
              v-if="planForm.success"
              class="bg-positive text-white q-my-md"
            >
              {{ $t('paymentPlans.success') }}
            </q-banner>

            <q-banner
              v-if="planForm.error"
              class="bg-negative text-white q-my-md"
            >
              {{ $t('paymentPlans.fail') }}
            </q-banner>

            <q-card-actions v-if="!planForm.success" class="text-primary">
              <q-space />
              <q-btn
                v-close-popup
                flat
                :label="$t('button.cancel')"
                :disable="planForm.loading"
              />
              <q-btn
                color="primary"
                :label="$t('button.submit')"
                :loading="planForm.loading"
                :disable="planForm.loading"
                type="submit"
              />
            </q-card-actions>

            <q-card-actions v-else align="right" class="text-primary">
              <q-btn v-close-popup flat :label="$t('button.close')" />
            </q-card-actions>
          </q-form>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex';
import { AxiosResponse } from 'axios';
import { api } from 'boot/axios';
import icons from '../../icons';
import formatMixin from '../../mixins/formatMixin';
import formMixin from '../../mixins/formMixin';

export default defineComponent({
  name: 'ManageTier',
  mixins: [formatMixin, formMixin],
  setup() {
    const store = useStore();
    const getTiers = () => store.dispatch('adminTools/getTiers');

    return {
      getTiers,
    };
  },
  data() {
    return {
      plans: [],
      form: {
        loading: false,
        error: false,
        success: false,
        name: '',
        description: '',
        visible: false,
        featured: false,
      },
      planForm: {
        loading: false,
        error: false,
        success: false,
        name: '',
        memberTier: '',
        stripeId: '',
        visible: true,
        currency: 'aud',
        costString: '',
        cost: 0,
        intervalCount: 1,
        interval: 'month',
      },
      addPlanDialog: false,
      filter: '',
      pagination: {
        sortBy: 'name',
        descending: true,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        rowsPerPage: (this as any).$q.screen.xs ? 3 : 10,
      },
    };
  },
  mounted() {
    this.getTier();
    this.getPlans();
  },
  computed: {
    icons() {
      return icons;
    },
  },
  methods: {
    getTier() {
      this.planForm.memberTier = this.$route.params.planId.toString();
      api
        .get(`/api/admin/tiers/${this.$route.params.planId}/`)
        .then((response: AxiosResponse) => {
          this.form.name = response.data.name;
          this.form.description = response.data.description;
          this.form.visible = response.data.visible;
          this.form.featured = response.data.featured;
        })
        .catch((error) => {
          if (error.response.status === 404) {
            this.$router.push({ name: 'Error404' });
            return;
          }
          this.$q.dialog({
            title: this.$tc('error.error'),
            message: this.$tc('error.requestFailed'),
          });
        });
    },
    removeTier() {
      this.$q
        .dialog({
          title: this.$tc('confirmAction'),
          message: this.$tc('confirmRemove'),
          cancel: true,
          persistent: true,
        })
        .onOk(() => {
          api
            .delete(`/api/admin/tiers/${this.$route.params.planId}/`)
            .then(() => {
              this.$router.go(-1);
            })
            .catch(() => {
              this.$q.dialog({
                title: this.$tc('error.error'),
                message: this.$tc('error.requestFailed'),
              });
            });
        });
    },
    submitTier() {
      this.form.loading = true;
      this.form.error = false;
      this.form.success = false;
      api
        .put(`/api/admin/tiers/${this.$route.params.planId}/`, this.form)
        .then(() => {
          this.getTiers();
          this.form.success = true;
          this.form.error = false;
        })
        .catch(() => {
          this.form.error = true;
          this.form.success = false;
        })
        .finally(() => (this.form.loading = false));
    },
    submitPlanForm() {
      this.planForm.loading = true;
      this.planForm.error = false;
      this.planForm.success = false;
      this.planForm.cost = parseFloat(this.planForm.costString) * 100;
      api
        .post('/api/admin/plans/', this.planForm)
        .then(() => {
          this.getPlans();
          this.planForm.success = true;
          this.planForm.error = false;
          this.addPlanDialog = false;
          this.resetPlanForm();
        })
        .catch(() => {
          this.planForm.success = false;
          this.planForm.error = true;
        })
        .finally(() => (this.planForm.loading = false));
    },
    getPlans() {
      api
        .get(`/api/admin/tiers/${this.$route.params.planId}/plans/`)
        .then((response: AxiosResponse) => {
          this.plans = response.data;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$tc('error.error'),
            message: this.$tc('error.requestFailed'),
          });
        });
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    managePlan(evt: InputEvent, row: any) {
      this.$router.push({ name: 'managePlan', params: { planId: row.id } });
    },
    resetForm() {
      this.form = {
        loading: false,
        error: false,
        success: false,
        name: '',
        description: '',
        visible: false,
        featured: false,
      };
    },
    resetPlanForm() {
      this.planForm = {
        loading: false,
        error: false,
        success: false,
        name: '',
        memberTier: '',
        stripeId: '',
        visible: true,
        currency: 'aud',
        costString: '',
        cost: 0,
        intervalCount: 1,
        interval: 'month',
      };
    },
  },
});
</script>
