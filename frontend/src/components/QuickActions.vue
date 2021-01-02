<template>
  <div class="row">
    <div
      v-for="action in quickActions"
      :key="action.title"
      class="q-pa-md col-12 col-sm-4"
    >
      <a
        @click="action.click"
      >
        <q-card
          class="q-pa-xl column justify-center items-center"
        >
          <p class="text-h4">
            {{ action.title }}
          </p>
          <q-icon
            style="font-size: 100px"
            :name="action.icon"
          />
        </q-card>
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from "vuex";
import icons from "@icons";

export default {
  name: "QuickActions",
  mounted() {
    this.getSiteSignedIn();
  },
  methods: {
    ...mapMutations("profile", ["setSiteSignedIn"]),
    ...mapActions("profile", ["getSiteSignedIn"]),
    doSignIn() {
      this.$axios.post("/api/sitesessions/signin/", { guests: [] })
        .then(() => {
          this.setSiteSignedIn(true);
          this.$q.dialog({
            title: "Success",
            message: this.$t("dashboard.signinSuccess"),
          });
        })
        .catch(() => {
          this.setSiteSignedIn(false);
          this.$q.dialog({
            title: "Alert",
            message: this.$t("dashboard.signinError"),
          });
        });
    },
    doSignOut() {
      this.$axios.put("/api/sitesessions/signout/")
        .then(() => {
          this.setSiteSignedIn(false);
          this.$router.push({ name: "logout" });
        })
        .catch(() => {
          this.$q.dialog({
            title: "Alert",
            message: this.$t("dashboard.signoutError"),
          });
        });
    },
  },
  computed: {
    ...mapGetters("profile", ["siteSignedIn"]),
    quickActions() {
      const actions = [];

      if (this.siteSignedIn) {
        actions.push({
          title: "Site Sign Out",
          icon: icons.signout,
          click: this.doSignOut,
        });
      } else {
        actions.push({
          title: "Site Sign In",
          icon: icons.signin,
          click: this.doSignIn,
        });
      }

      return actions;
    },
  },
};
</script>

<style scoped>
  a {
    text-decoration: none;
  }
  </style>
