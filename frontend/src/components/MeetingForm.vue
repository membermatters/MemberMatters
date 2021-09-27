<template>
  <q-card :flat="!!meetingId">
    <q-card-section>
      <div class="text-h6">
        {{
          meetingId
            ? $t("meetingForm.editMeeting")
            : $t("meetingForm.newMeeting")
        }}
      </div>
    </q-card-section>

    <q-card-section>
      <p>
        {{
          meetingId
            ? $t("meetingForm.editDescription")
            : $t("meetingForm.pageDescription")
        }}
      </p>

      <q-form
        ref="formRef"
        @submit="!!meetingId ? updateMeeting() : submitMeeting()"
      >
        <div>
          <q-select
            v-model="form.type"
            outlined
            :label="$t('form.meetingType')"
            :options="meetingTypes"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
            ]"
            class="q-mb-md"
            :disable="form.success || !!meetingId"
          />
          <q-tooltip v-if="!!meetingId" :offset="[0, -10]">
            {{ $t("meetingForm.noUpdateMeetingType") }}
          </q-tooltip>
        </div>

        <q-select
          v-if="form.type.value === 'group'"
          v-model="form.group"
          outlined
          :label="$t('group')"
          :options="groups"
          option-value="id"
          option-label="name"
          :rules="[
            (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
          ]"
          class="q-mb-md"
          :disable="form.success || !!meetingId"
        />

        <div>
          <q-tooltip v-if="pastMeeting" :offset="[0, -10]">
            {{ $t("meetingForm.updatePastMeeting") }}
          </q-tooltip>
          <q-input
            v-model="form.date"
            outlined
            :label="$t('form.dateTime')"
            mask="####-##-## ##:##"
            :rules="[
              (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
              (val) =>
                validateFutureDateTime(val, pastMeeting) ||
                $t('validation.futureDate'),
            ]"
            class="q-mb-sm"
            :disable="form.success || pastMeeting"
          >
            <template v-slot:append>
              <q-icon :name="icons.calendar" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                  <q-date
                    v-model="form.date"
                    mask="YYYY-MM-DD HH:mm"
                    :options="validateFutureDate"
                    :disable="form.success || pastMeeting"
                  >
                    <div class="row items-center justify-end q-gutter-sm">
                      <q-btn
                        v-close-popup
                        label="Cancel"
                        color="primary"
                        flat
                      />
                      <q-btn v-close-popup label="OK" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
              <q-icon :name="icons.clock" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                  <q-time
                    v-model="form.date"
                    mask="YYYY-MM-DD HH:mm"
                    :disable="form.success || pastMeeting"
                  >
                    <div class="row items-center justify-end q-gutter-sm">
                      <q-btn
                        v-close-popup
                        label="Cancel"
                        color="primary"
                        flat
                      />
                      <q-btn v-close-popup label="OK" color="primary" flat />
                    </div>
                  </q-time>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>

        <q-input
          v-model="form.chair"
          outlined
          :debounce="debounceLength"
          :label="$t('form.chair')"
          :rules="[
            (val) => validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
          ]"
          :disable="form.success"
        />

        <q-banner v-if="form.success" class="bg-positive text-white q-my-md">
          {{
            !!meetingId
              ? $t("meetingForm.editSuccess")
              : $t("meetingForm.success")
          }}
        </q-banner>

        <q-banner v-if="form.error" class="bg-negative text-white q-my-md">
          {{ $t("meetingForm.fail") }}
        </q-banner>

        <q-card-actions v-if="!form.success" align="right" class="text-primary">
          <q-btn
            v-close-popup
            flat
            :label="$t('button.cancel')"
            :disable="loading"
          />
          <q-btn
            color="primary"
            :label="$t('button.submit')"
            :loading="loading"
            :disable="loading"
            type="submit"
          />
        </q-card-actions>

        <q-card-actions v-else align="right" class="text-primary">
          <q-btn v-close-popup flat :label="$t('button.close')" />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import * as dayjs from "dayjs";
import icons from "../icons";
import formMixin from "../mixins/formMixin";

let d;

export default {
  name: "MeetingForm",
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

        type: "",
        group: "",
        date:
          dayjs().minute() || dayjs().second() || dayjs().millisecond()
            ? dayjs().add(1, "hour").startOf("hour").format("YYYY-MM-DD HH:mm")
            : dayjs().startOf("hour").format("YYYY-MM-DD HH:mm"),
        chair: "",
      },
    };
  },
  methods: {
    ...mapActions("adminTools", ["getMeetings", "getMeetingTypes"]),
    updateMeeting() {
      this.loading = true;

      this.$axios
        .put(`/api/meetings/${this.meetingId}/`, this.form)
        .then(() => {
          this.form.error = false;
          this.form.success = true;
          this.getMeetings();
        })
        .catch(() => {
          this.form.error = true;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    submitMeeting() {
      this.loading = true;

      this.$axios
        .post("/api/meetings/", this.form)
        .then(() => {
          this.form.error = false;
          this.form.success = true;
          this.getMeetings();
        })
        .catch(() => {
          this.form.error = true;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  beforeMount() {
    this.getMeetingTypes();
  },
  mounted() {
    // If true this means we're editing an existing meeting
    if (this.meetingId) {
      const meetingInfo = this.meetings[
        this.meetings.findIndex((p) => p.id === this.meetingId)
      ];

      this.form.type = meetingInfo.type;
      this.form.date = meetingInfo.date;
      this.form.chair = meetingInfo.chair;
    }
  },
  computed: {
    ...mapGetters("adminTools", ["meetings", "meetingTypes"]),
    ...mapGetters("config", ["groups"]),
    pastMeeting() {
      return dayjs(this.form.date) < dayjs();
    },
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
