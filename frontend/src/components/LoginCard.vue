<template>
  <div class="q-pa-md">
    <q-card class="login-card">
      <h6 class="q-ma-none q-pa-md">
        {{ $t('info.loginToContinue') }}
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
            {{ $t('info.loginSuccess') }}
          </q-banner>

          <q-banner
            v-if="loginFailed"
            class="bg-red text-white"
          >
            {{ $t('error.loginFailed') }}
          </q-banner>

          <p class="text-caption">
            {{ $t('info.notAMember') }}
            <router-link :to="{ name: 'register' }">
              {{ $t('info.registerHere') }}
            </router-link>
          </p>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('button.reset')"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
            <q-btn
              :label="$t('button.submit')"
              type="submit"
              color="primary"
              :loading="buttonLoading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
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
