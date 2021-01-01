<template>
  <div class="row q-gutter-md">
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm">{{ $t("menuLink.manageTier") }}</span>
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
            :disable="form.success"
          />

          <q-input
            v-model="form.description"
            outlined
            :debounce="debounceLength"
            :label="$t('form.description')"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
            :disable="form.success"
          />

          <q-checkbox
            v-model="form.visible"
            :label="$t('form.visibleToMembers')"
          />

          <q-banner v-if="form.success" class="bg-positive text-white q-my-md">
            {{ $t("tierForm.success") }}
          </q-banner>

          <q-banner v-if="form.error" class="bg-negative text-white q-my-md">
            {{ $t("tierForm.fail") }}
          </q-banner>

          <q-card-actions
            v-if="!form.success"
            align="right"
            class="text-primary"
          >
            <q-btn
              v-close-popup
              flat
              :label="$t('button.cancel')"
              :disable="form.loading"
            />
            <q-btn
              color="primary"
              :label="$t('button.submit')"
              :loading="form.loading"
              :disable="form.loading"
              type="submit"
            />
          </q-card-actions>

          <q-card-actions v-else align="right" class="text-primary">
            <q-btn
              v-close-popup
              flat
              :label="$t('button.close')"
              @click="resetForm()"
            />
          </q-card-actions>
        </q-form>
      </q-card-actions>
    </q-card>
    <q-card>
      <q-card-section class="row items-center">
        <span class="q-ml-sm">{{ $t("paymentPlans.title") }}</span>
      </q-card-section>

      <q-card-section class="row items-center q-pt-none">
        <q-table
          flat
          @row-click="manageTier"
          :data="tiers"
          :columns="[
            { name: 'name', label: 'Name', field: 'name', sortable: true },
            { name: 'description', label: 'Description', field: 'description' },
          ]"
          row-key="name"
          :filter="filter"
          :pagination.sync="pagination"
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
              <q-tooltip :delay="500">{{ $t("tiers.add") }}</q-tooltip>
            </q-btn>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog v-model="addPlanDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <span class="q-ml-sm">{{ $t("paymentPlans.add") }}</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-form ref="formRef" @submit="submitPlan()">
            <q-input
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
              v-model="planForm.description"
              outlined
              :debounce="debounceLength"
              :label="$t('form.description')"
              :rules="[
                (val) =>
                  validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
              ]"
              :disable="planForm.success"
            />

            <q-checkbox
              v-model="planForm.visible"
              :label="$t('form.visibleToMembers')"
            />

            <q-banner
              v-if="planForm.success"
              class="bg-positive text-white q-my-md"
            >
              {{ $t("paymentPlans.success") }}
            </q-banner>

            <q-banner
              v-if="planForm.error"
              class="bg-negative text-white q-my-md"
            >
              {{ $t("paymentPlans.fail") }}
            </q-banner>

            <q-card-actions
              v-if="!planForm.success"
              align="right"
              class="text-primary"
            >
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
              <q-btn
                v-close-popup
                flat
                :label="$t('button.close')"
                @click="resetPlanForm()"
              />
            </q-card-actions>
          </q-form>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/composition-api";
import { createNamespacedHelpers } from "vuex-composition-helpers";
import { AxiosResponse } from "axios";
import icons from "../../icons";
import formatMixin from "../../mixins/formatMixin";
import formMixin from "../../mixins/formMixin";

export default defineComponent({
  name: "ManageTier",
  mixins: [formatMixin, formMixin],
  setup() {
    const { useActions } = createNamespacedHelpers("adminTools");
    const { getTiers } = useActions(["getTiers"]);

    return {
      getTiers,
    };
  },
  data() {
    return {
      form: {
        loading: false,
        error: false,
        success: false,
        name: "",
        description: "",
        visible: false,
      },
      planForm: {
        loading: false,
        error: false,
        success: false,
        name: "",
        description: "",
        visible: false,
      },
      addPlanDialog: false,
      filter: "",
      pagination: {
        sortBy: "name",
        descending: true,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        rowsPerPage: (this as any).$q.screen.xs ? 3 : 10,
      },
    };
  },
  mounted() {
    this.getTier();
  },
  computed: {
    icons() {
      return icons;
    },
  },
  methods: {
    getTier() {
      this.$axios
        .get(`/api/admin/tiers/${this.$route.params.tierId}/`)
        .then((response: AxiosResponse) => {
          console.log(response);
          this.form.name = response.data.name;
          this.form.description = response.data.description;
          this.form.visible = response.data.visible;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$tc("error.error"),
            message: this.$tc("error.requestFailed"),
          });
        });
    },
    submitTier() {
      this.form.loading = true;
      this.$axios
        .put(`/api/admin/tiers/${this.$route.params.tierId}/`, this.form)
        .then(() => this.getTiers())
        .catch(() => {
          this.$q.dialog({
            title: this.$tc("error.error"),
            message: this.$tc("error.requestFailed"),
          });
        })
        .finally(() => (this.form.loading = false));
    },
    resetForm() {
      this.form = {
        loading: false,
        error: false,
        success: false,
        name: "",
        description: "",
        visible: false,
      };
    },
  },
});
</script>
