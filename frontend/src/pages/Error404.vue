<template>
  <div class="fixed-center text-center">
    <p>
      <sad-face />
    </p>
    <p class="text-faded">
      {{ $t('error.404') }}
    </p>
    <q-btn
      color="primary-btn"
      style="width:200px;"
      to="/"
      label="Go Home"
    />
  </div>
</template>

<script>
import SadFace from '../components/SadFace';

export default {
  name: 'Error404',
  components: { SadFace },
};
</script>
