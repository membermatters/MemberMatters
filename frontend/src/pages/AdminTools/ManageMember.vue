<template>
  <div class="row">
    <q-btn
      v-if="selectedMember.state==='Inactive'"
      class="q-mr-sm"
      color="positive"
      :label="$t('adminTools.enableAccess')"
      @click="setMemberState('active')"
      :loading="stateLoading"
    />
    <q-btn
      v-else-if="selectedMember.state==='New'"
      class="q-mr-sm"
      color="primary"
      :label="$t('adminTools.makeMember')"
      @click="activateMember()"
      :loading="stateLoading"
    />
    <q-btn
      v-else
      class="q-mr-sm"
      color="negative"
      :label="$t('adminTools.disableAccess')"
      @click="setMemberState('inactive')"
      :loading="stateLoading"
    />
  </div>
</template>

<script>
export default {
  name: 'ManageMember',
  components: {},
  data() {
    return {
      stateLoading: false,
    };
  },
  props: {
    member: {
      type: Object,
      default: () => {},
    },
    members: {
      type: Array,
      default: () => {},
    },
  },
  methods: {
    setMemberState(state) {
      this.stateLoading = true;
      this.$axios.post(`/api/admin/members/${this.member.id}/state/${state}/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('updateMembers');
          setTimeout(() => { this.stateLoading = false; }, 1200);
        });
    },
    activateMember() {
      this.stateLoading = true;
      this.$axios.post(`/api/admin/members/${this.member.id}/makemember/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('updateMembers');
          setTimeout(() => { this.stateLoading = false; }, 1200);
        });
    },
  },
  computed: {
    selectedMember() {
      if (this.members) {
        return this.members.find((e) => e.id === this.member.id);
      }
      return this.member;
    },
  },
};
</script>
