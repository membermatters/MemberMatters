import { boot } from "quasar/wrappers";
import { createI18n } from "vue-i18n";

import messages from "../i18n";
import numberFormats from "../i18n/numberFormats";

export const i18n = createI18n({
  locale: "en-AU",
  fallbackLocale: "en-AU",
  numberFormats,
  messages,
});

export default boot(({ app }) => {
  // Set i18n instance on app
  app.use(i18n);
});
