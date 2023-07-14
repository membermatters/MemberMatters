<template>
  <q-page class="column flex justify-start items-center">
    <manage-member
      v-if="currentMember"
      :members="members"
      :member="currentMember"
      @memberUpdated="getMembers"
    />
    <error404 v-else-if="!currentMember && members.length" />
  </q-page>
</template>

<script lang="ts">
import icons from '@icons';
import ManageMember from '@components/AdminTools/ManageMember.vue';
import Error404 from 'pages/Error404.vue';
import { MemberProfile } from 'types/member';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ManageMemberPage',
  components: {
    Error404,
    ManageMember,
  },
  props: {
    memberId: {
      type: [String, Number],
      default: '',
    },
  },
  data() {
    return {
      members: [],
    };
  },
  beforeRouteLeave(to, from, next) {
    this.getMembers();
    next();
  },
  computed: {
    icons() {
      return icons;
    },
    currentMember() {
      const member = this.members.find(
        (member: MemberProfile) => String(member.id) === String(this.memberId)
      );

      return member || false;
    },
  },
  created() {
    this.getMembers();
  },
  methods: {
    getMembers() {
      this.$axios
        .get('/api/admin/members/')
        .then((response) => {
          this.members = response.data;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        });
    },
  },
});
</script>
