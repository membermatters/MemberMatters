<template>
  <div>
    <q-banner
      v-if="inactiveWarning"
      inline-actions
      rounded
      class="bg-orange text-white q-ma-md"
    >
      <template v-slot:avatar>
        <q-icon :name="icons.warning" />
      </template>
      {{ $t('access.inactive') }}
    </q-banner>
    <div class="row flex content-start items-start">
      <q-list bordered padding class="rounded-borders q-ma-sm access-list">
        <q-item-label header>
          {{ $t('access.doors') }}
        </q-item-label>

        <div class="q-pa-md" v-if="!doors.length">
          {{ $t('doors.nodata') }}
        </div>

        <div
          v-for="door in doors"
          :key="door.name"
          @click="
            door.access
              ? revoke('door', memberId, door.id)
              : authorise('door', memberId, door.id)
          "
        >
          <q-item>
            <q-item-section avatar top>
              <q-avatar
                :icon="icons.doorOpen"
                :color="
                  door.locked_out ? 'orange' : door.access ? 'green' : 'red'
                "
                text-color="white"
              />
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1">
                {{ door.name }}
              </q-item-label>
              <q-item-label v-if="door.locked_out === true" caption>
                <div>{{ $t('access.maintenance') }}</div>
                <div v-if="door.access === true">
                  ({{ $t('access.authorised') }})
                </div>
                <div v-else>({{ $t('access.unauthorised') }})</div>
              </q-item-label>
              <q-item-label v-else-if="door.access === true" caption>
                {{ $t('access.authorised') }}
              </q-item-label>
              <q-item-label v-else caption>
                {{ $t('access.unauthorised') }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </q-list>

      <q-list bordered padding class="rounded-borders q-ma-sm access-list">
        <q-item-label header>
          {{ $t('access.interlocks') }}
        </q-item-label>

        <q-item-label class="q-pa-md" v-if="!interlocks.length">
          {{ $t('interlocks.nodata') }}
        </q-item-label>

        <div
          v-for="interlock in interlocks"
          :key="interlock.name"
          @click="
            interlock.access
              ? revoke('interlock', memberId, interlock.id)
              : authorise('interlock', memberId, interlock.id)
          "
        >
          <q-item>
            <q-item-section avatar top>
              <q-avatar
                :icon="icons.interlock"
                :color="
                  interlock.locked_out
                    ? 'orange'
                    : interlock.access
                    ? 'green'
                    : 'red'
                "
                text-color="white"
              />
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1">
                {{ interlock.name }}
              </q-item-label>
              <q-item-label v-if="interlock.locked_out === true" caption>
                {{ $t('access.maintenance') }}
                <div v-if="door.access === true">
                  ({{ $t('access.authorised') }})
                </div>
                <div v-else>({{ $t('access.unauthorised') }})</div>
              </q-item-label>
              <q-item-label v-else-if="interlock.access === true" caption>
                {{ $t('access.authorised') }}
              </q-item-label>
              <q-item-label v-else caption>
                {{ $t('access.unauthorised') }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </q-list>

      <refresh-data-dialog v-model="errorLoading" />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import RefreshDataDialog from '@components/RefreshDataDialog.vue';
import icons from '@icons';

export default {
  name: 'AccessList',
  components: { RefreshDataDialog },
  props: {
    memberId: {
      type: Number,
      default: null,
    },
    inactiveWarning: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      errorLoading: false,
      access: {},
    };
  },
  computed: {
    ...mapGetters('profile', ['doorAccess', 'interlockAccess']),
    icons() {
      return icons;
    },
    doors() {
      if (this.memberId && this.access.doors !== undefined)
        return this.access.doors;
      else return this.doorAccess;
    },
    interlocks() {
      if (this.memberId && this.access.interlocks !== undefined)
        return this.access.interlocks;
      else return this.interlockAccess;
    },
  },

  watch: {
    memberId() {
      this.getMemberAccess();
    },
  },
  mounted() {
    if (this.memberId) {
      this.getMemberAccess();
    } else {
      this.getAccess();
    }
  },
  methods: {
    ...mapActions('profile', ['getAccess']),
    /**
     * this method returns a specific user's access permissions
     */
    getMemberAccess() {
      this.$axios
        .get(`/api/admin/members/${this.memberId}/access/`)
        .then((response) => {
          this.access = response.data;
        })
        .catch((error) => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
          throw error;
        });
    },
    authorise(type, memberId, deviceId) {
      if (!this.memberId) return;
      const device = type === 'interlock' ? 'interlocks' : 'doors';
      this.$axios
        .put(`/api/access/${device}/${deviceId}/authorise/${memberId}/`)
        .then(() => {
          this.getMemberAccess();
        })
        .catch((error) => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
          throw error;
        });
    },
    revoke(type, memberId, deviceId) {
      if (!this.memberId) return;
      const device = type === 'interlock' ? 'interlocks' : 'doors';
      this.$axios
        .put(`/api/access/${device}/${deviceId}/revoke/${memberId}/`)
        .then(() => {
          this.getMemberAccess();
        })
        .catch((error) => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
          throw error;
        });
    },
  },
};
</script>

<style lang="sass" scoped>
@media (max-width: $breakpoint-xs-max)
  .access-list
    width: 100%
</style>
