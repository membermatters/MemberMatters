<template>
  <q-page class="flex flex-center">
    <q-spinner v-if="spinner && !error" color="primary-btn" size="3em" />

    <q-banner v-if="!spinner" class="bg-positive text-white">
      {{ $t("logoutPage.logoutSuccess") }}
    </q-banner>

    <q-banner v-if="error" class="bg-negative text-white">
      {{ $t("logoutPage.logoutFailed") }}
    </q-banner>
  </q-page>
</template>

<script>
import { mapMutations } from "vuex";

export default {
  name: "LogoutPage",
  data() {
    return {
      error: false,
      spinner: true,
    };
  },
  mounted() {
    this.$axios
      .post("/api/logout/")
      .then(() => {
        this.completeLogout();
      })
      .catch((error) => {
        if (error.response.status === 401) {
          this.completeLogout();
        } else {
          this.error = true;
          throw error;
        }
      });
  },
  methods: {
    ...mapMutations("profile", ["setLoggedIn", "resetState"]),
    ...mapMutations("auth", ["setAuth"]),
    completeLogout() {
      this.resetState();
      this.setAuth({ access: "", refresh: "" });
      this.setLoggedIn(false);
      this.error = false;
      this.spinner = false;
      setTimeout(() => {
        this.$router.push({ name: "login" });
      }, 2000);
    },
  },
};
</script>
