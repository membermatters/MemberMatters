export default {
  methods: {
    formatCsvList(list) {
      return list.map((x, i) => {
        if (list.length === i + 1) return x;
        return `${x}, `;
      });
    },
  },
};
