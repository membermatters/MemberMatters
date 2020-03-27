<template>
  <q-page class="column flex content-center justify-start">
    <p class="text-body1">
      {{ $t('lastseen.pageDescription') }}
    </p>
    <last-seen-list />
  </q-page>
</template>

<script>
import LastSeenList from '../components/LastSeenList';

export default {
  name: 'LastSeenPage',
  components: { LastSeenList },
};
</script>
