<template>
  <div class="column flex items-start justify-start">
    <div>
      <q-form
        ref="formRef"
        @submit="submitProxy"
      >
        <q-input
          outlined
          :label="$t('proxyForm.yourCity')"
          v-model="memberCity"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
          class="q-mb-md"
        />

        <q-select
          outlined
          v-model="proxy.member"
          use-input
          fill-input
          hide-selected
          input-debounce="0"
          :label="$t('proxyForm.proxyName')"
          :options="memberNames"
          @filter="filterNames"
          option-value="id"
          option-label="name"
          style="width: 250px"
        >
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
        </q-select>

        <q-input
          outlined
          :label="$t('proxyForm.proxyCity')"
          v-model="proxy.city"
          :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
          class="q-mb-md"
        />

        <q-select
          outlined
          v-model="meeting"
          :label="$t('proxyForm.meeting')"
          :options="displayUpcomingMeetings"
          option-label="selectName"
          option-value="id"
          style="width: 250px"
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

        <q-btn
          :label="$t('button.submit')"
          :loading="loading"
          :disable="loading"
          color="primary-btn"
          type="submit"
        />
      </q-form>
    </div>

    <proxy-card
      :proxy-card-info="proxyCardInfo"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';
import icons from '../icons';
import ProxyCard from './ProxyCard';
import formMixin from '../mixins/formMixin';

export default {
  name: 'ProxyForm',
  components: { ProxyCard },
  mixins: [formMixin],
  data() {
    return {
      memberNames: [],
      loading: false,
      form: {
        success: false,
        fail: false,
      },
      proxy: {
        member: '',
        city: '',
      },
      meeting: '',
      memberCity: '',
    };
  },
  methods: {
    ...mapActions('tools', ['getMembers', 'getUpcomingMeetings']),
    submitProxy() {
      axios.post('api/proxy/', {
        meeting: this.meeting.id,
        memberCity: this.memberCity,
        proxy: this.proxy.member.id,
        proxyCity: this.proxy.city,
      });
    },
    filterNames(val, update) {
      update(() => {
        const needle = val.toLowerCase();
        this.memberNames = this.members.filter(
          (v) => v.name.toLowerCase().indexOf(needle) > -1 && v.name !== this.profile.fullName,
        );
      });
    },
  },
  mounted() {
    this.getMembers();
    this.getUpcomingMeetings();
  },
  computed: {
    ...mapGetters('config', ['siteOwner']),
    ...mapGetters('profile', ['profile']),
    ...mapGetters('tools', ['members', 'upcomingMeetings']),
    icons() {
      return icons;
    },
    displayUpcomingMeetings() {
      return this.upcomingMeetings.map((meeting) => ({
        selectName: `${meeting.name} (${meeting.date})`,
        name: meeting.name,
        id: meeting.id,
        date: meeting.date,
      }));
    },
    proxyCardInfo() {
      return {
        proxy: {
          name: this.proxy.member ? this.proxy.member.name : '_______',
          city: this.proxy.city ? this.proxy.city : '_______',
        },
        meeting: {
          name: this.meeting.name ? this.meeting.name : '_______',
          date: this.meeting.date ? this.meeting.date : '_______',
        },
        memberCity: this.memberCity ? this.memberCity : '_______',
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
</style>
