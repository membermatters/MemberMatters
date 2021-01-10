<template>
  <div class="row">
    <div class="q-pa-md col-12 col-sm-4">
      <a @click="signInCard.click" :disabled="signinDisable">
        <q-card class="q-pa-xl column justify-center items-center">
          <p class="text-h4">
            {{ signInCard.title }}
          </p>
          <q-icon style="font-size: 100px" :name="signInCard.icon" />
        </q-card>
      </a>
    </div>
    <div class="q-pa-md col-12 col-sm-4">
      <report-issue-card />
    </div>
  </div>
</template>

<script>
import ReportIssueCard from "@components/ReportIssueCard.vue";
import { mapGetters, mapMutations, mapActions } from "vuex";
import icons from "@icons";

export default {
  name: "QuickActions",
  components: { ReportIssueCard },
  mounted() {
    this.getSiteSignedIn();
  },
  data() {
    return {
      signinDisable: false,
    };
  },
  methods: {
    ...mapMutations("profile", ["setSiteSignedIn"]),
    ...mapActions("profile", ["getSiteSignedIn"]),
    doSignIn() {
      this.signinDisable = true;
      this.$axios
        .post("/api/sitesessions/signin/", { guests: [] })
        .then(() => {
          this.setSiteSignedIn(true);
          this.$q.dialog({
            title: "Success",
            message: this.$t("dashboard.signinSuccess"),
          });
        })
        .catch(() => {
          this.setSiteSignedIn(false);
          this.$q
            .dialog({
              title: "Alert",
              message: this.$t("dashboard.signinError"),
            })
            .finally(() => (this.signinDisable = false));
        });
    },
    doSignOut() {
      this.$axios
        .put("/api/sitesessions/signout/")
        .then(() => {
          this.setSiteSignedIn(false);
          this.$router.push({ name: "logout" });
        })
        .catch(() => {
          this.$q
            .dialog({
              title: "Alert",
              message: this.$t("dashboard.signoutError"),
            })
            .finally(() => (this.signinDisable = false));
        });
    },
  },
  computed: {
    ...mapGetters("profile", ["siteSignedIn"]),
    signInCard() {
      if (this.siteSignedIn) {
        return {
          title: this.$t("dashboard.signOut"),
          icon: icons.signout,
          click: this.doSignOut,
        };
      } else {
        return {
          title: this.$t("dashboard.signIn"),
          icon: icons.signin,
          click: this.doSignIn,
        };
      }
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
