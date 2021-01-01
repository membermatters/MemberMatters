<template>
  <div>
    <q-icon
      color="primary-btn"
      :name="icons.sadFace"
      style="font-size: 800%;"
    />
  </div>
</template>

<script>
import icons from "../icons";

export default {
  name: "SadFace",
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
