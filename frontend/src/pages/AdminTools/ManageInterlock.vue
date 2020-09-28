<template>
  <q-page class="column flex justify-start items-center">
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">
          {{ $t('menuLink.manageInterlock') }}
        </div>
      </q-card-section>

      <q-card-section>
        <div class="column q-gutter-md q-px-sm">
          <q-input
            outlined
            v-model="interlock.name"
            :label="$t('interlocks.name')"
          />

          <q-input
            outlined
            v-model="interlock.description"
            :label="$t('interlocks.description')"
          />

          <q-input
            outlined
            v-model="interlock.ipAddress"
            :label="$t('form.ipAddress')"
          />

          <div class="column">
            <q-checkbox
              v-model="interlock.defaultAccess"
              :label="$t('access.defaultAccess')"
            />
            <q-checkbox
              v-model="interlock.maintenanceLockout"
              :label="$t('access.maintenanceLockout')"
            />
            <q-checkbox
              v-model="interlock.playThemeOnSwipe"
              :label="$t('access.playTheme')"
            />
            <q-checkbox
              v-model="interlock.exemptFromSignin"
              :label="$t('access.exemptSignin')"
            />
            <q-checkbox
              v-model="interlock.hiddenToMembers"
              :label="$t('access.hiddenToMembers')"
            />
          </div>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('interlocks.remove')"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import icons from '@icons';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'ManageInterlockPage',
  props: {
    interlockId: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      interlock: {
        name: '',
        description: '',
        ipAddress: '',
        defaultAccess: null,
        maintenanceLockout: null,
        playThemeOnSwipe: null,
        exemptFromSignin: null,
        hiddenToMembers: null,
      },
    };
  },
  mounted() {
    this.getInterlocks()
      .then(() => {
        if (this.currentInterlock === false) this.$router.push({ name: 'Error404' });

        this.interlock.name = this.currentInterlock.name;
        this.interlock.description = this.currentInterlock.description;
        this.interlock.ipAddress = this.currentInterlock.ipAddress;
        this.interlock.defaultAccess = this.currentInterlock.defaultAccess;
        this.interlock.maintenanceLockout = this.currentInterlock.maintenanceLockout;
        this.interlock.playThemeOnSwipe = this.currentInterlock.playThemeOnSwipe;
        this.interlock.exemptFromSignin = this.currentInterlock.exemptFromSignin;
        this.interlock.hiddenToMembers = this.currentInterlock.hiddenToMembers;
      });
  },
  methods: {
    ...mapActions('adminTools', ['getInterlocks']),
  },
  computed: {
    ...mapGetters('adminTools', ['interlocks']),
    icons() {
      return icons;
    },
    currentInterlock() {
      const interlock = this.interlocks.find((item) => String(item.id) === this.interlockId);

      return interlock || false;
    },
  },
};
</script>
