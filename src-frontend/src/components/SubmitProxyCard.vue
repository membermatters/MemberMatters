<template>
  <div class="q-pa-md">
    <q-card class="submit-issue-card">
      <h6 class="q-ma-none q-pa-md">
        {{ $t('submitProxy.pageDescription') }}
      </h6>

      <q-card-section>
        <q-form class="q-gutter-md" @submit="onSubmit">
          <q-input
            v-model="title"
            filled
            type="text"
            label="Issue Title"
            lazy-rules
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
          >
            <template v-slot:prepend>
              <q-icon :name="icons.warning" />
            </template>
          </q-input>

          <q-input
            v-model="description"
            filled
            type="textarea"
            label="Issue Description"
            autogrow
            lazy-rules
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
          >
            <template v-slot:prepend>
              <q-icon :name="icons.comment" />
            </template>
          </q-input>

          <q-banner v-if="submitSuccess" class="bg-positive text-white">
            {{ $t('submitProxy.success') }}<br />
            <a v-if="issueUrl" target="_blank" :href="issueUrl">{{
              issueUrl
            }}</a>
          </q-banner>

          <q-banner v-if="submitError" class="bg-negative text-white">
            {{ $t('submitProxy.fail') }}
          </q-banner>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('button.submit')"
              type="submit"
              color="primary-btn"
              :loading="buttonLoading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import formMixin from '../mixins/formMixin';
import icons from '../icons';

export default {
  name: 'SubmitProxyCard',
  mixins: [formMixin],
  data() {
    return {
      submitSuccess: false,
      submitError: false,
      buttonLoading: false,
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
  mounted() {
    // if (this.loggedIn) this.reditectLoggedIn();
  },
  methods: {
    onSubmit() {
      this.submit();
    },
    submit() {
      this.submitError = false;
      this.buttonLoading = true;

      this.$axios
        .post('/api/tools/issue/', {
          title: this.title,
          description: this.description,
        })
        .then((response) => {
          if (response.data.success === true) {
            this.issueUrl = response.data.url;
            this.submitError = false;
            this.submitSuccess = true;
          } else {
            this.submitError = true;
            this.submitSuccess = false;
          }
        })
        .catch((error) => {
          this.submitError = true;
          this.submitSuccess = false;
          throw error;
        })
        .finally(() => {
          this.buttonLoading = false;
        });
    },
  },
};
</script>

<style lang="sass" scoped>
.submit-issue-card
  min-width: $minWidth
</style>
