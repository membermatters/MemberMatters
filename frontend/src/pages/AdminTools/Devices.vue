<template>
  <q-page class="column flex content-center justify-start">
    <q-tabs v-model="tab" align="justify" narrow-indicator>
      <q-tab name="doors" :label="$t('access.doors')" />
      <q-tab name="interlocks" :label="$t('access.interlocks')" />
    </q-tabs>
    <q-separator />
    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="doors">
        <devices-list deviceChoice='doors' :tableData='doors'/>
      </q-tab-panel>
      <q-tab-panel name="interlocks">
        <devices-list deviceChoice='interlocks' :tableData='interlocks'></devices-list>
      </q-tab-panel>
    </q-tab-panels>
  </q-page>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import DevicesList from "components/AdminTools/DevicesList";

export default {
  name: "ManageDevices",
  components: { DevicesList },
  data() {
    return {
      tab: "doors",
    }
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
  },
};
</script>
