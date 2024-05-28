<template>
  <q-page class="column flex content-center" style="width: 100%">
    <q-card
      class="q-mb-none q-tabs"
      style="background-color: transparent"
      :class="{ 'q-pb-lg': $q.screen.xs }"
    >
      <q-tabs
        v-model="tab"
        align="justify"
        narrow-indicator
        class="bg-primary text-white"
      >
        <q-tab name="doors" :label="$t('access.doors')" />
        <q-tab name="interlocks" :label="$t('access.interlocks')" />
        <q-tab name="memberbucks" :label="$t('access.memberbucksDevices')" />
      </q-tabs>
      <q-separator />
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="doors" class="full-width">
          <devices-list
            deviceChoice="doors"
            :tableData="doors"
            @openDevice="manageDevice"
          ></devices-list>
        </q-tab-panel>
        <q-tab-panel name="interlocks" style="width: 100%">
          <devices-list
            deviceChoice="interlocks"
            :tableData="interlocks"
            @openDevice="manageDevice"
          ></devices-list>
        </q-tab-panel>
        <q-tab-panel name="memberbucks" style="width: 100%">
          <devices-list
            deviceChoice="memberbucks-devices"
            :tableData="memberbucksDevices"
            @openDevice="manageDevice"
          ></devices-list>
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import DevicesList from '@components/AdminTools/DevicesList.vue';
import DeviceDialog from '@components/AdminTools/DeviceDialog.vue';

export default {
  name: 'ManageDevices',
  components: { DevicesList },
  data() {
    return {
      tab: 'doors',
      interval: null,
    };
  },
  computed: {
    ...mapGetters('adminTools', ['interlocks', 'doors', 'memberbucksDevices']),
  },
  beforeMount() {
    this.getDoors();
    this.getInterlocks();
    this.getMemberbucksDevices();

    this.interval = setInterval(() => {
      this.getDoors();
      this.getInterlocks();
      this.getMemberbucksDevices();
    }, 30 * 1000);
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    ...mapActions('adminTools', [
      'getInterlocks',
      'getDoors',
      'getMemberbucksDevices',
    ]),
    manageDevice(deviceId, deviceTypeStr) {
      this.$q
        .dialog({
          component: DeviceDialog,
          componentProps: {
            test: 'something',
            deviceType: deviceTypeStr,
            deviceId: String(deviceId),
          },
        })
        .onOk(() => {
          // console.log("OK");
        })
        .onCancel(() => {
          // console.log("Cancel");
        })
        .onDismiss(() => {
          // console.log("Called on OK or Cancel");
        });
    },
  },
};
</script>
