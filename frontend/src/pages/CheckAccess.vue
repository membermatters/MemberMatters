<template>
  <q-page class="row flex content-start justify-center">
    <div
      class="row"
      style="width: 100%;"
    >
      <p class="page-description q-pa-lg">
        {{ $t('access.pageDescription') }}
      </p>
    </div>
    <div class="column flex content-start justify-center">
      <q-banner
        v-if="profile.memberStatus !== 'active'"
        inline-actions
        rounded
        class="bg-orange text-white q-ma-md"
      >
        <template v-slot:avatar>
          <q-icon
            :name="icons.warning"
          />
        </template>
        {{ $t('access.inactive') }}
      </q-banner>

      <door-access-list />
    </div>
  </q-page>
</template>

<script>
import { mapGetters } from 'vuex';
import DoorAccessList from '../components/AccessList';
import icons from '../icons';

export default {
  name: 'CheckAccessPage',
  components: { DoorAccessList },
  computed: {
    ...mapGetters('profile', ['profile']),
    icons() {
      return icons;
    },
  },
};
</script>

<style scoped>
  .page-description {
    max-width: 600px;
    margin: 0 auto;
  }
</style>
