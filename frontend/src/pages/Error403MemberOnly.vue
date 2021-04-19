<template>
  <div class="fixed-center text-center">
    <p>
      <sad-face />
    </p>
    <p class="text-body1 text-faded">
      {{ $t('error.403MemberOnly') }}
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
import SadFace from "../components/SadFace";

export default {
  name: "Error403MemberOnly",
  components: { SadFace },
};
</script>
