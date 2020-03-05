<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
  watch: {
    $route(to) {
      document.title = `${to.meta.title || 'MemberMatters'} | MemberMatters`;
    },
  },
};
</script>
