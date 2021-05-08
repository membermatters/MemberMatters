<template>
  <q-page class="column flex justify-start items-center">
    <div>
      <h3 class="q-mt-none q-mb-md">
        {{ door.name }}
      </h3>
      <q-card
      class="q-mb-none"
      style="background-color: transparent"
      :class="{ 'q-pb-lg': $q.screen.xs }"
    >


      <q-tabs v-model="tab" align="justify" narrow-indicator>
        <q-tab name="profile" :label="$t('menuLink.profile')"/>
        <q-tab name="stats" :label="$t('adminTools.stats')"/>
      </q-tabs>
        <q-separator />
        <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="profile" class="q-px-lg q-py-lg">
        <q-card-section>
          <q-form ref="formRef">
            <div class="column q-gutter-md q-px-sm">
              <q-input
                v-model="door.name"
                outlined
                :label="$t('doors.name')"
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
                v-model="door.description"
                outlined
                :label="$t('doors.description')"
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
                v-model="door.ipAddress"
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
                    v-model="door.defaultAccess"
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
                    v-model="door.maintenanceLockout"
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
                    v-model="door.playThemeOnSwipe"
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
                    v-model="door.exemptFromSignin"
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
                    v-model="door.hiddenToMembers"
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
                  :label="$t('doors.remove')"
                  type="reset"
                  color="primary"
                  flat
                  class="q-ml-sm"
                  :loading="removeLoading"
                  :disabled="removeLoading"
                  @click="removeDoor"
                />
              </div>
            </div>
          </q-form>
        </q-card-section>
        </q-tab-panel>
        <q-tab-panel name="stats">
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
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
  name: "ManageDoorPage",
  components: {
    SavedNotification,
  },
  mixins: [formMixin],
  props: {
    doorId: {
      type: [String, Number],
      default: "",
    },
  },
  data() {
    return {
      tab: "profile",
      removeLoading: false,
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
      door: {
        name: "",
        description: "",
        ipAddress: "",
        defaultAccess: null,
        maintenanceLockout: null,
        playThemeOnSwipe: null,
        exemptFromSignin: null,
        hiddenToMembers: null,
      },
    };
  },
  mounted() {
    this.getDoors()
      .then(() => {
        if (this.currentDoor === false) this.$router.push({ name: "Error404" });

        this.initForm();
      });
  },
  methods: {
    ...mapActions("adminTools", ["getDoors"]),
    initForm() {
      this.door.name = this.currentDoor.name;
      this.door.description = this.currentDoor.description;
      this.door.ipAddress = this.currentDoor.ipAddress;
      this.door.defaultAccess = this.currentDoor.defaultAccess;
      this.door.maintenanceLockout = this.currentDoor.maintenanceLockout;
      this.door.playThemeOnSwipe = this.currentDoor.playThemeOnSwipe;
      this.door.exemptFromSignin = this.currentDoor.exemptFromSignin;
      this.door.hiddenToMembers = this.currentDoor.hiddenToMembers;
    },
    removeDoor() {
      this.$q.dialog({
        title: this.$t("confirmRemove"),
        ok: "Ok",
        cancel: "Cancel",
      }).onOk(() => {
        this.removeLoading = true;
        this.$axios.delete(`/api/admin/doors/${this.doorId}/`)
          .then(() => {
            this.$router.push({ name: "doors" });
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
        this.$refs.formRef.validate(false)
          .then((result) => {
            if (result) {
              this.$axios.put(`/api/admin/doors/${this.doorId}/`, this.door)
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
    ...mapGetters("adminTools", ["doors"]),
    icons() {
      return icons;
    },
    currentDoor() {
      const door = this.doors.find((item) => String(item.id) === this.doorId);

      return door || false;
    },
  },
};
</script>
