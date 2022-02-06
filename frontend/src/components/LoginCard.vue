<template>
  <div class="q-pa-md login-card">
    <q-card v-if="!resetToken">
      <h6 class="q-ma-none q-pa-md">
        {{ $t("loginCard.loginToContinue") }}
      </h6>

      <form action="https://portal.hsbne.org"></form>

      <q-card-section>
        <q-form class="q-gutter-md" @submit="onSubmit" @reset="onReset">
          <q-input
            id="username-field"
            v-model="email"
            ref="focusInput"
            filled
            autocomplete="on"
            type="email"
            label="Your email"
            lazy-rules
            :rules="[
              (val) => validateEmail(val) || $t('validation.invalidEmail'),
            ]"
          />

          <q-input
            v-model="password"
            id="password-field"
            filled
            autocomplete="on"
            type="password"
            label="Your password"
            lazy-rules
            :rules="[
              (val) =>
                validateNotEmpty(val) || $t('validation.invalidPassword'),
            ]"
          />

          <q-banner v-if="loginComplete" class="bg-positive text-white">
            {{ $t("loginCard.loginSuccess") }}
          </q-banner>

          <q-banner v-if="loginFailed" class="bg-negative text-white">
            {{ $t("error.loginFailed") }}
          </q-banner>

          <q-banner v-if="unverifiedEmail" class="bg-negative text-white">
            {{ $t("loginCard.unverifiedEmail") }}
          </q-banner>

          <q-banner v-if="loginError" class="bg-negative text-white">
            {{ $t("error.requestFailed") }}
          </q-banner>

          <p class="text-caption">
            {{ $t("loginCard.notAMember") }}
            <router-link
              :to="{ name: 'register' }"
              :class="$q.dark.isActive ? 'text-white' : 'text-black'"
            >
              {{ $t("loginCard.registerHere") }}
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
              @click="reset.prompt = true"
            />
            <q-btn
              :label="$t('loginCard.login')"
              type="submit"
              color="primary-btn"
              :loading="buttonLoading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>

    <q-card v-else class="login-card">
      <h6 class="q-ma-none q-pa-md">
        {{ $t("loginCard.resetPassword") }}
      </h6>
      <q-card-section>
        <q-form class="q-gutter-md" @submit="submitResetPassword">
          <q-input
            v-model="reset.password"
            id="new-password-field"
            ref="focusInput"
            filled
            autocomplete="on"
            autofocus
            type="password"
            label="Your new password"
            lazy-rules
            :disable="this.reset.formDisabled"
            :rules="[
              (val) =>
                validateNotEmpty(val) || $t('validation.invalidPassword'),
            ]"
          />

          <q-input
            v-model="reset.password2"
            filled
            autocomplete="on"
            id="new-password-confirm-field"
            type="password"
            label="Confirm password"
            lazy-rules
            :disable="this.reset.formDisabled"
            :rules="[
              (val) =>
                validateNotEmpty(val) || $t('validation.invalidPassword'),
              (val) =>
                val === this.reset.password ||
                $t('validation.passwordNotMatch'),
            ]"
          />

          <q-banner v-if="this.reset.confirmed" class="bg-positive text-white">
            {{ $t("loginCard.resetConfirm") }}
          </q-banner>

          <q-banner
            v-if="this.reset.invalidToken"
            class="bg-negative text-white"
          >
            {{ $t("loginCard.resetInvalid") }}
          </q-banner>

          <q-banner v-if="this.reset.failed" class="bg-negative text-white">
            {{ $t("loginCard.resetNotConfirm") }}
          </q-banner>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('loginCard.backToLogin')"
              color="primary-btn"
              flat
              class="q-ml-sm"
              @click="$router.push({ name: 'login' })"
            />
            <q-btn
              :label="$t('button.submit')"
              type="submit"
              color="primary-btn"
              :disable="this.reset.formDisabled"
              :loading="this.reset.loading"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>

    <q-dialog v-model="reset.prompt" persistent>
      <q-card style="max-width: 350px">
        <q-card-section>
          <div class="text-h6">
            {{ $t("loginCard.forgottenPassword") }}
          </div>
          <div>
            {{ $t("loginCard.forgottenPasswordDescription") }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="reset.email"
            :label="$t('loginCard.emailLabel')"
            autofocus
            @keyup.enter="resetPassword()"
          />
        </q-card-section>

        <q-banner v-if="reset.success" class="bg-positive text-white q-mx-md">
          {{ $t("loginCard.resetSuccess") }}
        </q-banner>

        <q-banner v-if="reset.failed" class="bg-negative text-white q-mx-md">
          {{ $t("loginCard.resetFailed") }}
        </q-banner>

        <q-card-actions align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            :label="
              this.reset.disableResetSubmitButton
                ? $t('button.close')
                : $t('button.cancel')
            "
          />
          <q-btn
            flat
            :label="$t('button.submit')"
            :loading="reset.loading"
            :disable="this.reset.disableResetSubmitButton"
            @click="resetPassword()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script>
import { mapMutations, mapGetters, mapActions } from "vuex";
import { Loading } from "quasar";
import formMixin from "../mixins/formMixin";
import { Plugins } from "@capacitor/core";
const { SplashScreen } = Plugins;

export default {
  name: "LoginCard",
  mixins: [formMixin],
  props: {
    resetToken: {
      type: String,
      default: null,
    },
    noRedirect: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      email: "",
      password: "",
      loginFailed: false,
      loginError: false,
      loginComplete: false,
      unverifiedEmail: false,
      buttonLoading: false,
      disableResetSubmitButton: false,
      discourseSsoData: null,
      reset: {
        formDisabled: true,
        success: false,
        failed: false,
        loading: false,
        prompt: false,
        password: "",
        password2: "",
        confirmed: false,
        invalidToken: false,
      },
    };
  },
  async mounted() {
    if (this.$route.query.sso && this.$route.query.sig) {
      this.discourseSsoData = this.$route.query;
    }

    // check if we're logged in and our session is still valid
    await this.retrieveAuth();
    await this.getLoggedIn();

    // if we're logged in then open the app straight away, then
    if (this.loggedIn) {
      this.redirectLoggedIn(false);
    } else {
      await SplashScreen.hide();
      // if we're not in electron, auto focus the first field
      if (!this.$q.platform.is.electron) this.$refs.focusInput.focus();
    }

    if (this.resetToken) {
      Loading.show({ message: "Validating request..." });

      this.validatePasswordReset()
        .then(() => {
          Loading.hide();
          this.reset.formDisabled = false;
        })
        .catch(() => {
          Loading.hide();
          this.reset.invalidToken = true;
        });
    }
  },
  methods: {
    ...mapActions("profile", ["getLoggedIn"]),
    ...mapActions("auth", ["retrieveAuth"]),
    ...mapMutations("profile", ["setLoggedIn"]),
    ...mapMutations("auth", ["setAuth"]),
    /**
     * Redirects to the dashboard page on successful login.
     */
    redirectLoggedIn(delay = true) {
      this.loginFailed = false;
      this.loginError = false;

      if (this.discourseSsoData) {
        this.login();
        return;
      }

      this.loginComplete = true;
      this.$emit("login-complete");
      if (this.$route.query.redirect)
        this.$router.push(this.$route.query.redirect);
      else if (!this.noRedirect && delay) {
        setTimeout(() => {
          this.setLoggedIn(true);
          this.$router.push({ name: "dashboard" });
          setTimeout(SplashScreen.hide, 500);
        }, 1000);
      } else {
        this.$router.push({ name: "dashboard" });
        setTimeout(SplashScreen.hide, 500);
      }
    },
    onReset() {
      this.email = null;
      this.password = null;
    },
    onSubmit() {
      this.login();
    },
    /**
     * This sends the login API request to log the user in.
     */
    login() {
      this.loginFailed = false;
      this.loginError = false;
      this.buttonLoading = true;

      if (this.discourseSsoData) {
        this.$axios
          .post("/api/login/", {
            email: this.email,
            password: this.password,
            sso: this.discourseSsoData,
          })
          .then((response) => {
            this.loginFailed = false;
            this.loginError = false;
            this.loginComplete = true;

            window.location = response.data.redirect;
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.loginFailed = true;
              this.unverifiedEmail = false;
            } else if (error.response.status === 403) {
              this.unverifiedEmail = true;
              this.loginFailed = false;
              throw error;
            } else {
              this.loginError = true;
              this.unverifiedEmail = false;
              throw error;
            }
          })
          .finally(() => {
            this.buttonLoading = false;
          });
      } else if (this.$q.platform.is.capacitor) {
        this.$axios
          .post("/api/token/obtain/", {
            email: this.email,
            password: this.password,
          })
          .then((response) => {
            this.setAuth(response.data);
            this.redirectLoggedIn();
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.loginFailed = true;
              this.unverifiedEmail = false;
            } else if (error.response.status === 403) {
              this.unverifiedEmail = true;
              this.loginFailed = false;
              throw error;
            } else {
              this.loginError = true;
              this.unverifiedEmail = false;
              throw error;
            }
          })
          .finally(() => {
            this.buttonLoading = false;
          });
      } else {
        this.$axios
          .post("/api/login/", {
            email: this.email,
            password: this.password,
          })
          .then(() => {
            this.redirectLoggedIn();
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.loginFailed = true;
              this.unverifiedEmail = false;
            } else if (error.response.status === 403) {
              this.unverifiedEmail = true;
              this.loginFailed = false;
              throw error;
            } else {
              this.loginError = true;
              this.unverifiedEmail = false;
              throw error;
            }
          })
          .finally(() => {
            this.buttonLoading = false;
          });
      }
    },
    /**
     * This submits the password reset request so the user gets a reset link in their email.
     */
    resetPassword() {
      this.loginFailed = false;
      this.reset.success = false;
      this.reset.loading = true;

      this.$axios
        .post("/api/password/reset/", {
          email: this.reset.email,
        })
        .then((response) => {
          if (response.data.success === true) {
            this.reset.success = true;
            this.reset.disableResetSubmitButton = true;
            this.reset.failed = false;
          } else {
            this.reset.success = false;
            this.reset.failed = true;
          }
        })
        .catch((error) => {
          throw error;
        })
        .finally(() => {
          this.reset.loading = false;
        });
    },
    /**
     * This sends a request to validate the password reset token.
     * @returns {Promise<unknown>}
     */
    validatePasswordReset() {
      return new Promise((resolve, reject) => {
        this.$axios
          .post("/api/password/reset/", {
            token: this.resetToken,
          })
          .then((response) => {
            if (response.data.success) {
              resolve();
            } else {
              reject();
            }
          })
          .catch((error) => {
            reject();
            throw error;
          });
      });
    },
    /**
     * This will send the user's new password and reset token to the API.
     */
    submitResetPassword() {
      this.reset.success = false;
      this.reset.loading = true;

      this.$axios
        .post("/api/password/reset/", {
          password: this.reset.password,
          token: this.resetToken,
        })
        .then((response) => {
          if (response.data.success === true) {
            this.reset.confirmed = true;
            this.reset.failed = false;
            this.reset.formDisabled = true;
            setTimeout(() => {
              // eslint-disable-next-line no-restricted-globals
              location.href = "/login";
            }, 3000);
          } else {
            this.reset.confirmed = false;
            this.reset.failed = true;
          }
        })
        .catch((error) => {
          this.reset.confirmed = false;
          this.reset.failed = true;
          throw error;
        })
        .finally(() => {
          this.reset.loading = false;
        });
    },
  },
  computed: {
    ...mapGetters("profile", ["loggedIn"]),
  },
};
</script>

<style scoped>
.login-card {
  max-width: 400px;
  width: 100%;
}
</style>
