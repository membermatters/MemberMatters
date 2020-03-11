<template>
  <div class="fixed-center text-center">
    <p>
      <sad-face />
    </p>
    <p class="text-faded">
      {{ $t('error.403') }}
    </p>
    <q-btn
      color="primary"
      style="width:200px;"
      to="/"
      label="Go Home"
    />
  </div>
</template>

<script>
import SadFace from '../components/SadFace';

export default {
  name: 'Error403',
  components: { SadFace },
};
</script>
