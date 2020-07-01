<template>
  <div class="row">
    <q-btn
      outline
      color="primary"
      :label="$t('adminTools.enableAccess')"
    />
  </div>
</template>

<script>
export default {
  name: 'ManageMember',
  components: {},
  props: {
    member: {
      type: Object,
      default: () => {},
    },
  },
};
</script>
