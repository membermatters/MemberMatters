<template>
  <div class="profile-form">
    <p>
      {{ $t('form.pageDescription') }}
    </p>

    <q-form ref="formRef">
      <q-input
        outlined
        @input="saveChange('email')"
        :debounce="debounceLength"
        v-model="form.email"
        :label="$t('form.email')"
        :rules="[ val => validateEmail(val) || $t('validation.invalidEmail')]"
      >
        <template v-slot:append>
          <saved-notification
            show-text
            v-model="saved.email"
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        outlined
        @input="saveChange('firstName')"
        :debounce="debounceLength"
        v-model="form.firstName"
        :label="$t('form.firstName')"
        :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
      >
        <template v-slot:append>
          <saved-notification
            show-text
            v-model="saved.firstName"
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        outlined
        @input="saveChange('lastName')"
        :debounce="debounceLength"
        v-model="form.lastName"
        :label="$t('form.lastName')"
        :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
      >
        <template v-slot:append>
          <saved-notification
            show-text
            v-model="saved.lastName"
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        outlined
        @input="saveChange('phone')"
        :debounce="debounceLength"
        v-model="form.phone"
        :label="$t('form.phone')"
        :rules="[ val => validateNotEmpty(val) || $t('validation.invalidPhone')]"
      >
        <template v-slot:append>
          <saved-notification
            show-text
            v-model="saved.phone"
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        outlined
        @input="saveChange('screenName')"
        :debounce="debounceLength"
        v-model="form.screenName"
        :label="$t('form.screenName')"
        :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
      >
        <template v-slot:append>
          <saved-notification
            show-text
            v-model="saved.screenName"
            :error="saved.error"
          />
        </template>
      </q-input>
    </q-form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';
import icons from '../icons';
import formMixin from '../mixins/formMixin';
import SavedNotification from './SavedNotification';

export default {
  name: 'ProfileForm',
  mixins: [formMixin],
  components: {
    SavedNotification,
  },
  data() {
    return {
      form: {
        email: '',
        firstName: '',
        lastName: '',
        phone: '',
        screenName: '',
        groups: [],
      },
      saved: {
        // if there was an error saving the form
        error: false,

        email: false,
        firstName: false,
        lastName: false,
        phone: false,
        screenName: false,
        groups: false,
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
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false)
          .then((result) => {
            if (result) {
              axios.put('/api/profile/', this.form)
                .then(() => {
                  this.saved.error = false;
                  this.saved[field] = true;
                  this.getProfile();
                })
                .catch(() => {
                  this.saved.error = true;
                  this.saved[field] = true;
                });
            }
          });
      });
    },
  },
  beforeMount() {
    this.loadInitialForm();
  },
  watch: {
    profile() {
      this.loadInitialForm();
    },
  },
  computed: {
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
  },
};
</script>
