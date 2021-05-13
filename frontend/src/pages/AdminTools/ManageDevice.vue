<template>
  <q-page class="column flex justify-start items-center">
    <div>
      <h3 class="q-mt-none q-mb-md">{{ device.name }} {{ deviceType }}</h3>
      <q-card
        class="q-mb-none"
        style="background-color: transparent"
        :class="{ 'q-pb-lg': $q.screen.xs }"
      >
        <q-tabs v-model="tab" align="justify" narrow-indicator>
          <q-tab name="profile" :label="$t('menuLink.profile')" />
          <q-tab name="stats" :label="$t('adminTools.stats')" />
        </q-tabs>
        <q-separator />
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="profile" class="q-px-lg q-py-lg">
            <q-card-section>
              <q-form ref="formRef">
                <div class="column q-gutter-md q-px-sm">
                  <q-input
                    v-model="device.name"
                    outlined
                    :label="$t(`${deviceType}.name`)"
                    :debounce="debounceLength"
                    @input="saveChange('name')"
                  >
                    <template v-slot:append>
                      <saved-notification
                        v-model="saved.name"
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
                    @input="saveChange('description')"
                  >
                    <template v-slot:append>
                      <saved-notification
                        v-model="saved.description"
                        show-text
                        :error="saved.error"
                      />
                    </template>
                  </q-input>

                  <q-input
                    v-model="device.ipAddress"
                    outlined
                    :label="$t('form.ipAddress')"
                    :debounce="debounceLength"
                    @input="saveChange('ipAddress')"
                  >
                    <template v-slot:append>
                      <saved-notification
                        v-model="saved.ipAddress"
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
                        @input="saveChange('defaultAccess')"
                      />
                      <q-space />
                      <saved-notification
                        v-model="saved.defaultAccess"
                        show-text
                        :error="saved.error"
                      />
                    </div>

                    <div class="row items-center">
                      <q-checkbox
                        v-model="device.maintenanceLockout"
                        :label="$t('access.maintenanceLockout')"
                        :debounce="debounceLength"
                        @input="saveChange('maintenanceLockout')"
                      />
                      <q-space />
                      <saved-notification
                        v-model="saved.maintenanceLockout"
                        show-text
                        :error="saved.error"
                      />
                    </div>
                    <div class="row items-center">
                      <q-checkbox
                        v-model="device.playThemeOnSwipe"
                        :label="$t('access.playTheme')"
                        :debounce="debounceLength"
                        @input="saveChange('playTheme')"
                      />
                      <q-space />
                      <saved-notification
                        v-model="saved.playTheme"
                        show-text
                        :error="saved.error"
                      />
                    </div>
                    <div class="row items-center">
                      <q-checkbox
                        v-model="device.exemptFromSignin"
                        :label="$t('access.exemptSignin')"
                        :debounce="debounceLength"
                        @input="saveChange('exemptSignin')"
                      />
                      <q-space />
                      <saved-notification
                        v-model="saved.exemptSignin"
                        show-text
                        :error="saved.error"
                      />
                    </div>
                    <div class="row items-center q-gutter-sm">
                      <q-checkbox
                        v-model="device.hiddenToMembers"
                        :label="$t('access.hiddenToMembers')"
                        :debounce="debounceLength"
                        @input="saveChange('hiddenToMembers')"
                      />
                      <q-space />
                      <saved-notification
                        v-model="saved.hiddenToMembers"
                        show-text
                        :error="saved.error"
                      />
                    </div>
                  </div>

                  <div class="row">
                    <q-space />
                    <q-btn
                      :label="$t(`${deviceType}.remove`)"
                      type="reset"
                      color="primary"
                      flat
                      class="q-ml-sm"
                      :loading="removeLoading"
                      :disabled="removeLoading"
                      @click="removeDevice"
                    />
                  </div>
                </div>
              </q-form>
            </q-card-section>
          </q-tab-panel>

          <q-tab-panel name="stats">
            <div class="row flex content-start justify-center">
              <q-table
                :data="device.stats"
                :columns="columnI18n"
                row-key="key"
                :filter="filter"
                :pagination.sync="devicePagination"
                :dense="$q.screen.lt.md"
                :grid="$q.screen.xs"
                class="table"
                :loading="loading"
                :no-data-label="$t(`${deviceType}.nodata`)"
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
      </q-card>
    </div>
  </q-page>
