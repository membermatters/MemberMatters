<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <!-- <q-card class="q-dialog-plugin"> -->
    <q-card
      class="q-dialog-plugin"
      style="max-width: 800px; width: 100%; height: 650px"
    >
      <!-- <h3>
      {{ device.name }}
    </h3> -->
      <q-tabs
        v-model="tab"
        align="justify"
        narrow-indicator
        class="bg-primary text-white"
      >
        <q-tab name="manageDevice" :label="$t('menuLink.manageDevice')" />
        <q-tab name="stats" :label="$t('adminTools.stats')" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="manageDevice" class="q-px-lg q-py-lg">
          <q-card-section>
            <q-form ref="formRef">
              <div class="column q-gutter-md q-px-sm">
                <q-input
                  v-model="device.name"
                  outlined
                  :label="$t(`${deviceType}.name`)"
                  :debounce="debounceLength"
                  @update:model-value="saveChange('name')"
                >
                  <template v-slot:append>
                    <saved-notification
                      :success="saved.name"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="device.description"
                  outlined
                  :label="$t(`${deviceType}.description`)"
                  :debounce="debounceLength"
                  @update:model-value="saveChange('description')"
                >
                  <template v-slot:append>
                    <saved-notification
                      :success="saved.description"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  v-model="device.ipAddress"
                  outlined
                  :label="$t('form.ipAddress')"
                  disable
                >
                  <template v-slot:append>
                    <saved-notification
                      :success="saved.ipAddress"
                      show-text
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <div class="column">
                  <div class="row items-center">
                    <q-checkbox
                      v-model="device.defaultAccess"
                      :label="$t('access.defaultAccess')"
                      :debounce="debounceLength"
                      @update:model-value="saveChange('defaultAccess')"
                    />
                    <q-space />
                    <saved-notification
                      :success="saved.defaultAccess"
                      show-text
                      :error="saved.error"
                    />
                  </div>

                  <div class="row items-center">
                    <q-checkbox
                      v-model="device.maintenanceLockout"
                      :label="$t('access.maintenanceLockout')"
                      :debounce="debounceLength"
                      @update:model-value="saveChange('maintenanceLockout')"
                    />
                    <q-space />
                    <saved-notification
                      :success="saved.maintenanceLockout"
                      show-text
                      :error="saved.error"
                    />
                  </div>
                  <div class="row items-center">
                    <q-checkbox
                      v-model="device.playThemeOnSwipe"
                      :label="$t('access.playTheme')"
                      :debounce="debounceLength"
                      @update:model-value="saveChange('playTheme')"
                    />
                    <q-space />
                    <saved-notification
                      :success="saved.playTheme"
                      show-text
                      :error="saved.error"
                    />
                  </div>
                  <div class="row items-center">
                    <q-checkbox
                      v-model="device.exemptFromSignin"
                      :label="$t('access.exemptSignin')"
                      :debounce="debounceLength"
                      @update:model-value="saveChange('exemptSignin')"
                    />
                    <q-space />
                    <saved-notification
                      :success="saved.exemptSignin"
                      show-text
                      :error="saved.error"
                    />
                  </div>
                  <div class="row items-center q-gutter-sm">
                    <q-checkbox
                      v-model="device.hiddenToMembers"
                      :label="$t('access.hiddenToMembers')"
                      :debounce="debounceLength"
                      @update:model-value="saveChange('hiddenToMembers')"
                    />
                    <q-space />
                    <saved-notification
                      :success="saved.hiddenToMembers"
                      show-text
                      :error="saved.error"
                    />
                  </div>
                </div>

                <div class="row">
                  <q-btn
                    :disable="
                      unlockLoading || device.offline || disabled.unlock
                    "
                    :loading="unlockLoading"
                    class="q-mr-sm"
                    size="sm"
                    color="accent"
                    @click.stop="unlockDevice()"
                  >
                    <q-icon :name="icons.unlock" />
                    <q-tooltip>
                      {{ $t('device.unlock') }}
                    </q-tooltip>
                  </q-btn>

                  <q-btn
                    :disable="lockLoading || device.offline || disabled.lock"
                    :loading="lockLoading"
                    class="q-mr-sm"
                    size="sm"
                    color="accent"
                    @click.stop="lockDevice()"
                  >
                    <q-icon :name="icons.lock" />
                    <q-tooltip>
                      {{ $t('device.lock') }}
                    </q-tooltip>
                  </q-btn>

                  <q-btn
                    :disable="
                      rebootLoading || device.offline || disabled.reboot
                    "
                    :loading="rebootLoading"
                    class="q-mr-sm"
                    size="sm"
                    color="accent"
                    @click.stop="rebootDevice()"
                  >
                    <q-icon :name="icons.reboot" />
                    <q-tooltip>
                      {{ $t('device.reboot') }}
                    </q-tooltip>
                  </q-btn>

                  <q-btn
                    :disable="syncLoading || device.offline || disabled.sync"
                    :loading="syncLoading"
                    class="q-mr-sm"
                    size="sm"
                    color="accent"
                    @click.stop="syncDevice()"
                  >
                    <q-icon :name="icons.sync" />
                    <q-tooltip>
                      {{ $t('device.sync') }}
                    </q-tooltip>
                  </q-btn>

                  <q-btn
                    type="reset"
                    class="q-mr-sm"
                    size="sm"
                    color="negative"
                    :loading="removeLoading"
                    :disabled="removeLoading"
                    @click="removeDevice"
                  >
                    <q-icon :name="icons.delete" />
                    <q-tooltip>
                      {{ $t(`device.remove`) }}
                    </q-tooltip>
                  </q-btn>

                  <q-space />
                </div>
              </div>
            </q-form>
          </q-card-section>
        </q-tab-panel>

        <q-tab-panel name="stats">
          <div class="row flex content-start justify-center">
            <q-table
              :rows="device.userStats"
              :columns="columnI18n"
              row-key="key"
              :filter="filter"
              v-model:pagination="devicePagination"
              :dense="$q.screen.lt.md"
              :grid="$q.screen.xs"
              class="table"
              :loading="loading"
              :no-data-label="$t('error.noData')"
              style="width: 90%"
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
            </q-table>
          </div>
        </q-tab-panel>
      </q-tab-panels>

      <q-card-actions align="right" class="row absolute-bottom">
        <div class="q-pr-sm">
          {{ device.name }}
        </div>
        <q-btn
          color="primary"
          label="Previous"
          @click="onPreviousClick"
          :disable="deviceCount < 2"
        />
        <q-btn
          color="primary"
          label="Next"
          @click="onNextClick"
          :disable="deviceCount < 2"
        />
        <q-btn color="primary" label="Close" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import icons from '@icons';
