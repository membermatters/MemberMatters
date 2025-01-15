<template>
  <div class="">
    <h3 class="q-mt-none q-mb-md">
      {{ profileForm.firstName }} {{ profileForm.lastName }} ({{
        profileForm.screenName
      }})
    </h3>
    <q-card
      class="q-mb-none"
      style="background-color: transparent"
      :class="{ 'q-pb-lg': $q.screen.xs }"
    >
      <q-tabs
        v-model="tab"
        align="justify"
        narrow-indicator
        class="bg-primary text-white"
      >
        <q-tab name="profile" :label="$t('menuLink.profile')" />
        <q-tab name="access" :label="$t('adminTools.access')" />
        <q-tab name="billing" :label="$t('adminTools.billing')" />
        <q-tab name="log" :label="$t('adminTools.log')" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="profile" class="q-px-lg q-py-lg">
          <div
            class="row justify-start q-pt-sm"
            :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
          >
            <q-btn
              v-if="selectedMember.state === 'inactive'"
              class="q-mr-sm q-mb-sm"
              color="positive"
              :label="$t('adminTools.enableAccess')"
              :loading="stateLoading"
              @click="setMemberState('active')"
            />
            <q-btn
              v-else-if="
                selectedMember.state === 'noob' ||
                selectedMember.state === 'accountonly'
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
              class="q-mr-sm q-mb-sm"
              color="primary"
              :label="$t('adminTools.title')"
            >
              <q-list>
                <q-item v-close-popup clickable @click="sendWelcomeEmail">
                  <q-item-section>
                    <q-item-label
                      >{{ $t('adminTools.sendWelcomeEmail') }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <!-- Opt out of email exports -->
                <q-item
                  v-if="!selectedMember.excludeFromEmailExport"
                  v-close-popup
                  clickable
                  @click="optOutEmailExport"
                >
                  <q-item-section>
                    <q-item-label
                      >{{ $t('adminTools.optOutEmailExport') }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <!-- Opt in to email exports -->
                <q-item
                  v-if="selectedMember.excludeFromEmailExport"
                  v-close-popup
                  clickable
                  @click="optOutEmailExport"
                >
                  <q-item-section>
                    <q-item-label
                      >{{ $t('adminTools.optInEmailExport') }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <!-- Open the send sms modal -->
                <q-item
                  v-if="features.sms.enable"
                  :disable="profileForm.phone"
                  v-close-popup
                  clickable
                  @click="openSmsModal"
                >
                  <q-item-section>
                    <q-item-label>{{ $t('adminTools.sendSms') }}</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>

          <div class="row q-pt-md">
            <div
              class="col-12 col-md-6"
              :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
            >
              <q-form ref="formRef">
                <h5 class="q-my-sm">
                  {{ $t('adminTools.mainProfile') }}
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
                  @update:model-value="saveChange('email')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.email"
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
                  @update:model-value="saveChange('rfidCard')"
                >
                  <template v-slot:append>
                    <saved-notification
                      :success="saved.rfidCard"
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
                  @update:model-value="saveChange('firstName')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.firstName"
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
                  @update:model-value="saveChange('lastName')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.lastName"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.phone"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.mobile')"
                  :rules="[
                    (val) =>
                      validateNotEmpty(val) || $t('validation.invalidPhone'),
                  ]"
                  @update:model-value="saveChange('phone')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.phone"
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
                  @update:model-value="saveChange('screenName')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.screenName"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-if="
                    features?.signup?.collectVehicleRegistrationPlate ||
                    profileForm.vehicleRegistrationPlate
                  "
                  v-model="profileForm.vehicleRegistrationPlate"
                  :disable="!features?.signup?.collectVehicleRegistrationPlate"
                  outlined
                  :debounce="debounceLength"
                  :label="$t('form.vehicleRegistrationPlate')"
                  :rules="[
                    (val) => validateMax30(val) || $t('validation.max30'),
                  ]"
                  @update:model-value="saveChange('vehicleRegistrationPlate')"
                >
                  <template #append>
                    <saved-notification
                      :success="saved.vehicleRegistrationPlate"
                      :error="saved.error"
                    />
                  </template>
                </q-input>
              </q-form>
            </div>

            <div
              class="col-12 col-md-6"
              :class="{ 'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs }"
            >
              <h5 class="q-my-sm">
                {{ $t('adminTools.otherAttributes') }}
              </h5>

              <q-list bordered padding class="rounded-borders">
                <q-item>
                  <q-item-section>
                    <q-item-label
                      :class="{
                        inactive: selectedMember.state === 'inactive',
                        active: selectedMember.state === 'active',
                        cancelling: ['accountonly', 'noob'].includes(
                          selectedMember.state
                        ),
                      }"
                    >
                      {{
                        $t(
                          `adminTools.memberStatusString.${selectedMember.state}`
                        )
                      }}
                    </q-item-label>

                    <q-item-label caption>
                      {{ $t('adminTools.memberState') }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item key="excludeFromEmailExport">
                  <q-item-section>
                    <q-item-label
                      >{{
                        formatBooleanYesNo(
                          selectedMember.excludeFromEmailExport
                        )
                      }}
                    </q-item-label>

                    <q-item-label caption>
                      {{ $t(`form.excludeFromEmailExport`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item v-for="item in ['id']" :key="item">
                  <q-item-section>
                    <q-item-label
                      >{{
                        selectedMember[item as keyof MemberProfile] != null ||
                        selectedMember[item as keyof MemberProfile] != undefined
                          ? selectedMember[item as keyof MemberProfile]
                          : $t('error.noValue')
                      }}
                    </q-item-label>

                    <q-item-label caption>
                      {{ $t(`form.${item}`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item v-if="features.enableDocusealMemberDocs">
                  <q-item-section>
                    <q-item-label>
                      <a :href="selectedMember.memberdocsLink" target="_blank">
                        <div v-if="selectedMember.lastInduction">Complete</div>
                        <div v-else>Incomplete</div>
                      </a>
                    </q-item-label>

                    <q-item-label caption>
                      {{ $t(`form.memberDocLink`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
                
              </q-list>

              <h5 class="q-mt-md q-mb-sm">
                {{ $t('menuLink.memberbucks') }}
              </h5>
              <q-list bordered padding class="rounded-borders">
                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{
                        $n(
                          selectedMember.memberBucks.balance || 0,
                          'currency',
                          siteLocaleCurrency
                        )
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
                          ? formatDate(selectedMember.memberBucks.lastPurchase)
                          : $t('error.noValue')
                      }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`memberbucks.lastPurchase`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>

              <h5 class="q-mb-sm q-mt-md">
                {{ $t('adminTools.memberDates') }}
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
                            ? formatDate(selectedMember[item])
                            : $t('error.noValue')
                        }}
                      </template>
                      <template v-else>
                        {{
                          selectedMember[item as keyof MemberProfile]
                            ? formatDate(
                                selectedMember[item as keyof MemberProfile]
                              )
                            : $t('error.noValue')
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
          <div class="column q-gutter-y-sm full-width">
            <h6 class="q-mt-md q-mb-sm">
              {{ $t('adminTools.accessDescription') }}
            </h6>

            <access-list
              :member-id="selectedMemberFiltered.id"
              :inactive-warning="selectedMemberFiltered.state === 'inactive'"
            />
          </div>
        </q-tab-panel>

        <q-tab-panel name="billing">
          <div class="column flex content-start items-start q-gutter-y-lg">
            <div class="column q-gutter-y-sm full-width">
              <div class="text-h6">
                {{ $t('adminTools.subscriptionInfo') }}
              </div>

              <q-markup-table
                v-if="billing?.subscription"
                bordered
                padding
                class="rounded-borders desktop-only"
              >
                <thead>
                  <tr>
                    <th class="text-left">
                      {{ $t(`adminTools.membershipTier`) }}
                    </th>
                    <th class="text-left">
                      {{ $t(`adminTools.billingPlan`) }}
                    </th>
                    <th class="text-left">
                      {{ $t(`adminTools.billingCycleAnchor`) }}
                    </th>
                    <th class="text-left">{{ $t(`adminTools.startDate`) }}</th>
                    <th class="text-left">
                      {{ $t(`adminTools.currentPeriodEnd`) }}
                    </th>
                    <template v-if="billing.subscription.cancelAt">
                      <th class="text-left">
                        {{ $t(`adminTools.cancelAt`) }}
                      </th>
                      <th class="text-left">
                        {{ $t(`adminTools.cancelAtPeriodEnd`) }}
                      </th>
                    </template>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="text-left">
                      <router-link
                        :to="{
                          name: 'manageTier',
                          params: {
                            planId: billing.subscription.membershipPlan.id,
                          },
                        }"
                        >{{
                          billing.subscription.membershipTier.name
                        }}</router-link
                      >
                    </td>
                    <td class="text-left">
                      {{
                        $t('paymentPlans.intervalDescription', {
                          currency:
                            billing.subscription.membershipPlan.currency.toUpperCase(),
                          amount: $n(
                            billing.subscription.membershipPlan.cost / 100,
                            'currency',
                            siteLocaleCurrency
                          ),
                          interval: $tc(
                            `paymentPlans.interval.${billing.subscription.membershipPlan.interval.toLowerCase()}`,
                            billing.subscription.membershipPlan.intervalAmount
                          ),
                        })
                      }}
                    </td>
                    <td class="text-left">
                      {{ formatDate(billing.subscription.billingCycleAnchor) }}
                    </td>
                    <td class="text-left">
                      {{ formatDate(billing.subscription.startDate) }}
                    </td>
                    <td class="text-left">
                      {{ formatDate(billing.subscription.currentPeriodEnd) }}
                    </td>
                    <template v-if="billing.subscription.cancelAt">
                      <td class="text-left">
                        {{ formatDate(billing.subscription.cancelAt) }}
                      </td>
                      <td class="text-left">
                        {{
                          formatBooleanYesNo(
                            billing.subscription.cancelAtPeriodEnd
                          )
                        }}
                      </td>
                    </template>
                  </tr>
                </tbody>
              </q-markup-table>

              <q-list
                v-if="billing?.subscription"
                bordered
                padding
                class="rounded-borders desktop-hide"
                style="max-width: 350px"
              >
                <q-item>
                  <q-item-section>
                    <q-item-label
                      lines="1"
                      :class="{
                        inactive: billing.subscription.status === 'inactive',
                        active: billing.subscription.status === 'active',
                        cancelling:
                          billing.subscription.status === 'cancelling',
                      }"
                    >
                      {{
                        $t(
                          `adminTools.subscriptionStatusString.${billing.subscription.status}`
                        )
                      }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.subscriptionStatus`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{ formatDate(billing.subscription.billingCycleAnchor) }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.billingCycleAnchor`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{ formatDate(billing.subscription.startDate) }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.startDate`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      {{ formatDate(billing.subscription.currentPeriodEnd) }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.currentPeriodEnd`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item v-if="billing.subscription.cancelAt">
                  <q-item-section>
                    <q-item-label lines="1">
                      {{ formatDate(billing.subscription.cancelAt) }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`adminTools.cancelAt`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>

                <q-item v-if="billing.subscription.cancelAtPeriodEnd">
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
            </div>

            <div class="column q-gutter-y-sm full-width">
              <div class="text-h6">
                {{ $t('adminTools.billingInfo') }}
              </div>

              <q-markup-table
                v-if="billing?.subscription"
                bordered
                padding
                class="rounded-borders desktop-only"
              >
                <thead>
                  <tr>
                    <th class="text-left">
                      {{ $t(`memberbucks.lastPurchase`) }}
                    </th>
                    <th class="text-left">
                      {{ $t(`memberbucks.cardExpiry`) }}
                    </th>
                    <th class="text-left">{{ $t(`memberbucks.last4`) }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="text-left">
                      <div v-if="billing?.memberbucks.lastPurchase">
                        {{ this.formatWhen(billing?.memberbucks.lastPurchase) }}
                        <q-tooltip :delay="500">
                          {{
                            this.formatDate(billing?.memberbucks.lastPurchase)
                          }}
                        </q-tooltip>
                      </div>
                      <div v-else>
                        {{ $t('error.noValue') }}
                      </div>
                    </td>
                    <td class="text-left">
                      {{
                        billing?.memberbucks.stripe_card_expiry ||
                        $t('error.noValue')
                      }}
                    </td>
                    <td class="text-left">
                      {{
                        billing?.memberbucks.stripe_card_last_digits ||
                        $t('error.noValue')
                      }}
                    </td>
                  </tr>
                </tbody>
              </q-markup-table>

              <q-list
                bordered
                padding
                class="rounded-borders mobile-only"
                style="max-width: 350px"
              >
                <q-item>
                  <q-item-section>
                    <q-item-label lines="1">
                      <div v-if="billing?.memberbucks.lastPurchase">
                        {{ this.formatWhen(billing?.memberbucks.lastPurchase) }}
                        <q-tooltip :delay="500">
                          {{
                            this.formatDate(billing?.memberbucks.lastPurchase)
                          }}
                        </q-tooltip>
                      </div>
                      <div v-else>
                        {{ $t('error.noValue') }}
                      </div>
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
                        billing?.memberbucks.stripe_card_expiry ||
                        $t('error.noValue')
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
                        billing?.memberbucks.stripe_card_last_digits ||
                        $t('error.noValue')
                      }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`memberbucks.last4`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>

            <div class="column q-gutter-y-sm full-width">
              <div class="text-h6">
                {{ $t('adminTools.memberbucksTransactions') }}
              </div>

              <q-table
                :rows="billing?.memberbucks.transactions"
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
                    format: (val) => formatWhen(val),
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
                    {{ $t('memberbucks.currentBalance') }}
                    {{
                      $n(
                        billing?.memberbucks.balance || 0,
                        'currency',
                        siteLocaleCurrency
                      )
                    }}
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
                      :class="{
                        credit: props.value > 0,
                        debit: props.value < 0,
                      }"
                    >
                      ${{ props.value }}
                    </div>
                  </q-td>
                </template>
              </q-table>
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel name="log">
          <div class="text-h6 q-pb-sm">
            {{ $t('adminTools.userEvents') }}
          </div>

          <q-table
            :rows="logs.userEventLogs"
            :columns="[
              {
                name: 'logtype',
                label: 'Log Type',
                field: 'logtype',
                sortable: true,
              },
              {
                name: 'description',
                label: 'Description',
                field: 'description',
                sortable: true,
              },
              {
                name: 'date',
                label: 'Date',
                field: 'date',
                sortable: true,
              },
            ]"
            row-key="id"
            :filter="userEventsFilter"
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

            <template v-slot:item="props">
              <div
                class="q-pa-sm col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
              >
                <q-card class="q-py-sm">
                  <q-list dense>
                    <q-item
                      v-for="col in props.cols.filter(
                        (col) => col.name !== 'desc'
                      )"
                      :key="col.name"
                    >
                      <q-item-section>
                        <q-item-label>{{ col.label }}</q-item-label>
                      </q-item-section>
                      <q-item-section side>
                        <q-item-label caption>
                          <template v-if="col.name === 'date'">
                            <div>
                              {{ this.formatWhen(col.value) }}
                              <q-tooltip :delay="500">
                                {{ this.formatDate(col.value) }}
                              </q-tooltip>
                            </div>
                          </template>

                          <template v-else>
                            {{ col.value }}
                          </template>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <template v-if="col.name === 'date'">
                    <div>
                      {{ this.formatWhen(col.value) }}
                      <q-tooltip :delay="500">
                        {{ this.formatDate(col.value) }}
                      </q-tooltip>
                    </div>
                  </template>

                  <template v-else>
                    {{ col.value }}
                  </template>
                </q-td>
              </q-tr>
            </template>
          </q-table>

          <div class="text-h6 q-pb-sm subheading">
            {{ $t('adminTools.userDoorLogs') }}
          </div>

          <q-table
            :rows="logs.doorLogs"
            :columns="[
              {
                name: 'door',
                label: 'Door Name',
                field: 'door',
                sortable: true,
              },
              {
                name: 'success',
                label: 'Swipe Status',
                field: 'success',
                sortable: true,
              },
              {
                name: 'date',
                label: 'Date',
                field: 'date',
                sortable: true,
              },
            ]"
            row-key="id"
            :filter="doorFilter"
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

            <template v-slot:item="props">
              <div
                class="q-pa-sm col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
              >
                <q-card class="q-py-sm">
                  <q-list dense>
                    <q-item
                      v-for="col in props.cols.filter(
                        (col) => col.name !== 'desc'
                      )"
                      :key="col.name"
                    >
                      <q-item-section>
                        <q-item-label>{{ col.label }}</q-item-label>
                      </q-item-section>
                      <q-item-section side>
                        <q-item-label caption>
                          <template v-if="col.name === 'date'">
                            <div>
                              {{ this.formatWhen(col.value) }}
                              <q-tooltip :delay="500">
                                {{ this.formatDate(col.value) }}
                              </q-tooltip>
                            </div>
                          </template>

                          <template v-else-if="col.name === 'success'">
                            <div
                              :class="
                                col.value ? 'text-positive' : 'text-negative'
                              "
                            >
                              {{ $t(col.value ? 'success' : 'rejected') }}
                            </div>
                          </template>

                          <template v-else>
                            {{ col.value }}
                          </template>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <template v-if="col.name === 'date'">
                    <div>
                      {{ this.formatWhen(col.value) }}
                      <q-tooltip :delay="500">
                        {{ this.formatDate(col.value) }}
                      </q-tooltip>
                    </div>
                  </template>

                  <template v-else-if="col.name === 'success'">
                    <div :class="col.value ? 'text-positive' : 'text-negative'">
                      {{ $t(col.value ? 'success' : 'rejected') }}
                    </div>
                  </template>

                  <template v-else>
                    {{ col.value }}
                  </template>
                </q-td>
              </q-tr>
            </template>
          </q-table>

          <div class="text-h6 q-pb-sm subheading">
            {{ $t('adminTools.userInterlockLogs') }}
          </div>

          <q-table
            :rows="logs.interlockLogs"
            :columns="[
              {
                name: 'interlock',
                label: 'Interlock',
                field: 'interlockName',
                sortable: true,
              },
              {
                name: 'dateStarted',
                label: 'Date',
                field: 'dateStarted',
                sortable: true,
              },
              {
                name: 'totalTime',
                label: 'Total Time',
                field: 'totalTime',
                sortable: true,
                sort: sortByFloat,
              },
              {
                name: 'totalCost',
                label: 'Total Cost',
                field: 'totalCost',
                sortable: true,
                sort: sortByFloat,
                format: (val) => $n(val || 0, 'currency', siteLocaleCurrency),
              },
              {
                name: 'userEnded',
                label: 'Swiped Off By',
                field: 'userEnded',
                sortable: true,
              },
              {
                name: 'status',
                label: 'Status',
                field: 'status',
                sortable: true,
              },
            ]"
            row-key="id"
            :filter="doorFilter"
            :pagination="{
              ...pagination,
              sortBy: 'dateStarted',
            }"
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

            <template v-slot:item="props">
              <div
                class="q-pa-sm col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition"
              >
                <q-card class="q-py-sm">
                  <q-list dense>
                    <q-item
                      v-for="col in props.cols.filter(
                        (col) => col.name !== 'desc'
                      )"
                      :key="col.name"
                    >
                      <q-item-section>
                        <q-item-label>{{ col.label }}</q-item-label>
                      </q-item-section>
                      <q-item-section side>
                        <q-item-label caption>
                          <template v-if="col.name === 'dateStarted'">
                            <div>
                              {{ this.formatWhen(col.value) }}
                              <q-tooltip :delay="500">
                                {{ this.formatDate(col.value) }}
                              </q-tooltip>
                            </div>
                          </template>

                          <template v-else-if="col.name === 'totalTime'">
                            <div v-if="col.value > 1">
                              {{ this.humanizeDurationOfSeconds(col.value) }}
                              <q-tooltip :delay="500">
                                {{
                                  this.humanizeDurationOfSecondsPrecise(
                                    col.value
                                  )
                                }}
                              </q-tooltip>
                            </div>
                            <div v-else></div>
                          </template>

                          <template v-else-if="col.name === 'status'">
                            <div class="text-negative" v-if="col.value === -1">
                              {{ $t('rejected') }}
                            </div>
                            <div
                              class="text-positive"
                              v-else-if="col.value === 1"
                            >
                              {{ $t('interlocks.finished') }}
                            </div>
                            <div class="text-warning" v-else>
                              {{ $t('interlocks.inProgress') }}
                              <q-spinner-dots></q-spinner-dots>
                            </div>
                          </template>

                          <template v-else>
                            {{ col.value }}
                          </template>
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-card>
              </div>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <template v-if="col.name === 'dateStarted'">
                    <div>
                      {{ this.formatWhen(col.value) }}
                      <q-tooltip :delay="500">
                        {{ this.formatDate(col.value) }}
                      </q-tooltip>
                    </div>
                  </template>

                  <template v-else-if="col.name === 'totalTime'">
                    <div v-if="col.value > 1">
                      {{ this.humanizeDurationOfSeconds(col.value) }}
                      <q-tooltip :delay="500">
                        {{ this.humanizeDurationOfSecondsPrecise(col.value) }}
                      </q-tooltip>
                    </div>
                    <div v-else></div>
                  </template>

                  <template v-else-if="col.name === 'status'">
                    <div class="text-negative" v-if="col.value === -1">
                      {{ $t('rejected') }}
                    </div>
                    <div class="text-positive" v-else-if="col.value === 1">
                      {{ $t('interlocks.finished') }}
                    </div>
                    <div class="text-warning" v-else>
                      {{ $t('interlocks.inProgress') }}
                      <q-spinner-dots></q-spinner-dots>
                    </div>
                  </template>

                  <template v-else>
                    {{ col.value }}
                  </template>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
    <q-dialog v-model="smsModalIsOpen">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{
              $t('adminTools.sendSmsModalTitle', {
                name: `${profileForm.firstName} ${profileForm.lastName}`,
              })
            }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="smsBody"
            autofocus
            :maxlength="320"
            counter
            type="textarea"
            :placeholder="$t('adminTools.smsContentPlaceholder')"
            outlined
            :debounce="debounceLength"
            :label="$t('adminTools.smsContentTitle')"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
          >
          </q-input>
        </q-card-section>

        <q-card-section>
          <div class="text-h6">
            {{
              $t('adminTools.sendSmsModalPreviewTitle', {
                name: `${profileForm.firstName} ${profileForm.lastName}`,
              })
            }}
          </div>
          <div class="text-body">
            {{
              $t('adminTools.smsCostEstimate', {
                cost: smsCost,
              })
            }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div class="q-pa-md row justify-center">
            <div style="width: 100%; max-width: 400px">
              <q-chat-message
                :text="[
                  (smsBody.length
                    ? $t('adminTools.smsOneWayBody', { message: smsBody })
                    : $t('adminTools.smsOneWayBody', {
                        message: $t('adminTools.smsContentPlaceholder'),
                      })) +
                    ' ' +
                    features.sms.footer,
                ]"
                sent
                :name="features.sms.senderId"
              />
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            flat
            :label="$t('button.cancel')"
            :disable="smsSendLoading"
            @click="resetSmsModal"
          />
          <q-btn
            color="primary"
            :label="$t('button.send')"
            :loading="smsSendLoading"
            :disable="smsSendLoading"
            type="submit"
            @click="submitSmsModal"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import AccessList from '@components/AccessList.vue';
import formMixin from '@mixins/formMixin';
import SavedNotification from '@components/SavedNotification.vue';
import icons from '../../icons';
import formatMixin from '@mixins/formatMixin';
import { mapGetters } from 'vuex';
import { QForm } from 'quasar';
import { MemberBillingInfo, MemberProfile, MemberState } from 'types/member';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ManageMember',
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
      tab: 'profile',
      access: {},
      profileForm: {
        email: '',
        rfidCard: '',
        firstName: '',
        lastName: '',
        phone: '',
        screenName: '',
        vehicleRegistrationPlate: '',
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
        vehicleRegistrationPlate: false,
      },
      billing: null as MemberBillingInfo | null,
      logs: {
        userEventLogs: [],
        doorLogs: [],
        interlockLogs: [],
      },
      filter: '',
      userEventsFilter: '',
      doorFilter: '',
      interlockFiler: '',
      loading: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 3 : 5,
      },
      smsSendLoading: false,
      smsModalIsOpen: false,
      smsBody: '',
    };
  },
  beforeMount() {
    this.loadInitialForm();
    this.getMemberBilling();
    this.getMemberLogs();
  },
  methods: {
    loadInitialForm() {
      this.profileForm.email = this.selectedMember.email;
      this.profileForm.rfidCard = this.selectedMember.rfid;
      this.profileForm.firstName = this.selectedMember.name.first;
      this.profileForm.lastName = this.selectedMember.name.last;
      this.profileForm.phone = this.selectedMember.phone;
      this.profileForm.screenName = this.selectedMember.screenName;
      this.profileForm.vehicleRegistrationPlate =
        this.selectedMember.vehicleRegistrationPlate;
    },
    saveChange(field: keyof typeof this.saved) {
      const formRef = this.$refs.formRef as typeof QForm;
      formRef.validate(false).then(() => {
        formRef.validate(false).then((result: boolean) => {
          if (result) {
            this.$axios
              .put(`/api/admin/members/${this.member.id}/profile/`, {
                ...this.profileForm,
                excludeFromEmailExport:
                  this.selectedMember.excludeFromEmailExport,
              })
              .then(() => {
                this.saved.error = false;
                this.saved[field as keyof typeof this.saved] = true;
                this.$emit('memberUpdated');
                setTimeout(() => {
                  this.saved[field as keyof typeof this.saved] = false;
                }, 1500);
              })
              .catch(() => {
                this.saved.error = true;
                this.saved[field as keyof typeof this.saved] = true;
                setTimeout(() => {
                  this.saved[field as keyof typeof this.saved] = false;
                  this.saved.error = false;
                }, 1500);
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
            title: this.$t('actionSuccess'),
            message: this.$t('adminTools.sendWelcomeEmailSuccess'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.welcomeLoading = false;
        });
    },
    getMemberBilling() {
      this.$axios
        .get(`/api/admin/members/${this.member.id}/billing/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .then((res) => {
          if (!res) return;
          this.billing = res.data;
          if (this.billing && !this.billing?.subscription)
            this.billing.subscription = null;
        })
        .finally(() => {
          this.$emit('memberUpdated');
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
    getMemberLogs() {
      this.$axios
        .get(`/api/admin/members/${this.member.id}/logs/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .then((res) => {
          if (!res) return;
          this.logs = res.data;
        })
        .finally(() => {
          this.$emit('memberUpdated');
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
    setMemberState(state: MemberState) {
      this.stateLoading = true;
      this.$axios
        .post(`/api/admin/members/${this.member.id}/state/${state}/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('memberUpdated');
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
              title: this.$t('adminTools.makeMemberSuccess'),
              message: this.$t('adminTools.makeMemberSuccessDescription'),
            });
          } else {
            this.$q.dialog({
              title: this.$t('error.error'),
              message: this.$t(response.data.message),
            });
          }
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('memberUpdated');
          setTimeout(() => {
            this.stateLoading = false;
          }, 1200);
        });
    },
    optOutEmailExport() {
      this.$axios
        .put(`/api/admin/members/${this.member.id}/profile/`, {
          excludeFromEmailExport: !this.selectedMember.excludeFromEmailExport,
          ...this.profileForm,
        })
        .then(() => {
          this.$emit('memberUpdated');
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        });
    },
    openSmsModal() {
      this.smsModalIsOpen = true;
    },
    resetSmsModal() {
      this.smsModalIsOpen = false;
      this.smsBody = '';
      this.smsSendLoading = false;
    },
    submitSmsModal() {
      this.smsSendLoading = true;
      this.$axios
        .post(`/api/admin/members/${this.member.id}/sendsms/`, {
          smsBody: this.$t('adminTools.smsOneWayBody', {
            message: this.smsBody,
          }),
        })
        .then(() => {
          this.resetSmsModal();
          this.$q.notify({
            message: this.$t('adminTools.sendSmsSuccess', {
              name: `${this.profileForm.firstName} ${this.profileForm.lastName}`,
            }),
            type: 'positive',
          });
        })
        .catch(() => {
          this.smsSendLoading = false;
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('adminTools.sendSmsFail', {
              name: `${this.profileForm.firstName} ${this.profileForm.lastName}`,
            }),
          });
        });
      return;
    },
  },
  computed: {
    ...mapGetters('config', ['siteLocaleCurrency', 'features']),
    selectedMember() {
      if (this.members) {
        return (this.members as MemberProfile[]).find(
          (member) => member.id === this.member.id
        ) as MemberProfile;
      }
      return this.member as MemberProfile;
    },
    selectedMemberFiltered() {
      const newMember = { ...this.selectedMember };
      // eslint-disable-next-line
      // @ts-ignore
      delete newMember.access;
      return newMember;
    },
    icons() {
      return icons;
    },
    smsCost() {
      const smsContainsUnicode = /[^\u0000-\u00ff]/.test(this.smsBody);
      const charsPerSms = smsContainsUnicode ? 70 : 160;
      return Math.ceil(this.smsBody.length / charsPerSms);
    },
  },
});
</script>

<style lang="scss" scoped>
.q-card {
  max-width: 100%;
}

//a,
//a:visited,
//a:hover,
//a:active {
//  color: inherit;
//  text-decoration: none;
//}

.active {
  color: green;
}

.inactive {
  color: red;
}

.cancelling {
  color: orange;
}

.q-field__after,
.q-field__append {
  padding-left: 0;
}

.subheading {
  padding-top: 20px;
}
</style>
