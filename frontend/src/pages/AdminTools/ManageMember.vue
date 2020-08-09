<template>
  <div class="column">
    <q-card flat>
      <q-tabs
        v-model="tab"
        dense
        align="justify"
        narrow-indicator
      >
        <q-tab
          name="profile"
          :label="$t('menuLink.profile')"
        />
        <q-tab
          name="access"
          :label="$t('adminTools.access')"
        />
        <q-tab
          name="log"
          disable
          :label="$t('adminTools.log')"
        />
        <!--        <q-tab-->
        <!--          name="memberbucks"-->
        <!--          disable-->
        <!--          :label="$t('menuLink.memberbucks')"-->
        <!--        />-->
      </q-tabs>

      <q-separator />

      <q-tab-panels
        v-model="tab"
        animated
      >
        <q-tab-panel
          name="profile"
          class="q-px-xl q-py-lg"
        >
          <p>These pages are read only for now (apart from the buttons just below).</p>

          <div class="row justify-start q-pt-sm">
            <q-btn
              v-if="selectedMember.state==='Inactive'"
              class="q-mr-sm q-mb-sm"
              color="positive"
              :label="$t('adminTools.enableAccess')"
              @click="setMemberState('active')"
              :loading="stateLoading"
            />
            <q-btn
              v-else-if="selectedMember.state==='New'"
              class="q-mr-sm q-mb-sm"
              color="primary"
              :label="$t('adminTools.makeMember')"
              @click="activateMember()"
              :loading="stateLoading"
            />
            <q-btn
              v-else
              class="q-mr-sm q-mb-sm"
              color="negative"
              :label="$t('adminTools.disableAccess')"
              @click="setMemberState('inactive')"
              :loading="stateLoading"
            />
            <q-btn
              v-if="selectedMember.state!=='New'"
              class="q-mr-sm q-mb-sm"
              color="primary"
              :label="$t('adminTools.sendWelcomeEmail')"
              @click="sendWelcomeEmail()"
              :loading="welcomeLoading"
            />
          </div>

          <div class="q-pt-lg">
            <q-list
              bordered
              separator
            >
              <q-item
                clickable
                v-ripple
                v-for="(value, propertyName) in selectedMemberFiltered"
                :key="propertyName"
              >
                <q-item-section>
                  <q-item-label>{{ value }}</q-item-label>
                  <q-item-label caption>
                    {{ propertyName }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-tab-panel>

        <q-tab-panel name="access">
          <access-list
            :access="{doors: access.doors, interlocks: access.interlocks}"
          />
        </q-tab-panel>

        <q-tab-panel name="log">
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>

        <q-tab-panel name="memberbucks">
          <div class="text-h6">
            {{ $t('menuLink.memberbucks') }}
          </div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </q-tab-panel>
      </q-tab-panels>
    </q-card>
  </div>
</template>

<script>
import AccessList from 'components/AccessList';

export default {
  name: 'ManageMember',
  components: { AccessList },
  data() {
    return {
      stateLoading: false,
      welcomeLoading: false,
      tab: 'profile',
      access: {},
    };
  },
  props: {
    member: {
      type: Object,
      default: () => {},
    },
    members: {
      type: Array,
      default: () => {},
    },
  },
  mounted() {
    this.getMemberAccess();
  },
  watch: {
    member() {
      this.getMemberAccess();
    },
  },
  methods: {
    sendWelcomeEmail() {
      this.welcomeLoading = true;
      this.$axios.post(`/api/admin/members/${this.member.id}/sendwelcome/`)
        .then(() => {
          this.$q.dialog({
            title: this.$t('success'),
            message: this.$t('adminTools.sendWelcomeEmailSuccess'),
          });
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.welcomeLoading = false;
        });
    },
    getMemberAccess() {
      this.stateLoading = true;
      this.$axios.get(`/api/admin/members/${this.member.id}/access/`)
        .then((response) => {
          this.access = response.data;
        })
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.stateLoading = false;
        });
    },
    setMemberState(state) {
      this.stateLoading = true;
      this.$axios.post(`/api/admin/members/${this.member.id}/state/${state}/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('updateMembers');
          setTimeout(() => { this.stateLoading = false; }, 1200);
        });
    },
    activateMember() {
      this.stateLoading = true;
      this.$axios.post(`/api/admin/members/${this.member.id}/makemember/`)
        .catch(() => {
          this.$q.dialog({
            title: this.$t('error.error'),
            message: this.$t('error.requestFailed'),
          });
        })
        .finally(() => {
          this.$emit('updateMembers');
          setTimeout(() => { this.stateLoading = false; }, 1200);
        });
    },
  },
  computed: {
    selectedMember() {
      if (this.members) {
        return this.members.find((e) => e.id === this.member.id);
      }
      return this.member;
    },
    selectedMemberFiltered() {
      const newMember = { ...this.selectedMember };
      delete newMember.access;
      delete newMember.groups;
      return newMember;
    },
  },
};
</script>
