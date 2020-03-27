<template>
  <div class="profile-form">
    <p>
      {{ $t('form.pageDescription') }}
    </p>

    <q-form>
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
            :error="saved.error"
            v-model="saved.firstName"
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
          <saved-notification v-model="saved.lastName" />
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
          <saved-notification v-model="saved.phone" />
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
          <saved-notification v-model="saved.screenName" />
        </template>
      </q-input>
    </q-form>
  </div>
</template>

<script>
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
    saveChange(field) {
      this.saved[field] = true;
    },
  },
  computed: {
    debounceLength() {
      return 1000;
    },
    icons() {
      return icons;
    },
  },
};
</script>
