<template>
  <q-page class="column flex justify-start items-center">
    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">
          {{ $t('menuLink.manageDoor') }}
        </div>
      </q-card-section>

      <q-card-section>
        <div class="column q-gutter-md q-px-sm">
          <q-input
            outlined
            v-model="door.name"
            :label="$t('doors.name')"
          />

          <q-input
            outlined
            v-model="door.description"
            :label="$t('doors.description')"
          />

          <q-input
            outlined
            v-model="door.ipAddress"
            :label="$t('form.ipAddress')"
          />

          <div class="column">
            <q-checkbox
              v-model="door.defaultAccess"
              :label="$t('access.defaultAccess')"
            />
            <q-checkbox
              v-model="door.maintenanceLockout"
              :label="$t('access.maintenanceLockout')"
            />
            <q-checkbox
              v-model="door.playThemeOnSwipe"
              :label="$t('access.playTheme')"
            />
            <q-checkbox
              v-model="door.exemptFromSignin"
              :label="$t('access.exemptSignin')"
            />
            <q-checkbox
              v-model="door.hiddenToMembers"
              :label="$t('access.hiddenToMembers')"
            />
          </div>

          <div class="row">
            <q-space />
            <q-btn
              :label="$t('doors.remove')"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
              :loading="removeLoading"
              :disabled="removeLoading"
              @click="removeDoor"
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
  name: 'ManageDoorPage',
  props: {
    doorId: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      removeLoading: false,
      door: {
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
    this.getDoors()
      .then(() => {
        if (this.currentDoor === false) this.$router.push({ name: 'Error404' });

        this.door.name = this.currentDoor.name;
        this.door.description = this.currentDoor.description;
        this.door.ipAddress = this.currentDoor.ipAddress;
        this.door.defaultAccess = this.currentDoor.defaultAccess;
        this.door.maintenanceLockout = this.currentDoor.maintenanceLockout;
        this.door.playThemeOnSwipe = this.currentDoor.playThemeOnSwipe;
        this.door.exemptFromSignin = this.currentDoor.exemptFromSignin;
        this.door.hiddenToMembers = this.currentDoor.hiddenToMembers;
      });
  },
  methods: {
    ...mapActions('adminTools', ['getDoors']),
    removeDoor() {
      this.$q.dialog({
        title: this.$t('confirmRemove'),
        ok: 'Ok',
        cancel: 'Cancel',
      }).onOk(() => {
        this.removeLoading = true;
        this.$axios.delete(`/api/admin/doors/${this.doorId}/`)
          .then(() => {
            this.$router.push({ name: 'doors' });
          })
          .catch((error) => {
            this.removeLoading = true;
            this.$q.dialog({
              title: this.$t('error.error'),
              message: this.$t('error.requestFailed'),
            });
            throw error;
          })
          .finally(() => {
            this.removeLoading = false;
          });
      });
    },
  },
  computed: {
    ...mapGetters('adminTools', ['doors']),
    icons() {
      return icons;
    },
    currentDoor() {
      const door = this.doors.find((item) => String(item.id) === this.doorId);

      return door || false;
    },
  },
};
</script>
