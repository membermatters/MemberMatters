<template>
  <div class="profile-form">
    <q-form ref="formRef">
      <q-input
        v-model="form.email"
        outlined
        :debounce="debounceLength"
        :label="$t('form.email')"
        :rules="[(val) => validateEmail(val) || $t('validation.invalidEmail')]"
        @input="saveChange('email')"
      >
        <template v-slot:append>
          <saved-notification
            v-model="saved.email"
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
        @input="saveChange('firstName')"
      >
        <template v-slot:append>
          <saved-notification
            v-model="saved.firstName"
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
        @input="saveChange('lastName')"
      >
        <template v-slot:append>
          <saved-notification
            v-model="saved.lastName"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>

      <q-input
        v-model="form.phone"
        outlined
        :debounce="debounceLength"
        :label="$t('form.phone')"
        :rules="[
          (val) => validateNotEmpty(val) || $t('validation.invalidPhone'),
        ]"
        @input="saveChange('phone')"
      >
        <template v-slot:append>
          <saved-notification
            v-model="saved.phone"
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
        @input="saveChange('screenName')"
      >
        <template v-slot:append>
          <saved-notification
            v-model="saved.screenName"
            show-text
            :error="saved.error"
          />
        </template>
      </q-input>
    </q-form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import icons from "../icons";
import formMixin from "../mixins/formMixin";
import SavedNotification from "./SavedNotification";

export default {
  name: "ProfileForm",
  components: {
    SavedNotification,
  },
  mixins: [formMixin],
  data() {
    return {
      form: {
        email: "",
        firstName: "",
        lastName: "",
        phone: "",
        screenName: "",
      },
      saved: {
        // if there was an error saving the form
        error: false,

        email: false,
        firstName: false,
        lastName: false,
        phone: false,
        screenName: false,
      },
    };
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    loadInitialForm() {
      this.form.email = this.profile.email;
      this.form.firstName = this.profile.firstName;
      this.form.lastName = this.profile.lastName;
      this.form.phone = this.profile.phone;
      this.form.screenName = this.profile.screenName;
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false).then((result) => {
          if (result) {
            this.$axios
              .put("/api/profile/", this.form)
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
  watch: {
    profile() {
      this.loadInitialForm();
    },
  },
  beforeMount() {
    this.loadInitialForm();
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
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
