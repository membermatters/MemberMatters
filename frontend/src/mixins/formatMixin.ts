import { utc } from "moment";

export default {
  methods: {
    formatCsvList(list: Array<string>) {
      return list.map((x, i) => {
        if (list.length === i + 1) return x;
        return `${x}, `;
      });
    },
    formatDate(date: Date, time = true) {
      if (time) return utc(date).local().format("Do MMM YYYY, h:mm a");
      return utc(date).local().format("Do MMM YYYY");
    },
    formatDateSimple(date: Date, time = true) {
      if (time) return utc(date).local().format("DD/MM/YY, h:mm a");
      return utc(date).local().format("Do MMM YYYY");
    },
    formatWhen(date: Date) {
      return utc(date).local().fromNow();
    },
    capitaliseFirst(value: string) {
      return (
        String(value) && String(value)[0].toUpperCase() + String(value).slice(1)
      );
    },
  },
};
