<template>
  <q-page class="column flex content-center justify-start">
    <doors-list />
  </q-page>
</template>

<script>
import DoorsList from 'components/AdminTools/DoorsList';

export default {
  name: 'ManageDoors',
  components: { DoorsList },
};
</script>
