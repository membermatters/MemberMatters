<template>
  <q-page class="column flex content-center justify-start">
    <kiosk-list />
  </q-page>
</template>

<script>
import KioskList from '../components/KioskList';

export default {
  name: 'KiosksPage',
  components: { KioskList },
};
</script>
