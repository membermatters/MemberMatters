<template>
  <q-page class="row flex content-start justify-center">
    <div style="width: 100%;">
      <div
        class="row"
        style="width: 100%;"
      >
        <p class="q-pl-lg q-pt-lg q-pr-lg">
          {{ $t('recentSwipes.pageDescription') }}
        </p>
      </div>
      <recent-swipes-list />
    </div>
  </q-page>
</template>

<script>
import RecentSwipesList from '../components/RecentSwipesList';

export default {
  name: 'RecentSwipesPage',
  components: { RecentSwipesList },
};
</script>
