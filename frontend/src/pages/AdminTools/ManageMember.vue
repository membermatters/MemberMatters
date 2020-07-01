<template>
  <div class="row">
    <q-btn
      class="q-mr-sm"
      color="positive"
      :label="$t('adminTools.enableAccess')"
    />
    <q-btn
      class="q-mr-sm"
      color="negative"
      :label="$t('adminTools.disableAccess')"
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
  mounted() {
    console.log(this.member);
  },
};
</script>
