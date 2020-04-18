import Vue from 'vue';
import VueI18n from 'vue-i18n';
import messages from 'src/i18n';
import numberFormats from 'src/i18n/numberFormats';

Vue.use(VueI18n);

const i18n = new VueI18n({
  locale: 'en-AU',
  fallbackLocale: 'en-AU',
  numberFormats,
  messages,
});

export default ({ app }) => {
  // Set i18n instance on app
  app.i18n = i18n;
};

export { i18n };
