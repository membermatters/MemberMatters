<template>
  <q-page class="column flex items-center justify-center q-pt-xl">
    <login-card :reset-token="resetToken" />

    <h4 v-if="$q.platform.is.electron" class="q-my-sm">OR</h4>

    <login-rfid-card v-if="$q.platform.is.electron" />
  </q-page>
</template>

<script>
import LoginRfidCard from "components/LoginRfidCard";
import LoginCard from "../components/LoginCard";
import { mapGetters } from "vuex";

export default {
  name: "LoginPage",
  components: {
    LoginRfidCard,
    LoginCard,
  },
  props: {
    resetToken: {
      type: String,
      default: null,
    },
  },
  computed: {
    ...mapGetters("config", ["images"]),
  },
};
</script>

<style scoped>
.header-image-mobile {
  max-height: 50px;
}
</style>
