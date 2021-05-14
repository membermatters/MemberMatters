<template>
  <q-page class="column flex content-center justify-start">
    <q-tabs v-model="tab" align="justify" narrow-indicator class="bg-accent text-white">
      <q-tab name="doors" :label="$t('access.doors')" />
      <q-tab name="interlocks" :label="$t('access.interlocks')" />
    </q-tabs>
    <q-separator />
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="doors">
        <devices-list deviceChoice="doors" :tableData="doors" @openDevice="manageDevice"></devices-list>
      </q-tab-panel>
      <q-tab-panel name="interlocks">
        <devices-list
          deviceChoice="interlocks"
          :tableData="interlocks"
          @openDevice="manageDevice"
        ></devices-list>
      </q-tab-panel>
    </q-tab-panels>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import DevicesList from "components/AdminTools/DevicesList";
import DeviceDialog from "@components/AdminTools/DeviceDialog.vue";

export default {
  name: "ManageDevices",
  components: { DevicesList },
  data() {
    return {
      tab: "doors",
    };
  },
  computed: {
    ...mapGetters("adminTools", ["interlocks", "doors"]),
  },
  beforeMount() {
    this.getDoors();
    this.getInterlocks();
  },
  methods: {
    ...mapActions("adminTools", ["getInterlocks", "getDoors"]),
    manageDevice(deviceId, deviceTypeStr) {
      this.$q
        .dialog({
          component: DeviceDialog,

          // optional if you want to have access to
          // Router, Vuex store, and so on, in your
          // custom component:
          parent: this, // becomes child of this Vue node
          // ("this" points to your Vue component)
          // (prop was called "root" in < 1.1.0 and
          // still works, but recommending to switch
          // to the more appropriate "parent" name)

          // props forwarded to component
          // (everything except "component" and "parent" props above):
          test: "something",
          deviceType: deviceTypeStr,
          deviceId: String(deviceId),
          // ...more.props...
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
