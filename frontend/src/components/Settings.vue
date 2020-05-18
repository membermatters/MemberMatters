<template>
  <div class="q-pa-md">
    <q-dialog v-model="settingsDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ $t('settings.title') }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          {{ $t('settings.description') }}
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p class="text-h6">
            {{ $t('settings.rfidScanner.title') }}
          </p>

          <p>{{ $t('settings.rfidScanner.connectionStatus') }}: {{ connectionStatusDisplay }}</p>

          <q-input
            outlined
            v-model="readerUrlInput"
            label="Reader URL"
          />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p class="text-h6">
            {{ $t('settings.other.title') }}
          </p>

          <q-btn
            color="primary"
            :label="$t('settings.other.reloadPage')"
            @click="reloadWindow()"
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            :label="$t('button.close')"
            color="primary-btn"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <div
      @click="settingsDialog = true"
      class="settings-button"
    />
  </div>
</template>

<script>
import icons from 'src/icons';
import { mapGetters, mapMutations } from 'vuex';
import Vue from 'vue';
import { Platform } from 'quasar';
import formMixin from '../mixins/formMixin';

let getCurrentWindow;

if (Platform.is.electron) {
  // eslint-disable-next-line global-require
  getCurrentWindow = require('electron').remote.getCurrentWindow;
}

export default {
  name: 'Settings',
  mixins: [formMixin],
  props: {},
  data() {
    return {
      settingsDialog: false,
      readerUrlInput: '',
    };
  },
  mounted() {
    this.readerUrlInput = this.readerUrl;
    this.connectReader();
  },
  methods: {
    ...mapMutations('rfid', ['setConnected', 'setReaderUrl', 'setCardId']),
    connectReader() {
      console.log(`Opening connection to ${this.readerUrl}`);
      const ws = new WebSocket(this.readerUrl, ['arduino']);
      Vue.prototype.$rfid = ws;

      ws.onopen = () => {
        console.log('connected');
        ws.send('something');
        this.setConnected(true);
      };

      ws.onmessage = (message) => {
        if (message.data) {
          if (message.data.startsWith('c:')) {
            const cardId = message.data.replace('c:', '');

            console.log(`Received card: ${cardId}`);
            this.setCardId(cardId);
          } else {
            console.warn(`Received unknown socket message! ${message.data}`);
          }
        } else console.warn('Received corrupt socket message!');
      };

      ws.error = (error) => {
        console.warn(error);
      };

      ws.onclose = () => {
        console.warn('Disconnected from card reader! Trying to reconnect in 5 seconds.');
        setTimeout(() => { this.connectReader(); }, 5000);
      };
    },
    login() {
      this.loginFailed = false;
      this.buttonLoading = true;
      this.$axios.post('/api/login/', {
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
    ...mapGetters('rfid', ['connected', 'readerUrl']),
    icons() {
      return icons;
    },
    connectionStatusDisplay() {
      return this.connected ? this.$t('settings.rfidScanner.connected') : this.$t('settings.rfidScanner.disconnected');
    },
    reloadWindow() {
      return Platform.is.electron ? getCurrentWindow().reload() : window.location.reload();
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
