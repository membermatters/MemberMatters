<template>
  <q-card class="my-card">
    <q-card-section class="row items-center q-pb-none">
      <q-space />
      <q-btn
        :icon="icons.close"
        flat
        round
        dense
        v-close-popup
      />
    </q-card-section>

    <q-card-section class="column flex items-start justify-start">
      <div
        class="column flex items-center justify-center q-pb-md"
        style="width: 100%;"
      >
        <h5 class="q-mb-md q-mt-none">
          {{ siteOwner }} {{ $t('digitalId.title') }}
        </h5>
        <q-avatar
          color="primary"
          text-color="white"
          class="q-my-lg text-h1"
        >
          <q-icon :name="icons.profile" />
        </q-avatar>
      </div>

      <div
        class="row"
        style="width: 100%;"
      >
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

      <div
        class="row"
        style="width: 100%;"
      >
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
import icons from '../icons';

export default {
  name: 'DigitalIdCard',
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
</style>
