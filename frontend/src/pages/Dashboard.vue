<template>
  <q-page class="row flex content-start justify-center">
    <div v-if="loggedIn">
      <template v-if="Platform.is.electron">
        <h5 class="q-ma-md">
          {{ $t("dashboard.quickActions") }}
        </h5>
        <div class="row">
          <quick-actions />
        </div>
      </template>

      <h5 class="q-ma-md">
        {{ $t("dashboard.statistics") }}
      </h5>
      <div class="row">
        <statistics-cards />
      </div>

      <h5 class="q-ma-md">
        {{ $t("dashboard.usefulResources") }}
      </h5>
      <div class="row">
        <dashboard-card
          v-for="card in homepageCards"
          :key="card.title"
          class="col-12 col-sm-4"
          :title="card.title"
          :icon="card.icon"
          :description="card.description"
          :link-text="card.btn_text"
          :link-location="card.url"
          :router-link="card.routerLink ? card.routerLink : false"
        />
      </div>
    </div>
    <div v-else />
  </q-page>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import QuickActions from "components/QuickActions";
import { Platform } from "quasar";
import StatisticsCards from "components/StatisticsCards";
import DashboardCard from "../components/DashboardCard";

export default {
  name: "DashboardPage",
  components: { StatisticsCards, QuickActions, DashboardCard },
  computed: {
    Platform() {
      return Platform;
    },
    ...mapGetters("config", ["homepageCards", "features"]),
    ...mapGetters("profile", ["loggedIn", "profile"]),
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
  },
  async mounted() {
    await this.getProfile();
    if (
      this.profile.memberStatus === "Needs Induction" &&
      this.$route.name !== "membershipTier" &&
      this.features.stripe.enableMembershipPayments
    ) {
      this.$router.push({ name: "membershipTier" });
    }
  },
};
</script>

<style lang="sass" scoped>
.row
  width: 100%
  max-width: $maxWidth
  margin: auto
</style>
