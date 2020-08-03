<template>
  <div class="column">
    <div class="row justify-start q-pb-sm">
      <q-btn
        v-if="selectedMember.state==='Inactive'"
        class="q-mr-sm"
        color="positive"
        :label="$t('adminTools.enableAccess')"
        @click="setMemberState('active')"
        :loading="stateLoading"
      />
      <q-btn
        v-else-if="selectedMember.state==='New'"
        class="q-mr-sm"
        color="primary"
        :label="$t('adminTools.makeMember')"
        @click="activateMember()"
        :loading="stateLoading"
      />
      <q-btn
        v-else
        class="q-mr-sm"
        color="negative"
        :label="$t('adminTools.disableAccess')"
        @click="setMemberState('inactive')"
        :loading="stateLoading"
      />
    </div>

    <q-card>
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
        <q-tab-panel name="profile">
          <div class="text-h6">
            {{ $t('menuLink.profile') }}
          </div>
          These pages are read only for now.


          <div class="q-pa-md">
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
          <div class="text-h6">
            {{ $t('adminTools.access') }}
          </div>
          <access-list :prop-data="selectedMember" />
        </q-tab-panel>

        <q-tab-panel name="log">
          <div class="text-h6">
            {{ $t('adminTools.log') }}
          </div>
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
      tab: 'profile',
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
  methods: {
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
