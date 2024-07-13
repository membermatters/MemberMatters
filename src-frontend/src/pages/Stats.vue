<template>
  <q-page class="row flex content-start justify-center q-mt-md">
    <div class="row flex flex-center">
      <p class="text-body1 col-12 q-px-md q-pt-md">
        {{ $t('stats.internalStatsDescription') }}
      </p>

      <q-banner
        v-if="!features.enableStatsPage"
        inline-actions
        rounded
        class="bg-orange text-white q-ma-md"
      >
        <template v-slot:avatar>
          <q-icon :name="icons.warning" />
        </template>
        {{ $t('stats.disabled') }}
      </q-banner>

      <template v-if="StatisticsLoaded">
        <template v-for="(value, key) in this.statistics" :key="key">
          <div v-if="key !== 'on_site'" class="col-lg-6 col-12 q-px-md q-pt-md">
            <q-card class="full-width">
              <q-card-section>
                <div class="row flex flex-center">
                  <div
                    class="col-12 q-px-md q-pt-md row flex items-center justify-start"
                  >
                    <div class="q-mr-md">
                      <q-icon :name="icons[key]" size="40px" />
                    </div>
                    <div class="text-h6">{{ $t(`stats.${key}`) }}</div>
                  </div>
                  <div class="col-12 q-px-md q-pt-md">
                    <MetricsGraph :metricsData="value" />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </template>
      </template>
      <div v-else>
        {{ $t('stats.errorLoading') }}
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import icons from '@icons';
import MetricsGraph from 'components/MetricsGraph.vue';
import { MetricsApiSchema } from 'types/api/metrics';

export default {
  name: 'StatsPage',
  components: { MetricsGraph },
  data() {
    return {
      statsData: {},
    };
  },
  mounted() {
    this.getStatistics();
  },
  methods: {
    ...mapActions('tools', ['getStatistics']),
  },
  computed: {
    StatisticsLoaded() {
      return Object.keys(this.statistics).length > 0;
    },
    ...mapGetters('tools', ['statistics']),
    ...mapGetters('config', ['features']),
    icons() {
      return icons;
    },
  },
};
</script>

<style scoped>
.row {
  width: 100%;
  max-width: 100vw;
}
</style>
