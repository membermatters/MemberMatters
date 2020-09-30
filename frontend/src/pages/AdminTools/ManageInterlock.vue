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
                outlined
                v-model="interlock.name"
                :label="$t('interlocks.name')"
                @input="saveChange('name')"
                :debounce="debounceLength"
              >
                <template v-slot:append>
                  <saved-notification
                    show-text
                    v-model="saved.name"
                    :error="saved.error"
                  />
                </template>
              </q-input>

              <q-input
                outlined
                v-model="interlock.description"
                :label="$t('interlocks.description')"
                @input="saveChange('description')"
                :debounce="debounceLength"
              >
                <template v-slot:append>
                  <saved-notification
                    show-text
                    v-model="saved.description"
                    :error="saved.error"
                  />
                </template>
              </q-input>

              <q-input
                outlined
                v-model="interlock.ipAddress"
                :label="$t('form.ipAddress')"
                @input="saveChange('ipAddress')"
                :debounce="debounceLength"
              >
                <template v-slot:append>
                  <saved-notification
                    show-text
                    v-model="saved.ipAddress"
                    :error="saved.error"
                  />
                </template>
              </q-input>

              <div class="column">
                <div class="row items-center">
                  <q-checkbox
                    v-model="interlock.defaultAccess"
                    :label="$t('access.defaultAccess')"
                    @input="saveChange('defaultAccess')"
                    :debounce="debounceLength"
                  />
                  <q-space />
                  <saved-notification
                    show-text
                    v-model="saved.defaultAccess"
                    :error="saved.error"
                  />
                </div>

                <div class="row items-center">
                  <q-checkbox
                    v-model="interlock.maintenanceLockout"
                    :label="$t('access.maintenanceLockout')"
                    @input="saveChange('maintenanceLockout')"
                    :debounce="debounceLength"
                  />
                  <q-space />
                  <saved-notification
                    show-text
                    v-model="saved.maintenanceLockout"
                    :error="saved.error"
                  />
                </div>
                <div class="row items-center">
                  <q-checkbox
                    v-model="interlock.playThemeOnSwipe"
                    :label="$t('access.playTheme')"
                    @input="saveChange('playTheme')"
                    :debounce="debounceLength"
                  />
                  <q-space />
                  <saved-notification
                    show-text
                    v-model="saved.playTheme"
                    :error="saved.error"
                  />
                </div>
                <div class="row items-center">
                  <q-checkbox
                    v-model="interlock.exemptFromSignin"
                    :label="$t('access.exemptSignin')"
                    @input="saveChange('exemptSignin')"
                    :debounce="debounceLength"
                  />
                  <q-space />
                  <saved-notification
                    show-text
                    v-model="saved.exemptSignin"
                    :error="saved.error"
                  />
                </div>
                <div class="row items-center q-gutter-sm">
                  <q-checkbox
                    v-model="interlock.hiddenToMembers"
                    :label="$t('access.hiddenToMembers')"
                    @input="saveChange('hiddenToMembers')"
                    :debounce="debounceLength"
                  />
                  <q-space />
                  <saved-notification
                    show-text
                    v-model="saved.hiddenToMembers"
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
import icons from '@icons';
import { mapGetters, mapActions } from 'vuex';
import formMixin from '@mixins/formMixin';
import SavedNotification from '@components/SavedNotification';

export default {
  name: 'ManageInterlockPage',
  mixins: [formMixin],
  components: {
    SavedNotification,
  },
  props: {
    interlockId: {
      type: String,
      default: '',
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
        name: '',
        description: '',
        ipAddress: '',
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
        if (this.currentInterlock === false) this.$router.push({ name: 'Error404' });

        this.initForm();
      });
  },
  methods: {
    ...mapActions('adminTools', ['getInterlocks']),
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
        title: this.$t('confirmRemove'),
        ok: 'Ok',
        cancel: 'Cancel',
      }).onOk(() => {
        this.removeLoading = true;
        this.$axios.delete(`/api/admin/interlocks/${this.interlockId}/`)
          .then(() => {
            this.$router.push({ name: 'interlocks' });
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
    ...mapGetters('adminTools', ['interlocks']),
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
