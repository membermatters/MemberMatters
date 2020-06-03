import Vue from 'vue';
import * as Sentry from '@sentry/browser';
import { Vue as VueIntegration } from '@sentry/integrations';

Sentry.init({
  dsn: 'https://c1c9e0f7f7984b1e916794b262897879@o402264.ingest.sentry.io/5263083',
  integrations: [new VueIntegration({ Vue, attachProps: true })],
});
