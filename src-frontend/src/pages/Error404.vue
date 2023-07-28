<template>
  <div class="fixed-center text-center">
    <p>
      <sad-face />
    </p>
    <p class="text-body1 text-faded">
      {{ $t('error.404') }}
    </p>
    <q-btn
      color="primary-btn"
      style="width: 200px"
      :to="{ name: 'dashboard' }"
      label="Go Home"
    />
  </div>
</template>

<script>
import SadFace from '@components/SadFace.vue';

export default {
  name: 'Error-404',
  components: { SadFace },
};
</script>
