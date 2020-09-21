<template>
  <q-page class="column flex content-center justify-start">
    <interlocks-list />
  </q-page>
</template>

<script>
import InterlocksList from 'components/AdminTools/InterlocksList';

export default {
  name: 'ManageDoors',
  components: { InterlocksList },
};
</script>
