<template>
  <q-card style="max-width: 400px">
    <q-card-section class="row">
      <div class="text-h6">
        {{ $t("proxyForm.newProxy") }}
      </div>
    </q-card-section>
    <q-card-section class="row items-center">
      <q-form ref="formRef" @submit="submitProxy">
        <div class="column flex items-center justify-center">
          <p class="page-description">
            {{ $t("proxyForm.pageDescription") }}
          </p>
          <div class="row flex items-start justify-center">
            <proxy-card class="q-ma-md" :proxy-card-info="proxyCardInfo" />

            <div class="q-ma-md">
              <q-input
                v-model="memberCity"
                outlined
                :label="$t('proxyForm.yourCity')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                class="q-mb-sm"
              />

              <q-select
                v-model="proxy.member"
                outlined
                use-input
                fill-input
                hide-selected
                input-debounce="0"
                :label="$t('proxyForm.proxyName')"
                :options="memberNames"
                option-value="id"
                option-label="name"
                class="q-mb-lg"
                @filter="filterNames"
              >
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      {{ $t("form.noResults") }}
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>

              <q-input
                v-model="proxy.city"
                outlined
                :label="$t('proxyForm.proxyCity')"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                class="q-mb-sm"
              />

              <q-select
                v-model="meeting"
                outlined
                :label="$t('proxyForm.meeting')"
                :options="displayUpcomingMeetings"
                :rules="[
                  (val) =>
                    validateNotEmpty(val) || $t('validation.cannotBeEmpty'),
                ]"
                option-label="selectName"
                option-value="id"
                style="width: 250px"
                class="q-mb-md"
              >
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey">
                      {{ $t("proxyForm.noMeetings") }}
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>

              <q-banner
                v-if="form.success"
                class="bg-positive text-white q-my-md"
              >
                {{ $t("meetingForm.success") }}
              </q-banner>

              <q-banner
                v-if="form.error"
                class="bg-negative text-white q-my-md"
              >
                {{ $t("meetingForm.fail") }}
              </q-banner>

              <q-card-actions
                v-if="!form.success"
                align="right"
                class="text-primary"
              >
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
            </div>
          </div>
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import icons from "../icons";
import ProxyCard from "./ProxyCard";
import formMixin from "src/mixins/formMixin";
import formatMixin from "src/mixins/formatMixin";

export default {
  name: "ProxyForm",
  components: { ProxyCard },
  mixins: [formMixin, formatMixin],
  data() {
    return {
      memberNames: [],
      loading: false,
      form: {
        success: false,
        fail: false,
      },
      proxy: {
        member: "",
        city: "",
      },
      meeting: "",
      memberCity: "",
    };
  },
  methods: {
    ...mapActions("tools", ["getMembers", "getUpcomingMeetings"]),
    submitProxy() {
      this.loading = true;
      this.$axios
        .post("api/proxies/", {
          meeting: this.meeting.id,
          memberCity: this.memberCity,
          proxy: this.proxy.member.id,
          proxyCity: this.proxy.city,
        })
        .then(() => {
          this.$emit("close-form");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    filterNames(val, update) {
      update(() => {
        const needle = val.toLowerCase();
        this.memberNames = this.members.filter(
          (v) =>
            v.name.toLowerCase().indexOf(needle) > -1 &&
            v.name !== this.profile.fullName
        );
      });
    },
  },
  mounted() {
    this.getMembers();
    this.getUpcomingMeetings();
  },
  computed: {
    ...mapGetters("config", ["siteOwner"]),
    ...mapGetters("profile", ["profile"]),
    ...mapGetters("tools", ["members", "upcomingMeetings"]),
    icons() {
      return icons;
    },
    displayUpcomingMeetings() {
      return this.upcomingMeetings.map((meeting) => ({
        selectName: `${meeting.name} (${this.formatDate(meeting.date)})`,
        name: meeting.name,
        id: meeting.id,
        date: meeting.date,
      }));
    },
    proxyCardInfo() {
      return {
        proxy: {
          name: this.proxy.member ? this.proxy.member.name : "_______",
          city: this.proxy.city ? this.proxy.city : "_______",
        },
        meeting: {
          name: this.meeting.name ? this.meeting.name : "_______",
          date: this.meeting.date ? this.meeting.date : "_______",
        },
        memberCity: this.memberCity ? this.memberCity : "_______",
      };
    },
  },
};
</script>

<style lang="sass" scoped>
.proxy-field
  font-style: italic
  font-weight: bold
  text-decoration: underline

  .page-description
    max-width: 700px
</style>
