<template>
  <q-page class="column flex justify-start items-center">
    <div class="column flex content-start justify-center">
      <q-banner
          v-if="profile.lastInduction === null"
          inline-actions
          rounded
          class="bg-red text-white q-ma-md"
        >
          <template v-slot:avatar>
            <q-icon :name="icons.warning" />
          </template>
          <div v-if="profile.inductionLink.length != 0">
            {{ $t('access.inductionIncompleteTasks') }}
            <li v-for="(link, index) in profile.inductionLink" :key="index">
              <a :href="link" target="_blank">Task {{ index+1 }}</a>
            </li>
          </div>
          <div v-else>{{ $t('access.inductionIncompleteNoTasks') }}</div>
        </q-banner>

      <q-banner
        v-if="
          profile.memberStatus !== 'active' &&
          profile.memberStatus !== 'accountonly'
        "
        inline-actions
        rounded
        class="bg-orange text-white q-ma-md"
      >
        <template v-slot:avatar>
          <q-icon :name="icons.warning" />
        </template>
        {{ $t('access.inactive') }}
      </q-banner>

      <q-banner
        v-if="profile.memberStatus === 'Account Only'"
        inline-actions
        rounded
        class="bg-blue text-white q-ma-md"
      >
        <template v-slot:avatar>
          <q-icon :name="icons.info" />
        </template>
        {{ $t('paymentPlans.profileAccountOnlyWarning') }}
      </q-banner>
    </div>

    <profile-form class="q-mb-lg" />

    <q-btn-group push>
      <q-btn
        push
        color="toolbar"
        label="Digital ID"
        @click="digitalId = true"
      />
      <q-btn
        push
        color="primary"
        label="Change Password"
        @click="changePassword = true"
      />
    </q-btn-group>

    <a v-if="features.enableDocusealMemberDocs"
      :href="profile.memberdocsLink"
      >Download Membership Agreement</a>

    <q-dialog v-model="digitalId">
      <digital-id-card />
    </q-dialog>

    <q-dialog v-model="changePassword">
      <change-password-card />
    </q-dialog>
  </q-page>
</template>

<script>
import ProfileForm from '@components/ProfileForm.vue';
import icons from '../icons';
import DigitalIdCard from '@components/DigitalIdCard.vue';
import ChangePasswordCard from '@components/ChangePasswordCard.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'ProfilePage',
  components: { ChangePasswordCard, DigitalIdCard, ProfileForm },
  data() {
    return {
      text: '',
      digitalId: false,
      changePassword: false,
    };
  },
  computed: {
    ...mapGetters('profile', ['loggedIn', 'profile']),
    ...mapGetters('config', ['features']),
    icons() {
      return icons;
    },
  },
};


</script>
