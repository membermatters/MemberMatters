import Moment from 'moment';

export default {
  methods: {
    formatCsvList(list) {
      return list.map((x, i) => {
        if (list.length === i + 1) return x;
        return `${x}, `;
      });
    },
    formatDate(date, time = true) {
      if (time) return Moment.utc(date).local().format('Do MMM YYYY, h:mm a');
      return Moment.utc(date).local().format('Do MMM YYYY');
    },
    formatWhen(date) {
      return Moment.utc(date).local().fromNow();
    },
    capitaliseFirst(value) {
      return String(value) && String(value)[0].toUpperCase() + String(value).slice(1);
    },
  },
};
