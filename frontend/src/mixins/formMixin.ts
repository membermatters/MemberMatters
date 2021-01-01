import * as Moment from "moment";

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
      return date >= Moment().format("YYYY/MM/DD");
    },
    validateFutureTime(time: string) {
      return time >= Moment().format("HH:MM");
    },
    validateFutureDateTime(date: string, disable: boolean) {
      if (disable) return true;
      return date >= Moment().format("YYYY-MM-DD HH:MM");
    },
  },
  computed: {
    debounceLength() {
      return 1000;
    },
  },
};
