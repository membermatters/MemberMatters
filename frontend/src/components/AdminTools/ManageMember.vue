<template>
  <div class="column">
    <h3 class="q-mt-none q-mb-md">
      {{ profileForm.firstName }} {{ profileForm.lastName }}
    </h3>
    <q-card
      class="q-mb-none"
      style="background-color: transparent"
      :class="{ 'q-pb-lg': $q.screen.xs }"
    >
      <q-tabs v-model="tab" align="justify" narrow-indicator>
        <q-tab name="profile" :label="$t('menuLink.profile')" />
        <q-tab name="access" :label="$t('adminTools.access')" />
        <q-tab name="billing" :label="$t('adminTools.billing')" />
        <q-tab name="log" disable :label="$t('adminTools.log')" />
        <!--        <q-tab-->
        <!--          name="memberbucks"-->
        <!--          disable-->
        <!--          :label="$t('menuLink.memberbucks')"-->
        <!--        />-->
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="profile" class="q-px-lg q-py-lg">
          <div
            class="row justify-start q-pt-sm"
            :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
          >
            <q-btn
              v-if="selectedMember.state === 'Inactive'"
              class="q-mr-sm q-mb-sm"
              color="positive"
              :label="$t('adminTools.enableAccess')"
              :loading="stateLoading"
              @click="setMemberState('active')"
            />
            <q-btn
              v-else-if="
                selectedMember.state === 'Needs Induction' ||
                selectedMember.state === 'Account only'
              "
              class="q-mr-sm q-mb-sm"
              color="primary"
              :label="$t('adminTools.makeMember')"
              :loading="stateLoading"
              @click="activateMember()"
            />
            <q-btn
              v-else
              class="q-mr-sm q-mb-sm"
              color="negative"
              :label="$t('adminTools.disableAccess')"
              :loading="stateLoading"
              @click="setMemberState('inactive')"
            />

            <q-btn-dropdown
              style="min-width: 170px"
              class="q-mr-sm q-mb-sm"
              color="primary"
              :label="$t('menuLink.adminTools')"
            >
              <q-list>
                <q-item v-close-popup clickable @click="sendWelcomeEmail">
                  <q-item-section>
                    <q-item-label>{{
                      $t("adminTools.sendWelcomeEmail")
                    }}</q-item-label>
                  </q-item-section>
                </q-item>

                <template v-if="selectedMember.xero.accountId">
                  <q-item v-close-popup clickable @click="createInvoice()">
                    <q-item-section>
                      <q-item-label>{{
                        $t("adminTools.createInvoice")
                      }}</q-item-label>
                    </q-item-section>
                  </q-item>

                  <q-item v-close-popup clickable>
                    <q-item-section>
                      <a
                        :href="`https://go.xero.com/Contacts/View/${this.selectedMember.xero.accountId}`"
                        target="_blank"
                      >
                        <q-item-label>{{
                          $t("adminTools.openXero")
                        }}</q-item-label>
                      </a>
                    </q-item-section>
                  </q-item>
                </template>
              </q-list>
            </q-btn-dropdown>
          </div>

          <div
            class="text-body1"
            :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
          >
            {{ $t("adminTools.memberState") }}: {{ selectedMember.state }}
          </div>

          <div class="row q-pt-md">
            <div
              class="col-12 col-md-6"
              :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
            >
              <q-form ref="formRef">
                <h5 class="q-my-sm">
                  {{ $t("adminTools.mainProfile") }}
                </h5>
                <q-input
                  v-model="profileForm.email"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.email')"
                  :rules="[
                    (val) =>
                      validateEmail(val) || $t('validation.invalidEmail'),
                  ]"
                  @input="saveChange('email')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.email"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.rfidCard"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.rfidCard')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                  ]"
                  @input="saveChange('rfidCard')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.rfidCard"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.firstName"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.firstName')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                  ]"
                  @input="saveChange('firstName')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.firstName"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.lastName"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.lastName')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                  ]"
                  @input="saveChange('lastName')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.lastName"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.phone"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.phone')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.invalidPhone'),
                  ]"
                  @input="saveChange('phone')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.phone"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.screenName"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.screenName')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                  ]"
                  @input="saveChange('screenName')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.screenName"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-select
                  v-model="profileForm.memberType"
                  outlined
                  :label="$t('form.memberType')"
                  :options="memberTypes"
                  option-value="id"
                  option-label="name"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                  ]"
                  @input="saveChange('memberType')"
                >
                  <template #append>
                    <saved-notification
                      v-model="saved.memberType"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-select>
              </q-form>
            </div>

            <div
              class="col-12 col-md-6"
              :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
            >
              <h5 class="q-my-sm">
                {{ $t("menuLink.memberbucks") }}
              </h5>
              <q-list bordered padding class="rounded-borders">
                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{
                        selectedMember.memberBucks.balance
                          ? $n(selectedMember.memberBucks.balance, "currency")
                          : $t("error.noValue")
                      }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`memberbucks.currentBalance`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{
                        selectedMember.memberBucks.lastPurchase
                          ? selectedMember.memberBucks.lastPurchase
                          : $t("error.noValue")
                      }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`memberbucks.lastPurchase`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>

              <h5 class="q-mt-md q-mb-sm">
                {{ $t("adminTools.otherAttributes") }}
              </h5>
              <q-list bordered padding class="rounded-borders">
                <q-item v-for="item in ['id', 'state', 'admin']" :key="item">
                  <q-item-section>
                    <q-item-label lines="1">
                      <template>
                        {{
                          selectedMember[item]
                            ? selectedMember[item]
                            : $t("error.noValue")
                        }}
                      </template>
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`form.${item}`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>

              <h5 class="q-mb-sm q-mt-md">
                {{ $t("adminTools.memberDates") }}
              </h5>
              <q-list bordered padding class="rounded-borders">
                <q-item
                  v-for="item in [
                    'lastInduction',
                    'registrationDate',
                    'lastUpdatedProfile',
                    'lastSeen',
                  ]"
                  :key="item"
                >
                  <q-item-section>
                    <q-item-label lines="1">
                      <template v-if="item === 'registrationDate'">
                        {{
                          selectedMember[item]
                            ? selectedMember[item]
                            : $t("error.noValue")
                        }}
                      </template>
                      <template v-else>
                        {{
                          selectedMember[item]
                            ? selectedMember[item]
                            : $t("error.noValue")
                        }}
                      </template>
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.${item}`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel name="access">
          <p class="text-center q-mb-none q-mt-sm">
            {{ $t("adminTools.accessDescription") }}
          </p>
          <access-list :member-id="selectedMemberFiltered.id" />
        </q-tab-panel>

        <q-tab-panel name="log"> Coming Soon! </q-tab-panel>

        <q-tab-panel name="billing">
          <div class="text-h6">
            {{ $t("adminTools.subscriptionInfo") }}
          </div>

          <q-list
            v-if="billing.subscription"
            bordered
            padding
            class="rounded-borders"
          >
            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{ billing.subscription.status }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.subscriptionStatus`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{
                    this.formatDateSimple(
                      billing.subscription.billingCycleAnchor
                    )
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.billingCycleAnchor`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{ this.formatDateSimple(billing.subscription.startDate) }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.startDate`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{
                    this.formatDateSimple(billing.subscription.currentPeriodEnd)
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.currentPeriodEnd`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{ this.formatDateSimple(billing.subscription.cancelAt) }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.cancelAt`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{ billing.subscription.cancelAtPeriodEnd }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`adminTools.cancelAtPeriodEnd`) }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>

          <div v-else>
            {{ $t(`adminTools.noSubscription`) }}
          </div>

          <br />
          <div class="text-h6">
            {{ $t("adminTools.billingInfo") }}
          </div>

          <q-list bordered padding class="rounded-borders">
            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{
                    billing.memberbucks.lastPurchase
                      ? this.formatWhen(billing.memberbucks.lastPurchase)
                      : $t("error.noValue")
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`memberbucks.lastPurchase`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{
                    billing.memberbucks.stripe_card_expiry
                      ? this.formatWhen(billing.memberbucks.lastPurchase)
                      : $t("error.noValue")
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`memberbucks.cardExpiry`) }}
                </q-item-label>
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section>
                <q-item-label lines="1">
                  {{
                    billing.memberbucks.stripe_card_last_digits
                      ? this.formatWhen(billing.memberbucks.lastPurchase)
                      : $t("error.noValue")
                  }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t(`memberbucks.last4`) }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>

          <br />
          <div class="text-h6">
            {{ $t("adminTools.memberbucksTransactions") }}
          </div>

          <q-table
            :rows="this.billing.memberbucks.transactions"
            :columns="[
              {
                name: 'description',
                label: 'Description',
                field: 'description',
                sortable: true,
              },
              {
                name: 'amount',
                label: 'Amount',
                field: 'amount',
                sortable: true,
              },
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
              <div class="row">
                <q-input
                  v-if="$q.screen.xs"
                  v-model="filter"
                  outlined
                  dense
                  debounce="300"
                  placeholder="Search"
                  style="margin-top: -3px"
                >
                  <template v-slot:append>
                    <q-icon :name="icons.search" />
                  </template>
                </q-input>
              </div>
              <div class="row">
                {{ $t("memberbucks.currentBalance") }}
                {{ $n(billing.memberbucks.balance || 0, "currency") }}
              </div>
            </template>

            <template v-if="$q.screen.gt.xs" v-slot:top-right>
              <q-input
                v-model="filter"
                outlined
                dense
                debounce="300"
                placeholder="Search"
                style="margin-top: -3px"
              >
                <template v-slot:append>
                  <q-icon :name="icons.search" />
                </template>
              </q-input>
            </template>

            <template v-slot:body-cell-amount="props">
              <q-td>
                <div
                  :class="{ credit: props.value > 0, debit: props.value < 0 }"
                >
                  ${{ props.value }}
                </div>
              </q-td>
            </template>
          </q-table>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </div>
