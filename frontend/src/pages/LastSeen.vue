<template>
  <q-page class="flex content-start">
    <div>
      <div
        class="row"
        style="width: 100%;"
      >
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
