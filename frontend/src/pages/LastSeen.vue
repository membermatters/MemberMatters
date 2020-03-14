<template>
  <q-page class="row flex content-start justify-center">
    <div>
      <div>
        <p class="q-pl-lg q-pt-lg q-pr-lg">
          {{ $t('lastseen.pageDescription') }}
        </p>
      </div>
      <last-seen-list />
    </div>
  </q-page>
</template>

<script>
import LastSeenList from '../components/LastSeenList';

export default {
  name: 'LastSeenPage',
  components: { LastSeenList },
};
</script>
