<template>
  <q-page class="column flex justify-start items-center">
    <div>
      <h3 class="q-mt-none q-mb-md">
        {{ interlock.name }}
      </h3>
      <q-card class="my-card">
        <q-card-section>
          <div class="text-h6">
            {{ $t('menuLink.manageInterlock') }}
          </div>
        </q-card-section>

        <q-card-section>
          <q-form ref="formRef">
            <div class="column q-gutter-md q-px-sm">
              <q-input
                v-model="interlock.name"
                outlined
                :label="$t('interlocks.name')"
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
                v-model="interlock.description"
                outlined
                :label="$t('interlocks.description')"
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
                v-model="interlock.ipAddress"
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
                    v-model="interlock.defaultAccess"
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
                    v-model="interlock.maintenanceLockout"
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
                    v-model="interlock.playThemeOnSwipe"
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
                    v-model="interlock.exemptFromSignin"
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
                    v-model="interlock.hiddenToMembers"
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
                  :label="$t('interlocks.remove')"
                  type="reset"
                  color="primary"
                  flat
                  class="q-ml-sm"
                  :loading="removeLoading"
                  :disabled="removeLoading"
                  @click="removeInterlock"
                />
              </div>
            </div>
          </q-form>
        </q-card-section>
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
  name: "ManageInterlockPage",
  components: {
    SavedNotification,
  },
  mixins: [formMixin],
  props: {
    interlockId: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
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
      interlock: {
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
    this.getInterlocks()
      .then(() => {
        if (this.currentInterlock === false) this.$router.push({ name: "Error404" });

        this.initForm();
      });
  },
  methods: {
    ...mapActions("adminTools", ["getInterlocks"]),
    initForm() {
      this.interlock.name = this.currentInterlock.name;
      this.interlock.description = this.currentInterlock.description;
      this.interlock.ipAddress = this.currentInterlock.ipAddress;
      this.interlock.defaultAccess = this.currentInterlock.defaultAccess;
      this.interlock.maintenanceLockout = this.currentInterlock.maintenanceLockout;
      this.interlock.playThemeOnSwipe = this.currentInterlock.playThemeOnSwipe;
      this.interlock.exemptFromSignin = this.currentInterlock.exemptFromSignin;
      this.interlock.hiddenToMembers = this.currentInterlock.hiddenToMembers;
    },
    removeInterlock() {
      this.$q.dialog({
        title: this.$t("confirmRemove"),
        ok: "Ok",
        cancel: "Cancel",
      }).onOk(() => {
        this.removeLoading = true;
        this.$axios.delete(`/api/admin/interlocks/${this.interlockId}/`)
          .then(() => {
            this.$router.push({ name: "interlocks" });
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
              this.$axios.put(`/api/admin/interlocks/${this.interlockId}/`, this.interlock)
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
    ...mapGetters("adminTools", ["interlocks"]),
    icons() {
      return icons;
    },
    currentInterlock() {
      const interlock = this.interlocks.find((item) => String(item.id) === this.interlockId);

      return interlock || false;
    },
  },
};
</script>
