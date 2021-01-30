<template>
  <div class="row">
    <div class="q-pa-md col-12 col-sm-4">
      <q-card>
        <img src="https://hsbne.org/assets/img/carousel/00.jpg" />

        <q-list>
          <q-item clickable>
            <q-item-section avatar>
              <q-icon color="primary" :name="icons.members" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ $t("statistics.memberCount") }}</q-item-label>
              <q-item-label caption>
                {{ onsiteCount }} {{ $t("statistics.onSite") }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-item clickable>
            <q-item-section avatar>
              <q-icon color="primary" :name="icons.membersOnSite" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ $t("statistics.memberList") }}</q-item-label>
              <q-item-label caption>
                {{ onsiteMembers.join(", ") }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import icons from "@icons";

export default {
  name: "StatisticsCards",
  data() {
    return {
      refreshInterval: null,
    };
  },
  mounted() {
    this.getSiteSignedIn();
    this.getStatistics();

    // Refresh statistics every 10 seconds while the page is open
    this.refreshInterval = setInterval(this.getStatistics, 10000);
  },
  beforeDestroy() {
    clearInterval(this.refreshInterval);
  },
  methods: {
    ...mapActions("profile", ["getSiteSignedIn"]),
    ...mapActions("tools", ["getStatistics"]),
  },
  computed: {
    ...mapGetters("tools", ["statistics"]),
    icons() {
      return icons;
    },
    onsiteCount() {
      return this.statistics?.onSite ? this.statistics?.onSite?.count : 0;
    },
    onsiteMembers() {
      return this.statistics?.onSite?.members
        ? this.statistics?.onSite?.members
        : [];
    },
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
