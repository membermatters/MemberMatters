<template>
  <q-page class="column flex justify-start items-center">
    <manage-member-bucks :dialog="dialog" />
  </q-page>
</template>

<script>
import ManageMemberBucks from 'components/MemberBucks';
import icons from '../icons';

export default {
  name: 'MemberBucks',
  components: { ManageMemberBucks },
  props: {
    dialog: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      text: '',
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
