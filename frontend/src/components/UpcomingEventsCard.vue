<template>
  <div>
    <q-card class="upcoming-events-card">
      <h6 class="q-ma-none q-pa-md">
        {{ $t("upcomingEvents.pageDescription") }}
      </h6>

      <q-card-section>
        <q-list>
          <q-item v-for="event in upcomingEvents" :key="event.name">
            <q-item-section>
              <q-item-label>
                {{ event.name }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import icons from "../icons";
import { mapActions, mapGetters } from "vuex";

export default {
  name: "UpcomingEventsCard",
  data() {
    return {
      events: [],
    };
  },
  computed: {
    ...mapGetters("tools", ["upcomingEvents"]),
    icons() {
      return icons;
    },
  },
  mounted() {
    this.getUpcomingMeetings();
    console.log("UPCOMING");
  },
  methods: {
    ...mapActions("tools", ["getUpcomingMeetings"]),
  },
};
</script>

<style lang="sass" scoped>
.submit-issue-card
  min-width: $minWidth
</style>
