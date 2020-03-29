<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">
        New Meeting
      </div>
    </q-card-section>

    <q-card-section>
      <p>
        {{ $t('meetingForm.pageDescription') }}
      </p>

      <q-form
        ref="formRef"
        @submit="submitMeeting"
      >
        <q-select
          outlined
          :label="$t('form.meetingType')"
          v-model="form.type"
          :options="meetingTypes"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
          class="q-mb-md"
          :disable="form.success"
        />

        <q-select
          v-if="form.type.value === 'group'"
          outlined
          :label="$t('group')"
          v-model="form.group"
          :options="groups"
          option-value="id"
          option-label="name"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
          class="q-mb-md"
          :disable="form.success"
        />

        <q-input
          outlined
          v-model="form.date"
          :label="$t('form.dateTime')"
          mask="####-##-## ##:##"
          :rules="[
            val => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            val => validateFutureDateTime(val) || $t('validation.futureDate'),
          ]"
          class="q-mb-sm"
          :disable="form.success"
        >
          <template v-slot:append>
            <q-icon
              :name="icons.calendar"
              class="cursor-pointer"
            >
              <q-popup-proxy
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="form.date"
                  mask="YYYY-MM-DD HH:mm"
                  :options="validateFutureDate"
                  :disable="form.success"
                >
                  <div class="row items-center justify-end q-gutter-sm">
                    <q-btn
                      label="Cancel"
                      color="primary"
                      flat
                      v-close-popup
                    />
                    <q-btn
                      label="OK"
                      color="primary"
                      flat
                      v-close-popup
                    />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-icon>
            <q-icon
              :name="icons.clock"
              class="cursor-pointer"
            >
              <q-popup-proxy
                transition-show="scale"
                transition-hide="scale"
              >
                <q-time
                  v-model="form.date"
                  mask="YYYY-MM-DD HH:mm"
                  :disable="form.success"
                >
                  <div class="row items-center justify-end q-gutter-sm">
                    <q-btn
                      label="Cancel"
                      color="primary"
                      flat
                      v-close-popup
                    />
                    <q-btn
                      label="OK"
                      color="primary"
                      flat
                      v-close-popup
                    />
                  </div>
                </q-time>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-input
          outlined
          :debounce="debounceLength"
          v-model="form.chair"
          :label="$t('form.chair')"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
          :disable="form.success"
        />

        <q-banner
          v-if="form.success"
          class="bg-positive text-white q-my-md"
        >
          {{ $t('meetingForm.success') }}
        </q-banner>

        <q-banner
          v-if="form.error"
          class="bg-negative text-white q-my-md"
        >
          {{ $t('meetingForm.fail') }}
        </q-banner>

        <q-card-actions
          align="right"
          class="text-primary"
          v-if="!form.success"
        >
          <q-btn
            flat
            :label="$t('button.cancel')"
            :disable="loading"
            v-close-popup
          />
          <q-btn
            flat
            :label="$t('button.submit')"
            :loading="loading"
            :disable="loading"
            type="submit"
          />
        </q-card-actions>

        <q-card-actions
          align="right"
          class="text-primary"
          v-else
        >
          <q-btn
            flat
            :label="$t('button.close')"
            v-close-popup
          />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';
import Moment from 'moment';
import icons from '../icons';
import formMixin from '../mixins/formMixin';

const m = Moment();

export default {
  name: 'MeetingForm',
  mixins: [formMixin],
  props: {
    meetingId: {
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

        type: '',
        group: '',
        date: m.minute() || m.second() || m.millisecond() ? m.add(1, 'hour').startOf('hour').format('YYYY-MM-DD HH:mm') : m.startOf('hour').format('YYYY-MM-DD HH:mm'),
        chair: '',
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getMeetings', 'getMeetingTypes']),
    submitMeeting() {
      this.loading = true;

      axios.post('/api/meetings/', this.form)
        .then(() => {
          this.form.error = false;
          this.form.success = true;
          this.getMeetings();
        })
        .catch(() => {
          this.form.error = true;
        })
        .finally(() => { this.loading = false; });
    },
  },
  beforeMount() {
    this.getMeetingTypes();
  },
  computed: {
    ...mapGetters('adminTools', ['meetings', 'meetingTypes']),
    ...mapGetters('config', ['groups']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass">
  .meeting-form
    max-width: $maxWidthMedium
    width: 100%
</style>
