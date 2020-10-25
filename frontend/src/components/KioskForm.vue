<template>
  <q-card flat>
    <q-card-section>
      <div class="text-h6">
        {{ $t('kiosk.editForm') }}
      </div>
    </q-card-section>

    <q-card-section>
      <q-form
        @submit="updateKiosk()"
      >
        <q-input
          v-model="form.name"
          outlined
          :debounce="debounceLength"
          :label="$t('form.name')"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
        />

        <q-checkbox
          v-model="form.authorised"
          :label="$t('kiosk.authorised')"
        />

        <q-checkbox
          v-model="form.playTheme"
          :label="$t('form.playTheme')"
        />

        <q-banner
          v-if="form.success"
          class="bg-positive text-white q-my-md"
        >
          {{ $t('kiosk.updated') }}
        </q-banner>

        <q-banner
          v-if="form.error"
          class="bg-negative text-white q-my-md"
        >
          {{ $t('kiosk.fail') }}
        </q-banner>

        <q-card-actions
          align="right"
          class="text-primary"
        >
          <q-btn
            v-if="!form.success"
            v-close-popup
            flat
            :label="$t('button.cancel')"
            :disable="loading"
          />
          <q-btn
            v-if="form.success"
            v-close-popup
            flat
            :label="$t('button.close')"
          />
          <q-btn
            color="primary"
            :label="$t('button.submit')"
            :loading="loading"
            :disable="loading"
            type="submit"
          />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import icons from '../icons';
import formMixin from '../mixins/formMixin';

export default {
  name: 'KioskForm',
  mixins: [formMixin],
  props: {
    kioskId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      form: {
        error: false,
        success: false,

        name: '',
        authorised: false,
        playTheme: false,
        kioskId: null,
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getKiosks']),
    updateKiosk() {
      this.loading = true;

      this.$axios.put(`/api/kiosks/${this.kioskId}/`, this.form)
        .then(() => {
          this.form.error = false;
          this.form.success = true;
          this.getKiosks();
        })
        .catch(() => {
          this.form.error = true;
        })
        .finally(() => { this.loading = false; });
    },
  },
  mounted() {
    const kioskInfo = this.kiosks[this.kiosks.findIndex((p) => p.id === this.kioskId)];
    this.form.name = kioskInfo.name;
    this.form.authorised = kioskInfo.authorised;
    this.form.playTheme = kioskInfo.playTheme;
    this.form.kioskId = kioskInfo.kioskId;
  },
  computed: {
    ...mapGetters('adminTools', ['kiosks']),
    icons() {
      return icons;
    },
  },
};
</script>
