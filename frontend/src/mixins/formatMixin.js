import Moment from 'moment';

export default {
  methods: {
    formatCsvList(list) {
      return list.map((x, i) => {
        if (list.length === i + 1) return x;
        return `${x}, `;
      });
    },
    formatDate(date) {
      return Moment.utc(date).local().format('Do MMM YYYY, h:mm a');
    },
    formatWhen(date) {
      return Moment.utc(date).local().fromNow();
    },
  },
};
