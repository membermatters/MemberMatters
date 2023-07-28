<template>
  <div class="profile-form">
    <q-form ref="formRef">
      <q-input
        v-model="form.email"
        outlined
        :debounce="debounceLength"
        :label="$t('form.email')"
        :rules="[(val) => validateEmail(val) || $t('validation.invalidEmail')]"
        @update:model-value="saveChange('email')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.email"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-model="form.firstName"
        outlined
        :debounce="debounceLength"
        :label="$t('form.firstName')"
        :rules="[
          (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
        ]"
        @update:model-value="saveChange('firstName')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.firstName"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-model="form.lastName"
        outlined
        :debounce="debounceLength"
        :label="$t('form.lastName')"
        :rules="[
          (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
        ]"
        @update:model-value="saveChange('lastName')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.lastName"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-model="form.phone"
        outlined
        :debounce="debounceLength"
        :label="$t('form.mobile')"
        :rules="[
          (val) => validateNotEmpty(val) || $t('validation.invalidPhone'),
        ]"
        @update:model-value="saveChange('phone')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.phone"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-model="form.screenName"
        outlined
        :debounce="debounceLength"
        :label="$t('form.screenName')"
        :rules="[
          (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
        ]"
        @update:model-value="saveChange('screenName')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.screenName"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-if="features?.signup?.collectVehicleRegistrationPlate"
        v-model="form.vehicleRegistrationPlate"
        outlined
        :debounce="debounceLength"
        :label="$t('form.vehicleRegistrationPlate')"
        :rules="[(val) => validateMax30(val) || $t('validation.max30')]"
        @update:model-value="saveChange('vehicleRegistrationPlate')"
      >
        <template v-slot:append>
          <saved-notification
            :success="saved.vehicleRegistrationPlate"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>
    </q-form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import icons from '../icons';
import formMixin from '../mixins/formMixin';
import SavedNotification from '@components/SavedNotification.vue';

export default {
  name: 'ProfileForm',
  components: {
    SavedNotification,
  },
  mixins: [formMixin],
  data() {
    return {
      form: {
        email: '',
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
        firstName: false,
        lastName: false,
        phone: false,
        screenName: false,
        vehicleRegistrationPlate: false,
      },
    };
  },
  methods: {
    ...mapActions('profile', ['getProfile']),
    loadInitialForm() {
      this.form.email = this.profile.email;
      this.form.firstName = this.profile.firstName;
      this.form.lastName = this.profile.lastName;
      this.form.phone = this.profile.phone;
      this.form.screenName = this.profile.screenName;
      this.form.vehicleRegistrationPlate =
        this.profile.vehicleRegistrationPlate;
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false).then((result) => {
          if (result) {
            this.$axios
              .put('/api/profile/', this.form)
              .then(() => {
                this.saved.error = false;
                this.saved[field] = true;
                setTimeout(() => {
                  this.saved[field] = false;
                }, 1500);
                this.getProfile();
              })
              .catch(() => {
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
  },
  watch: {
    profile() {
      this.loadInitialForm();
    },
  },
  beforeMount() {
    this.loadInitialForm();
  },
  computed: {
    ...mapGetters('profile', ['profile']),
    ...mapGetters('config', ['features']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass">
.profile-form
  max-width: $maxWidthMedium
  width: 100%
</style>
