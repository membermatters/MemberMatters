<template>
  <div>
    <q-dialog v-model="settingsDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ $t("settings.title") }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          {{ $t("settings.description") }}
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p class="text-h6">
            {{ $t("settings.rfidScanner.title") }}
          </p>

          <p>
            {{ $t("settings.rfidScanner.connectionStatus") }}:
            {{ connectionStatusDisplay }}
          </p>

          <q-input v-model="readerUrlInput" outlined label="Reader URL" />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p class="text-h6">
            {{ $t("settings.other.title") }}
          </p>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            v-close-popup
            flat
            :label="$t('button.close')"
            color="primary-btn"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <div class="settings-button" @click="settingsDialog = true" />
  </div>
</template>

<script>
/* eslint-disable no-console */
import icons from "@icons";
import { mapGetters, mapMutations } from "vuex";
import Vue from "vue";
import formMixin from "../mixins/formMixin";

export default {
  name: "Settings",
  mixins: [formMixin],
  props: {},
  data() {
    return {
      settingsDialog: false,
      readerUrlInput: "",
    };
  },
  mounted() {
    this.readerUrlInput = this.readerUrl;
    this.connectReader();
  },
  methods: {
    ...mapMutations("rfid", ["setConnected", "setReaderUrl", "setCardId"]),
    connectReader() {
      const ws = new WebSocket(this.readerUrl, ["arduino"]);
      Vue.prototype.$rfid = ws;

      ws.onopen = () => {
        ws.send("something");
        this.setConnected(true);
      };

      ws.onmessage = (message) => {
        if (message.data) {
          if (message.data.startsWith("c:")) {
            const cardId = message.data.replace("c:", "");

            this.setCardId(cardId);
          }
        } else console.warn("Received corrupt socket message!");
      };

      ws.error = (error) => {
        console.warn(error);
      };

      ws.onclose = () => {
        console.warn(
          "Disconnected from card reader! Trying to reconnect in 5 seconds."
        );
        setTimeout(() => {
          this.connectReader();
        }, 5000);
      };
    },
    login() {
      this.loginFailed = false;
      this.buttonLoading = true;
      this.$axios
        .post("/api/login/", {
          email: this.email,
          password: this.password,
        })
        .then(() => {
          this.redirectLoggedIn();
        })
        .catch((error) => {
          this.loginError = true;
          throw error;
        })
        .finally(() => {
          this.buttonLoading = false;
        });
    },
  },
  watch: {
    readerUrlInput(value) {
      this.setReaderUrl(value);
    },
  },
  computed: {
    ...mapGetters("rfid", ["connected", "readerUrl"]),
    icons() {
      return icons;
    },
    connectionStatusDisplay() {
      return this.connected
        ? this.$t("settings.rfidScanner.connected")
        : this.$t("settings.rfidScanner.disconnected");
    },
  },
};
</script>

<style lang="sass" scoped>
.settings-button
  width: 50px
  height: 50px
  position: fixed
  bottom: 0
  right: 0
</style>
