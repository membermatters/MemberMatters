<template>
  <q-page class="flex flex-start">
    <div
      class="row"
      style="width: 100%;"
    >
      <p class="q-pl-lg q-pt-lg q-pr-lg">
        {{ $t('access.pageDescription') }}
      </p>
    </div>
    <div class="row">
      <door-access-list />
    </div>
  </q-page>
</template>

<script>
import DoorAccessList from '../components/DoorAccessList';

export default {
  name: 'CheckAccessPage',
  components: { DoorAccessList },
};
</script>