import { mapGetters, mapActions } from 'vuex';
import formMixin from '@mixins/formMixin';
import formatMixin from '@mixins/formatMixin';
import SavedNotification from '@components/SavedNotification.vue';

export default {
  emits: ['ok', 'cancel', 'hide'],
  components: {
    SavedNotification,
  },
  mixins: [formMixin, formatMixin],
  props: {
    deviceId: {
      type: String,
      default: '',
    },
    deviceType: {
      type: String,
      default: '',
    },
    // ...your custom props
  },
  data() {
    return {
      tab: 'manageDevice',
      interval: null,
      removeLoading: false,
      syncLoading: false,
      rebootLoading: false,
      lockLoading: false,
      unlockLoading: false,
      loading: false,
      errorLoading: false,
      updateInterval: null,
      disabled: {
        unlock: false,
        lock: false,
        reboot: false,
        sync: false,
      },
      filter: '',
      devicePagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: this.$q.screen.xs ? 3 : 8,
      },
      saved: {
        // if there was an error saving the form
        error: false,

        name: false,
        description: false,
        ipAddress: false,
        defaultAccess: false,
        maintenanceLockout: false,
        playThemeOnSwipe: false,
        exemptFromSignin: false,
        hiddenToMembers: false,
      },
      device: {
        name: '',
        description: '',
        ipAddress: '',
        defaultAccess: null,
        maintenanceLockout: null,
        playThemeOnSwipe: null,
        exemptFromSignin: null,
        hiddenToMembers: null,
        usage: null,
        stats: [],
      },
      deviceIndex: 1,
    };
  },
  mounted() {
    Promise.allSettled([
      this.getDoors(),
      this.getInterlocks(),
      this.getMemberbucksDevices(),
    ]).then(() => {
      this.initForm();
      if (!this.device.id) this.$router.push({ name: 'Error404' });
    });

    this.interval = setInterval(() => {
      this.getDoors();
      this.getInterlocks();
      this.getMemberbucksDevices();
    }, 30 * 1000);

    // find the device index from the devices list
    if (this.deviceType === 'doors') {
      this.deviceIndex = this.doors.findIndex(
        (item) => String(item.id) === this.deviceId
      );
    } else if (this.deviceType === 'interlocks') {
      this.deviceIndex = this.interlocks.findIndex(
        (item) => String(item.id) === this.deviceId
      );
    } else if (this.deviceType === 'memberbucks-devices') {
      this.disabled = {
        unlock: true,
        lock: true,
        reboot: true,
        sync: true,
      };
      this.deviceIndex = this.memberbucksDevices.findIndex(
        (item) => String(item.id) === this.deviceId
      );
    } else {
      console.error('Invalid device type: ', this.deviceType);
    }
  },
  methods: {
    ...mapActions('adminTools', [
      'getDoors',
      'getInterlocks',
      'getMemberbucksDevices',
    ]),
    ...mapGetters('config', ['siteLocaleCurrency']),
    initForm() {
      if (this.deviceType === 'doors') {
        if (this.deviceIndex === this.doors.length) {
          this.deviceIndex = 0;
        }
        this.device = this.doors[this.deviceIndex];
      } else if (this.deviceType === 'interlocks') {
        if (this.deviceIndex === this.interlocks.length) {
          this.deviceIndex = 0;
        }
        this.device = this.interlocks[this.deviceIndex];
      } else if (this.deviceType === 'memberbucks-devices') {
        if (this.deviceIndex === this.memberbucksDevices.length) {
          this.deviceIndex = 0;
        }
        this.device = this.memberbucksDevices[this.deviceIndex];
      }
    },
    unlockDevice() {
      this.unlockLoading = true;
      this.$axios
        .post(`/api/access/${this.deviceType}/${this.device.id}/unlock/`)
        .then(() => {
          this.$q.notify({
            message: this.$t('device.unlocked'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('device.requestFailed'),
          });
        })
        .finally(() => {
          this.unlockLoading = false;
        });
    },
    lockDevice() {
      this.lockLoading = true;
      this.$axios
        .post(`/api/access/${this.deviceType}/${this.device.id}/lock/`)
        .then(() => {
          this.$q.notify({
            message: this.$t('device.locked'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('device.requestFailed'),
          });
        })
        .finally(() => {
          this.lockLoading = false;
        });
    },
    rebootDevice() {
      this.rebootLoading = true;
      this.$axios
        .post(`/api/access/${this.deviceType}/${this.device.id}/reboot/`)
        .then(() => {
          this.$q.notify({
            message: this.$t('device.rebooted'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('device.requestFailed'),
          });
        })
        .finally(() => {
          this.rebootLoading = false;
        });
    },
    syncDevice() {
      this.syncLoading = true;
      this.$axios
        .post(`/api/access/${this.deviceType}/${this.device.id}/sync/`)
        .then(() => {
          this.$q.notify({
            message: this.$t('device.synced'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('device.requestFailed'),
          });
        })
        .finally(() => {
          this.syncLoading = false;
        });
    },
    removeDevice() {
      this.$q
        .dialog({
          title: this.$t('confirmRemove'),
          ok: 'Ok',
          cancel: 'Cancel',
        })
        .onOk(() => {
          this.removeLoading = true;
          this.$axios
            .delete(`/api/admin/${this.deviceType}/${this.device.id}/`)
            .then(() => {
              this.$router.push({ name: 'devices' });
            })
            .catch((error) => {
              this.removeLoading = true;
              this.$q.dialog({
                title: this.$t('error.error'),
                message: this.$t('error.requestFailed'),
              });
              throw error;
            })
            .finally(() => {
              this.removeLoading = false;
            });
        });
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false).then((result) => {
          if (result) {
            this.$axios
              .put(
                `/api/admin/${this.deviceType}/${this.device.id}/`,
                this.device
              )
              .then(() => {
                this.saved.error = false;
                this.saved[field] = true;
                setTimeout(() => {
                  this.saved[field] = false;
                }, 1500);
              })
              .catch(() => {
                this.initForm();
                this.saved.error = true;
                this.saved[field] = true;
                setTimeout(() => {
                  this.saved[field] = false;
                  this.saved.error = false;
                }, 1500);
              });
          }
        });
      });
    },
    // following method is REQUIRED
    // (don't change its name --> "show")
    show() {
      this.$refs.dialog.show();
    },

    // following method is REQUIRED
    // (don't change its name --> "hide")
    hide() {
      this.$refs.dialog.hide();
    },

    onDialogHide() {
      // required to be emitted
      // when QDialog emits "hide" event
      this.$emit('hide');
    },

    onOKClick() {
      // on OK, it is REQUIRED to
      // emit "ok" event (with optional payload)
      // before hiding the QDialog
      this.$emit('ok');
      // or with payload: this.$emit('ok', { ... })

      // then hiding dialog
      this.hide();
    },

    onNextClick() {
      this.deviceIndex = this.deviceIndex + 1;
      this.initForm();
    },
    onPreviousClick() {
      let newDevice;
      this.deviceIndex = this.deviceIndex - 1;
      if (this.deviceIndex === -1) {
        if (this.deviceType === 'doors') {
          this.deviceIndex += this.doors.length;
        } else if (this.deviceType === 'interlocks') {
          this.deviceIndex += this.interlocks.length;
        } else if (this.deviceType === 'memberbucks-devices') {
          this.deviceIndex += this.memberbucksDevices.length;
        }
      }
      if (this.deviceType === 'doors') {
        newDevice = this.doors[this.deviceIndex];
      } else if (this.deviceType === 'interlocks') {
        newDevice = this.interlocks[this.deviceIndex];
      } else if (this.deviceType === 'memberbucks-devices') {
        newDevice = this.memberbucksDevices[this.deviceIndex];
      }
      this.device = newDevice;
    },
  },
  computed: {
    ...mapGetters('adminTools', ['doors', 'interlocks', 'memberbucksDevices']),
    deviceCount() {
      if (this.deviceType === 'doors') {
        return this.doors.length;
      } else if (this.deviceType === 'interlocks') {
        return this.interlocks.length;
      } else if (this.deviceType === 'memberbucks-devices') {
        return this.memberbucksDevices.length;
      } else return 0;
    },
    columnI18n() {
      let columns = [];
      if (this.deviceType === 'doors') {
        columns = [
          {
            name: 'name',
            label: this.$t('digitalId.fullName'),
            field: 'full_name',
            sortable: true,
          },
          {
            name: 'screenName',
            label: this.$t('tableHeading.screenName'),
            field: 'screen_name',
            sortable: true,
          },
          {
            name: 'totalSwipes',
            label: this.$t('access.totalSwipes'),
            field: 'total_swipes',
            sortable: true,
          },
          {
            name: 'lastSeen',
            label: this.$t('access.lastSwipe'),
            field: 'last_swipe',
            sortable: true,
            format: (val) => this.formatDate(val),
          },
        ];
      } else if (this.deviceType === 'interlocks') {
        columns = [
          {
            name: 'name',
            label: this.$t('digitalId.fullName'),
            field: 'full_name',
            sortable: true,
          },
          {
            name: 'screenName',
            label: this.$t('tableHeading.screenName'),
            field: 'screen_name',
            sortable: true,
          },
          {
            name: 'totalSwipes',
            label: this.$t('access.totalSwipes'),
            field: 'total_swipes',
            sortable: true,
          },
          {
            name: 'totalTime',
            label: this.$t('access.totalTime'),
            field: 'total_seconds',
            sortable: true,
            format: (val) => this.humanizeDurationOfSeconds(val),
          },
        ];
      } else if (this.deviceType === 'memberbucks-devices') {
        columns = [
          {
            name: 'name',
            label: this.$t('digitalId.fullName'),
            field: 'full_name',
            sortable: true,
          },
          {
            name: 'screenName',
            label: this.$t('tableHeading.screenName'),
            field: 'screen_name',
            sortable: true,
          },
          {
            name: 'totalPurchases',
            label: this.$t('memberbucks-devices.totalPurchases'),
            field: 'total_purchases',
            sortable: true,
          },
          {
            name: 'totalVolume',
            label: this.$t('memberbucks-devices.totalVolume'),
            field: 'total_volume',
            sortable: true,
            format: (val) => this.$n(val, 'currency', this.siteLocaleCurrency),
          },
        ];
      }

      return columns;
    },
    icons() {
      return icons;
    },
  },
};
</script>
