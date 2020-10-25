<template>
  <div class="row flex content-start items-start">
    <q-list
      bordered
      padding
      class="rounded-borders q-ma-sm access-list"
    >
      <q-item-label header>
        {{ $t('access.doors') }}
      </q-item-label>

      <div
        v-for="door in doors"
        :key="door.name"
        @click="door.access ? revoke('door', memberId, door.id) :
          authorise('door', memberId, door.id)"
      >
        <q-item>
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
              v-if="door.access === true"
              caption
            >
              {{ $t('access.authorised') }}
            </q-item-label>
            <q-item-label
              v-else
              caption
            >
              {{ $t('access.unauthorised') }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </q-list>

    <q-list
      bordered
      padding
      class="rounded-borders q-ma-sm access-list"
    >
      <q-item-label header>
        {{ $t('access.interlocks') }}
      </q-item-label>

      <div
        v-for="interlock in interlocks"
        :key="interlock.name"
        @click="interlock.access ? revoke('interlock', memberId, interlock.id) :
          authorise('interlock', memberId, interlock.id)"
      >
        <q-item>
          <q-item-section
            avatar
            top
          >
            <q-avatar
              icon="fad fa-tools"
              :color="interlock.access ? 'green' : 'red'"
              text-color="white"
            />
          </q-item-section>

          <q-item-section>
            <q-item-label lines="1">
              {{ interlock.name }}
            </q-item-label>
            <q-item-label
              v-if="interlock.access === true"
              caption
            >
              {{ $t('access.authorised') }}
            </q-item-label>
            <q-item-label
              v-else
              caption
            >
              {{ $t('access.unauthorised') }}
            </q-item-label>
          </q-item-section>
        </q-item>
      </div>
    </q-list>

    <refresh-data-dialog v-model="errorLoading" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import RefreshDataDialog from './RefreshDataDialog';

export default {
  name: 'AccessList',
  components: { RefreshDataDialog },
  props: {
    memberId: {
      type: Number,
      default: null,
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
    doors() {
      return this.memberId ? this.access.doors : this.doorAccess;
    },
    interlocks() {
      return this.memberId ? this.access.interlocks : this.interlockAccess;
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
      this.$axios.get(`/api/admin/members/${this.memberId}/access/`)
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
      this.$axios.put(`api/access/${device}/${deviceId}/authorise/${memberId}/`)
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
      this.$axios.put(`api/access/${device}/${deviceId}/revoke/${memberId}/`)
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

<style lang="stylus" scoped>
  @media (max-width: $breakpoint-xs-max)
    .access-list
      width: 100%;
</style>
