<template>
  <q-card class="my-card">
    <q-card-section class="row items-center q-pb-none">
      <q-space />
      <q-btn v-close-popup :icon="icons.close" flat round dense />
    </q-card-section>

    <q-card-section class="column flex items-start justify-start">
      <div class="column flex content-start justify-center">
        <q-banner
          v-if="profile.memberStatus !== 'active'"
          inline-actions
          rounded
          class="bg-orange text-white q-ma-md"
        >
          <template v-slot:avatar>
            <q-icon :name="icons.info" />
          </template>
          {{ $t('digitalId.inactiveMember') }}
        </q-banner>
      </div>

      <div
        class="column flex items-center justify-center q-pb-md"
        style="width: 100%"
      >
        <h5 class="q-mb-md q-mt-none">
          {{ siteOwner }} {{ $t('digitalId.title') }}
        </h5>
        <q-img class="qrcode" :src="qrcode" />
      </div>

      <div class="row" style="width: 100%">
        <div class="col-6">
          <h6 class="q-mb-none q-mt-sm">
            {{ $t('digitalId.fullName') }}
          </h6>
          <div class="text-body1">
            {{ profile.fullName }}
          </div>
        </div>
        <div class="col-6">
          <h6 class="q-mb-none q-mt-sm">
            {{ $t('digitalId.memberState') }}
          </h6>
          <div class="text-body1">
            {{ profile.memberStatus }}
          </div>
        </div>
      </div>

      <div class="row" style="width: 100%">
        <div class="col-6">
          <h6 class="q-mb-none q-mt-sm">
            {{ $t('digitalId.memberId') }}
          </h6>
          <div class="text-body1">
            {{ profile.id }}
          </div>
        </div>
        <div class="col-6">
          <h6 class="q-mb-none q-mt-sm">
            {{ $t('digitalId.memberSince') }}
          </h6>
          <div class="text-body1">
            {{ profile.firstJoined }}
          </div>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters } from 'vuex';
import QRCode from 'qrcode';
import icons from '../icons';

export default {
  name: 'DigitalIdCard',
  data() {
    return {
      qrcode: '',
    };
  },
  mounted() {
    this.getIdToken();
  },
  methods: {
    getIdToken() {
      this.$axios.get('/api/profile/idtoken/').then((result) => {
        QRCode.toDataURL(result.data.token, async (err, url) => {
          this.qrcode = url;
        });
      });
    },
  },
  computed: {
    ...mapGetters('config', ['siteOwner']),
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
.my-card
  width: 100vw
  max-width: 400px
  text-transform: capitalize

.disclaimer
  text-transform: none

.qrcode
  max-width: 200px
</style>
