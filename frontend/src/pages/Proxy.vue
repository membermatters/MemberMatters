<template>
  <q-page class="row flex content-start justify-center">
    <proxy-list />
  </q-page>
</template>

<script>
import ProxyList from "../components/ProxyList";

export default {
  name: "ProxyPage",
  components: { ProxyList },
};
</script>
