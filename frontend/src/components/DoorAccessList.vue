<template>
  <div class="q-pa-md row flex content-start items-start">
    <q-list
      bordered
      padding
      class="rounded-borders q-ma-sm access-list"
    >
      <q-item-label header>
        {{ $t('access.doors') }}
      </q-item-label>

      <q-item
        v-for="door in doorAccess"
        :key="door.name"
      >
        <q-item-section
          avatar
          top
        >
          <q-avatar
            icon="fad fa-door-open"
            :color="door.access ? 'green' : 'red'"
            text-color="white"
          />
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">
            {{ door.name }}
          </q-item-label>
          <q-item-label
            caption
            v-if="door.access === true"
          >
            {{ $t('access.authorised') }}
          </q-item-label>
          <q-item-label
            caption
            v-else
          >
            {{ $t('access.unauthorised') }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>

    <q-list
      bordered
      padding
      class="rounded-borders q-ma-sm access-list"
    >
      <q-item-label header>
        {{ $t('access.interlocks') }}
      </q-item-label>

      <q-item
        v-for="interlock in interlockAccess"
        :key="interlock.name"
      >
        <q-item-section
          avatar
          top
        >
          <q-avatar
            icon="fad fa-door-open"
            :color="interlock.access ? 'green' : 'red'"
            text-color="white"
          />
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">
            {{ interlock.name }}
          </q-item-label>
          <q-item-label
            caption
            v-if="interlock.access === true"
          >
            {{ $t('access.authorised') }}
          </q-item-label>
          <q-item-label
            caption
            v-else
          >
            {{ $t('access.unauthorised') }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'DoorAccessList',
  methods: {
    ...mapActions('profile', ['getAccess']),
  },
  mounted() {
    this.getAccess();
    setInterval(() => {
      this.getAccess();
    }, 60000);
  },
  computed: {
    ...mapGetters('profile', ['doorAccess', 'interlockAccess']),
  },
};
</script>

<style lang="stylus" scoped>
  @media (max-width: $breakpoint-xs-max)
    .access-list
      width: 100%;
</style>