</template>

<script>
import icons from "@icons";
import { mapGetters, mapActions } from "vuex";
import formMixin from "@mixins/formMixin";
import SavedNotification from "@components/SavedNotification";

export default {
  name: "ManageDevicePage",
  components: {
    SavedNotification,
  },
  mixins: [formMixin],
  props: {
    deviceId: {
      type: String,
      default: "",
    },
    deviceType: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      tab: "profile",
      removeLoading: false,
      loading: false,
      errorLoading: false,
      updateInterval: null,
      filter: "",
      devicePagination: {
        sortBy: "desc",
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
        name: "",
        description: "",
        ipAddress: "",
        defaultAccess: null,
        maintenanceLockout: null,
        playThemeOnSwipe: null,
        exemptFromSignin: null,
        hiddenToMembers: null,
        usage: null,
        stats: [],
      },
    };
  },
  mounted() {
    this.getDoors().then(() => {
      this.getInterlocks().then(() => {
        if (this.currentDevice === false)
          this.$router.push({ name: "Error404" });

        this.initForm();
      });
    });
  },
  methods: {
    ...mapActions("adminTools", ["getDoors", "getInterlocks"]),
    initForm() {
      this.device.name = this.currentDevice.name;
      this.device.description = this.currentDevice.description;
      this.device.ipAddress = this.currentDevice.ipAddress;
      this.device.defaultAccess = this.currentDevice.defaultAccess;
      this.device.maintenanceLockout = this.currentDevice.maintenanceLockout;
      this.device.playThemeOnSwipe = this.currentDevice.playThemeOnSwipe;
      this.device.exemptFromSignin = this.currentDevice.exemptFromSignin;
      this.device.hiddenToMembers = this.currentDevice.hiddenToMembers;
      this.device.usage = this.currentDevice.usage;
      this.device.stats = this.currentDevice.stats;
    },
    removeDevice() {
      this.$q
        .dialog({
          title: this.$t("confirmRemove"),
          ok: "Ok",
          cancel: "Cancel",
        })
        .onOk(() => {
          this.removeLoading = true;
          this.$axios
            .delete(`/api/admin/${this.deviceType}/${this.deviceId}/`)
            .then(() => {
              this.$router.push({ name: "devices" });
            })
            .catch((error) => {
              this.removeLoading = true;
              this.$q.dialog({
                title: this.$t("error.error"),
                message: this.$t("error.requestFailed"),
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
                `/api/admin/${this.deviceType}/${this.deviceId}/`,
                this.device
              )
              .then(() => {
                this.saved.error = false;
                this.saved[field] = true;
              })
              .catch(() => {
                this.initForm();
                this.saved.error = true;
                this.saved[field] = true;
              });
          }
        });
      });
    },
  },
  computed: {
    ...mapGetters("adminTools", ["doors", "interlocks"]),
    columnI18n() {
      let columns = [];
      if (this.deviceType === "doors") {
        columns = [
          {
            name: "user",
            label: "User",
            field: "screen_name",
            sortable: true,
          },
          {
            name: "record",
            label: "Swipes",
            field: "records",
            sortable: true,
          },
          {
            name: "lastSeen",
            label: "Last Swipe",
            field: "lastSeen",
            sortable: true,
          },
        ];
      } else {
        columns = [
          {
            name: "user",
            label: "User",
            field: "screen_name",
            sortable: true,
          },
          {
            name: "record",
            label: "Records",
            field: "records",
            sortable: true,
          },
          {
            name: "onTime",
            label: "Minutes Logged",
            field: "onTime",
            sortable: true,
          },
        ];
      }
      return columns;
    },
    icons() {
      return icons;
    },
    currentDevice() {
      // TODO: Could we implement Next/Previous buttons to cycle through them?
      let device;
      if (this.deviceType === "doors") {
        device = this.doors.find((item) => String(item.id) === this.deviceId);
      } else {
        device = this.interlocks.find(
          (item) => String(item.id) === this.deviceId
        );
      }
      return device || false;
    },
  },
};
</script>
