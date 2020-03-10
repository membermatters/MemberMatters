<template>
  <div class="fixed-center text-center">
    <p>
      <img
        src="~assets/sad.svg"
        style="width:30vw;max-width:150px;"
      >
    </p>
    <p class="text-faded">
      {{ $t('error.403') }}
    </p>
    <q-btn
      color="secondary"
      style="width:200px;"
      to="/"
      label="Go Home"
    />
  </div>
</template>

<script>
export default {
  name: 'Error403',
};
</script>
