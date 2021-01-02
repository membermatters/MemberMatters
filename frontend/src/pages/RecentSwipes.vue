<template>
  <q-page class="column flex content-center justify-start">
    <p class="text-body1 q-pl-lg q-pt-lg q-pr-lg">
      {{ $t('recentSwipes.pageDescription') }}
    </p>
    <recent-swipes-list />
  </q-page>
</template>

<script>
import RecentSwipesList from "../components/RecentSwipesList";

export default {
  name: "RecentSwipesPage",
  components: { RecentSwipesList },
};
</script>
