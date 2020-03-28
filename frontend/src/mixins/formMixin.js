export default {
  methods: {
    validateEmail(email) {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    },
    validateNotEmpty(value) {
      return value !== null && value !== '';
    },
    validatePassword(value) {
      return value.length > 7;
    },
    validateMatchingField(current, newField) {
      return current === newField;
    },
  },
  computed: {
    debounceLength() {
      return 1000;
    },
  },
};
