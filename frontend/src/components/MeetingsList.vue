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
          {{ $t('edit') }}
        </q-th>
        <q-th auto-width>
          {{ $t('delete') }}
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
            @click="editMeeting(props.row.id)"
            :icon="icons.edit"
          />

          <q-dialog v-model="editMeetingDialog">
            <q-card>
              <q-card-section class="row items-center q-pb-none dialog-close-button">
                <q-space />
                <q-btn
                  :icon="icons.close"
                  flat
                  round
                  dense
                  v-close-popup
                />
              </q-card-section>

              <q-card-section>
                <meeting-form :meeting-id="editMeetingId" />
              </q-card-section>
            </q-card>
          </q-dialog>
        </q-td>
        <q-td auto-width>
          <q-btn
            size="sm"
            color="accent"
            round
            @click="deleteMeeting(props.row.id)"
            :icon="icons.delete"
          />
        </q-td>
      </q-tr>
      <q-tr
        v-show="props.expand"
        :props="props"
      >
        <q-td colspan="100%">
          <meetings-details
            :proxies="props.row.proxyList"
            :attendees="props.row.attednees"
          />
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import MeetingsDetails from 'components/MeetingDetails';
import icons from '../icons';
import formatMixin from '../mixins/formatMixin';
import MeetingForm from './MeetingForm';

export default {
  name: 'MeetingsList',
  components: { MeetingsDetails, MeetingForm },
  mixins: [formatMixin],
  data() {
    return {
      filter: '',
      loading: false,
      newMeeting: false,
      editMeetingDialog: false,
      editMeetingId: 0,
      pagination: {
        sortBy: 'date',
        descending: true,
        rowsPerPage: this.$q.screen.xs ? 2 : 12,
      },
    };
  },
  methods: {
    ...mapActions('adminTools', ['getMeetings']),
    deleteMeeting(id) {
      this.$q.dialog({
        title: 'Confirm',
        message: this.$t('meetingForm.deleteMeeting'),
        cancel: {
          color: 'primary',
          flat: true,
          label: this.$t('button.cancel'),
        },
        ok: {
          color: 'primary',
          label: this.$t('button.ok'),
        },
        persistent: true,
      }).onOk(() => {
        this.$axios.delete(`/api/meetings/${id}/`, this.form)
          .then(() => {
            this.getMeetings();
          })
          .catch(() => {
            this.$q.dialog({
              title: this.$t('error.error'),
              message: this.$t('error.requestFailed'),
            });
          });
      });
    },
    editMeeting(id) {
      this.editMeetingId = id;
      this.editMeetingDialog = true;
    },
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