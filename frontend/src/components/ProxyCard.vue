<template>
  <q-card class="q-pa-md card">
    <i18n
      path="proxyForm.proxyTo"
      tag="p"
    >
      <template v-slot:siteOwner>
        <span>{{ siteOwner }}</span>
      </template>
    </i18n>

    <i18n
      path="proxyForm.proxyBody"
      tag="p"
    >
      <template v-slot:memberName>
        <span class="proxy-field">{{ profile.fullName }}</span>
      </template>
      <template v-slot:memberCity>
        <span class="proxy-field">{{ proxyCardInfo.memberCity }}</span>
      </template>
      <template v-slot:proxyName>
        <span class="proxy-field">{{ proxyCardInfo.proxy.name }}</span>
      </template>
      <template v-slot:proxyCity>
        <span class="proxy-field">{{ proxyCardInfo.proxy.city }}</span>
      </template>
      <template v-slot:meetingName>
        <span class="proxy-field">{{ proxyCardInfo.meeting.name }}</span>
      </template>
      <template v-slot:meetingDate>
        <span class="proxy-field">{{ proxyCardInfo.meeting.date }}</span>
      </template>
    </i18n>

    <i18n
      path="proxyForm.proxySignature"
      tag="p"
    >
      <template v-slot:memberName>
        <span class="proxy-field">{{ profile.fullName }}</span>
      </template>
      <template v-slot:currentDate>
        <span class="proxy-field">{{ currentDate }}</span>
      </template>
    </i18n>
  </q-card>
</template>

<script>
import { mapGetters } from 'vuex';
import Moment from 'moment';
import icons from '../icons';

export default {
  name: 'ProxyCard',
  props: {
    proxyCardInfo: {
      type: Object,
      default: () => { {} },
    },
  },
  computed: {
    ...mapGetters('config', ['siteOwner']),
    ...mapGetters('profile', ['profile']),
    currentDate() {
      return Moment().format('Do MMMM YYYY');
    },
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
  .card
    max-width: 400px

  .proxy-field
    font-style: italic
    font-weight: bold
    text-decoration: underline
</style>
