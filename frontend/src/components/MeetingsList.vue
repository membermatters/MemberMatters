<template>
  <q-table
    :data="meetings"
    :columns="[{ name: 'type', label: 'Type', field: 'type', sortable: true },
               { name: 'date',
                 label: 'Date',
                 field: 'date',
                 sortable: true,
                 format: (val, row) => this.formatDate(val)
               },
               { name: 'chair', label: 'Chair', field: 'chair', sortable: true },
               { name: 'attendeeCount',
                 label: 'Attendees',
                 field: 'attendeeCount',
                 sortable: true
               },
    ]"
    row-key="id"
    :filter="filter"
    :pagination.sync="pagination"
    :loading="loading"
    :grid="$q.screen.xs"
  >
    <template v-slot:top-left>
      <q-btn
        color="accent"
        :icon="icons.add"
        :label="$t('meetingForm.newMeeting')"
        @click="newMeeting = true"
        class="q-mb-sm"
      />

      <q-dialog
        v-model="newMeeting"
        persistent
      >
        <meeting-form />
      </q-dialog>
    </template>

    <template v-slot:top-right>
      <q-input
        outlined
        dense
        debounce="300"
        v-model="filter"
        placeholder="Search"
      >
        <template v-slot:append>
          <q-icon :name="icons.search" />
        </template>
      </q-input>
    </template>

    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th auto-width />
        <q-th
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.label }}
        </q-th>
        <q-th auto-width>
          Edit
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            @click="props.expand = !props.expand"
            :icon="props.expand ? icons.down : icons.up"
          />
        </q-td>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
        >
          {{ col.value }}
        </q-td>
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            :icon="icons.edit"
          />
        </q-td>
      </q-tr>
      <q-tr
        v-show="props.expand"
        :props="props"
      >
        <q-td colspan="100%">
          <div class="text-left proxy-votes">
            <h5
              class="q-ma-md"
            >
              {{ $t('meetings.proxyVotes') }}
            </h5>
            <template v-if="props.row.proxyList.length">
              <q-markup-table>
                <thead>
                  <tr>
                    <th class="text-left">
                      {{ $t('meetings.memberName') }}
                    </th>
                    <th class="text-right">
                      {{ $t('meetings.proxy') }}
                    </th>
                    <th class="text-right">
                      {{ $t('meetings.dateAssigned') }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="proxy in props.row.proxyList"
                    :key="proxy.name"
                  >
                    <td class="text-left">
                      {{ proxy.name }}
                    </td>
                    <td class="text-right">
                      {{ proxy.proxyName }}
                    </td>
                    <td class="text-right">
                      {{ formatDate(proxy.date) }}
                    </td>
                  </tr>
                </tbody>
              </q-markup-table>
            </template>
            <div
              class="q-pl-md"
              v-else
            >
              {{ $t('meetings.noProxies') }}
            </div>
          </div>

          <div class="text-left attendees">
            <h5
              class="q-pa-md q-ma-none"
            >
              {{ $t('meetings.attendees') }}
            </h5>
            <p class="q-px-md">
              <template v-if="props.row.attendees.length">
                <span
                  v-for="member in props.row.attendees"
                  :key="member"
                >
                  {{ member }},
                </span>
              </template>
              <template v-else>
                {{ $t('meetings.noAttendees') }}
              </template>
            </p>
          </div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';
import MeetingForm from './MeetingForm';

export default {
  name: 'MeetingsList',
  components: { MeetingForm },
  mixins: [formatMixin],
  data() {
    return {
      filter: '',
      loading: false,
      newMeeting: false,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 2 : 12,
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getMeetings']),
  },
  mounted() {
    this.loading = true;
    this.getMeetings()
      .finally(() => {
        this.loading = false;
      });
  },
  computed: {
    ...mapGetters('adminTools', ['meetings']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="stylus" scoped>
  @media (max-width: $breakpoint-xs-max)
    .access-list
      width: 100%;
</style>
