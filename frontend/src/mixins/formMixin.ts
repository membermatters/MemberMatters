import * as dayjs from "dayjs";

export default {
  methods: {
    validateEmail(email: string) {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    },
    validateNotEmpty(value: string) {
      return value !== null && value !== "";
    },
    validatePassword(value: string) {
      return value.length > 7;
    },
    validateMatchingField(current: string, newField: string) {
      return current === newField;
    },
    validateFutureDate(date: string) {
      return date >= dayjs().format("YYYY/MM/DD");
    },
    validateFutureTime(time: string) {
      return time >= dayjs().format("HH:MM");
    },
    validateFutureDateTime(date: string, disable: boolean) {
      if (disable) return true;
      return date >= dayjs().format("YYYY-MM-DD HH:MM");
    },
  },
  computed: {
    debounceLength() {
      return 1000;
    },
    intervalOptions() {
      return [
        { label: "day(s)", value: "day" },
        { label: "week(s)", value: "week" },
        { label: "month(s)", value: "month" },
        { label: "year(s)", value: "year" },
      ];
    },
  },
};
