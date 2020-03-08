<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  watch: {
    $route(to) {
      document.title = `${to.meta.title || 'MemberMatters'} | MemberMatters`;
    },
  },
  mounted() {
    // This sets the default axios base URL to the django dev server if we're on the dev server
    // eslint-disable-next-line no-restricted-globals
    if (location.port === '8080') {
      // eslint-disable-next-line no-restricted-globals
      axios.defaults.baseURL = `http://${location.hostname}:8000`;
    }
  },
};
</script>