</template>

<script>
import AccessList from "components/AccessList";
import formMixin from "src/mixins/formMixin";
import SavedNotification from "components/SavedNotification";
import { mapGetters } from "vuex";
import icons from "../../icons";
import formatMixin from "src/mixins/formatMixin";

export default {
  name: "ManageMember",
  components: { AccessList, SavedNotification },
  mixins: [formMixin, formatMixin],
  props: {
    member: {
      type: Object,
      default: () => {
        {
        }
      },
    },
    members: {
      type: Array,
      default: () => {
        [];
      },
    },
  },
  data() {
    return {
      stateLoading: false,
      welcomeLoading: false,
      tab: "profile",
      access: {},
      profileForm: {
        email: "",
        rfidCard: "",
        firstName: "",
        lastName: "",
        phone: "",
        screenName: "",
        memberType: "",
      },
      saved: {
        // if there was an error saving the form
        error: false,

        email: false,
        rfidCard: false,
        firstName: false,
        lastName: false,
        phone: false,
        screenName: false,
        memberType: false,
      },
      billing: {
        memberbucks: {
          transactions: [],
          balance: 0,
        },
        subscription: {
          billingCycleAnchor: "",
          cancelAt: "",
          cancelAtPeriodEnd: "",
          currentPeriodEnd: "",
          startDate: "",
          status: "",
        },
      },
      filter: "",
      loading: false,
      pagination: {
        sortBy: "date",
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 12,
      },
    };
  },
  beforeMount() {
    this.loadInitialForm();
    this.getMemberBilling();
  },
  methods: {
    loadInitialForm() {
      this.profileForm.email = this.selectedMember.email;
      this.profileForm.rfidCard = this.selectedMember.rfid;
      this.profileForm.firstName = this.selectedMember.name.first;
      this.profileForm.lastName = this.selectedMember.name.last;
      this.profileForm.phone = this.selectedMember.phone;
      this.profileForm.screenName = this.selectedMember.screenName;
      this.profileForm.memberType = this.selectedMember.memberType;
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false).then((result) => {
          if (result) {
            this.$axios
              .put(
                `/api/admin/members/${this.member.id}/profile/`,
                this.profileForm
              )
              .then(() => {
                this.saved.error = false;
                this.saved[field] = true;
                this.$emit("memberUpdated");
              })
              .catch(() => {
                this.saved.error = true;
                this.saved[field] = true;
              });
          }
        });
      });
    },
    sendWelcomeEmail() {
      this.welcomeLoading = true;
      this.$axios
        .post(`/api/admin/members/${this.member.id}/sendwelcome/`)
        .then(() => {
          this.$q.dialog({
            title: this.$t("success"),
            message: this.$t("adminTools.sendWelcomeEmailSuccess"),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        })
        .finally(() => {
          this.welcomeLoading = false;
        });
    },
    createInvoice() {
      let emailInvoice = false;
      this.$q
        .dialog({
          title: this.$t("confirmAction"),
          message: this.$t("adminTools.confirmInvoice"),
          ok: "Ok",
          cancel: "Cancel",
        })
        .onOk(() => {
          this.$q
            .dialog({
              title: this.$t("confirmAction"),
              message: this.$t("adminTools.confirmInvoiceEmail"),
              ok: "Email Them",
              cancel: "Don't Email",
            })
            .onOk(() => {
              emailInvoice = true;
            })
            .onDismiss(() => {
              this.$axios
                .post(
                  `/api/admin/members/${this.member.id}/invoice/${emailInvoice}/`
                )
                .then(() => {
                  this.$q.dialog({
                    title: this.$t("success"),
                    message: this.$t("adminTools.createInvoiceSuccess"),
                  });
                  this.$emit("memberUpdated");
                })
                .catch(() => {
                  this.$q.dialog({
                    title: this.$t("error.error"),
                    message: this.$t("error.requestFailed"),
                  });
                });
            });
        });
    },
    getMemberBilling() {
      this.$axios
        .get(`/api/admin/members/${this.member.id}/billing/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        })
        .then((res) => {
          this.billing = res.data;
          if (!this.billing?.subscription) this.billing.subscription = null;
        })
        .finally(() => {
          this.$emit("memberUpdated");
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
    setMemberState(state) {
      this.stateLoading = true;
      this.$axios
        .post(`/api/admin/members/${this.member.id}/state/${state}/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        })
        .finally(() => {
          this.$emit("memberUpdated");
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
    activateMember() {
      this.stateLoading = true;
      this.$axios
        .post(`/api/admin/members/${this.member.id}/makemember/`)
        .then((response) => {
          if (response.data.success) {
            this.$q.dialog({
              title: this.$t("adminTools.makeMemberSuccess"),
              message: this.$t("adminTools.makeMemberSuccessDescription"),
            });
          } else {
            this.$q.dialog({
              title: this.$t("error.error"),
              message: this.$t(response.data.message),
            });
          }
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t("error.error"),
            message: this.$t("error.requestFailed"),
          });
        })
        .finally(() => {
          this.$emit("memberUpdated");
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
  },
  computed: {
    ...mapGetters("config", ["memberTypes"]),
    selectedMember() {
      if (this.members) {
        return this.members.find((e) => e.id === this.member.id);
      }
      return this.member;
    },
    selectedMemberFiltered() {
      const newMember = { ...this.selectedMember };
      delete newMember.access;
      return newMember;
    },
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="scss" scoped>
.q-card {
  max-width: 100%;
}

a,
a:visited,
a:hover,
a:active {
  color: inherit;
  text-decoration: none;
}
</style>
