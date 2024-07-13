<template>
  <apexchart
    style="width: 100%"
    type="line"
    :options="options"
    :series="series"
  ></apexchart>
</template>

<script>
import formatMixin from 'src/mixins/formatMixin';

export default {
  name: 'MetricsGraph',
  mixins: [formatMixin],
  props: {
    metricsData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {};
  },
  computed: {
    options() {
      return {
        chart: {
          id: 'metrics-graph',
        },
        xaxis: {
          categories: this.metricsData.map((item) =>
            this.formatDate(item.date)
          ),
        },
        theme: {
          mode: this.$q.dark.isActive ? 'dark' : 'light',
        },
        yaxis: {
          labels: {
            formatter: function (val) {
              return val.toFixed(0);
            },
            min: 0,
          },
        },
      };
    },
    series() {
      let states = {};
      this.metricsData.map((item) => {
        if (Array.isArray(item.data)) {
          item.data.forEach((state) => {
            if (!state?.state && !state?.type) return;
            if (states[state?.state ?? state?.type] === undefined) {
              states[state?.state ?? state?.type] = [];
            }
            states[state?.state ?? state?.type].push(state.total);
          });
        } else {
          if (states['value'] === undefined) {
            states['value'] = [];
          }
          states['value'].push(item.data.value);
        }
      });
      return Object.keys(states).map((state) => {
        return {
          name: state,
          data: states[state],
        };
      });
    },
  },
};
</script>
