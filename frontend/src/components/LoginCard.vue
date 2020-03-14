<template>
  <div class="q-pa-md">
    <q-card class="login-card">
      <h6 class="q-ma-none q-pa-md">
        {{ $t('loginCard.loginToContinue') }}
      </h6>

      <q-card-section>
        <q-form
          @submit="onSubmit"
          @reset="onReset"
          class="q-gutter-md"
        >
          <q-input
            filled
            type="email"
            v-model="email"
            label="Your email"
            lazy-rules
            :rules="[ val => validateEmail(val) || $t('validation.invalidEmail')]"
          />

          <q-input
            filled
            type="password"
            v-model="password"
            label="Your password"
            lazy-rules
            :rules="[
              val => validateNotEmpty(val) || $t('validation.invalidPassword'),
            ]"
          />


          <q-banner
            v-if="this.loggedIn"
            class="bg-green text-white"
          >
            {{ $t('loginCard.loginSuccess') }}
          </q-banner>

          <q-banner
            v-if="loginFailed"
            class="bg-red text-white"
          >
            {{ $t('loginCard.loginFailed') }}
          </q-banner>

          <p class="text-caption">
            {{ $t('loginCard.notAMember') }}
            <router-link :to="{ name: 'register' }">
              {{ $t('loginCard.registerHere') }}
            </router-link>
          </p>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('loginCard.resetPassword')"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
              @click="resetPasswordPrompt = true"
            />
            <q-btn
              :label="$t('loginCard.login')"
              type="submit"
              color="primary"
              :loading="buttonLoading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>

    <q-dialog
      v-model="resetPasswordPrompt"
      persistent
    >
      <q-card style="max-width: 350px">
        <q-card-section>
          <div class="text-h6">
            {{ $t('loginCard.forgottenPassword') }}
          </div>
          <div>
            {{ $t('loginCard.forgottenPasswordDescription') }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            :label="$t('loginCard.emailLabel')"
            v-model="email"
            autofocus
            @keyup.enter="resetPasswordPrompt = false"
          />
        </q-card-section>

        <q-card-actions
          align="right"
          class="text-primary"
        >
          <q-btn
            flat
            :label="$t('button.cancel')"
            v-close-popup
          />
          <q-btn
            flat
            :label="$t('button.submit')"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapGetters } from 'vuex';
import formMixin from '../mixins/formMixin';

export default {
  name: 'LoginCard',
  mixins: [formMixin],
  data() {
    return {
      email: '',
      password: '',
      loginFailed: false,
      buttonLoading: false,
      resetPasswordPrompt: false,
    };
  },
  mounted() {
    if (this.loggedIn) this.reditectLoggedIn();
  },
  methods: {
    ...mapMutations('profile', ['setLoggedIn']),
    reditectLoggedIn() {
      if (this.$route.query.redirect) this.$router.push(this.$route.query.redirect);
      else { this.$router.push({ name: 'dashboard' }); }
    },
    onReset() {
      this.email = null;
      this.password = null;
    },
    onSubmit() {
      this.login();
    },
    login() {
      this.loginFailed = false;
      this.buttonLoading = true;
      axios.post('/api/login/', {
        email: this.email,
        password: this.password,
      })
        .then((response) => {
          if (response.data.success === true) {
            this.setLoggedIn(true);
            this.loginFailed = false;
            this.reditectLoggedIn();
          } else {
            this.loginFailed = true;
          }
        })
        .catch((error) => {
          throw error;
        })
        .finally(() => {
          this.buttonLoading = false;
        });
    },
  },
  computed: {
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>

<style scoped>
  .login-card {
    min-width: 300px;
  }
</style>
