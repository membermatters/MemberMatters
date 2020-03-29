<template>
  <q-page class="row flex content-start justify-center">
    <proxy-form />
  </q-page>
</template>

<script>
import ProxyForm from '../components/ProxyForm';

export default {
  name: 'ProxyPage',
  components: { ProxyForm },
};
</script>
