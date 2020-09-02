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
          class="q-px-lg q-py-lg"
        >
          <div
            class="row justify-start q-pt-sm"
            :class="{'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs}"
          >
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


          <div class="row q-pt-md">
            <div
              class="col-12 col-md-6"
              :class="{'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs}"
            >
              <q-form
                ref="formRef"
              >
                <q-input
                  outlined
                  @input="saveChange('email')"
                  :debounce="debounceLength"
                  v-model="profileForm.email"
                  :label="$t('form.email')"
                  :rules="[ val => validateEmail(val) || $t('validation.invalidEmail')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.email"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  outlined
                  @input="saveChange('rfidCard')"
                  :debounce="debounceLength"
                  v-model="profileForm.rfidCard"
                  :label="$t('form.rfidCard')"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.rfidCard"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  outlined
                  @input="saveChange('firstName')"
                  :debounce="debounceLength"
                  v-model="profileForm.firstName"
                  :label="$t('form.firstName')"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.firstName"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  outlined
                  @input="saveChange('lastName')"
                  :debounce="debounceLength"
                  v-model="profileForm.lastName"
                  :label="$t('form.lastName')"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.lastName"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  outlined
                  @input="saveChange('phone')"
                  :debounce="debounceLength"
                  v-model="profileForm.phone"
                  :label="$t('form.phone')"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.invalidPhone')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.phone"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-input
                  outlined
                  @input="saveChange('screenName')"
                  :debounce="debounceLength"
                  v-model="profileForm.screenName"
                  :label="$t('form.screenName')"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.screenName"
                      :error="saved.error"
                    />
                  </template>
                </q-input>

                <q-select
                  @input="saveChange('groups')"
                  outlined
                  :label="$t('groups')"
                  v-model="profileForm.groups"
                  use-chips
                  multiple
                  :options="groups"
                  option-value="id"
                  option-label="name"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.groups"
                      :error="saved.error"
                    />
                  </template>
                </q-select>

                <q-select
                  @input="saveChange('memberType')"
                  outlined
                  :label="$t('form.memberType')"
                  v-model="profileForm.memberType"
                  :options="memberTypes"
                  option-value="id"
                  option-label="name"
                  :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
                >
                  <template v-slot:append>
                    <saved-notification
                      show-text
                      v-model="saved.memberType"
                      :error="saved.error"
                    />
                  </template>
                </q-select>
              </q-form>
            </div>

            <div
              class="col-12 col-md-6"
              :class="{'q-px-sm': $q.screen.xs, 'q-px-lg': !$q.screen.xs}"
            >
              <q-list
                bordered
                padding
                class="rounded-borders"
                style="max-width: 350px"
              >
                <q-item-label header>
                  Other Attributes
                </q-item-label>

                <q-item
                  clickable
                  v-ripple
                  v-for="item in ['registrationDate', 'state', 'last_induction']"
                  :key="item"
                >
                  <q-item-section>
                    <q-item-label lines="1">
                      {{ selectedMember[item] ? selectedMember[item] : $t('error.noValue') }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ $t(`form.${item}`) }}
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel name="access">
          {{ $t('adminTools.accessDescription') }}
          <access-list
            :member-id="selectedMemberFiltered.id"
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
import formMixin from 'src/mixins/formMixin';
import SavedNotification from 'components/SavedNotification';
import { mapGetters } from 'vuex';

export default {
  name: 'ManageMember',
  components: { AccessList, SavedNotification },
  mixins: [formMixin],
  data() {
    return {
      stateLoading: false,
      welcomeLoading: false,
      tab: 'profile',
      access: {},
      profileForm: {
        email: '',
        rfidCard: '',
        firstName: '',
        lastName: '',
        phone: '',
        screenName: '',
        groups: [],
        memberType: '',
      },
      saved: {
        // if there was an error saving the form
        error: false,

        email: false,
        rfidCard: false,
        firstName: false,
        lastName: false,
        phone: false,
        screenName: false,
        groups: false,
        memberType: false,
      },
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
  beforeMount() {
    this.loadInitialForm();
  },
  methods: {
    loadInitialForm() {
      this.profileForm.email = this.selectedMember.email;
      this.profileForm.rfidCard = this.selectedMember.rfid;
      this.profileForm.firstName = this.selectedMember.name.first;
      this.profileForm.lastName = this.selectedMember.name.last;
      this.profileForm.phone = this.selectedMember.phone;
      this.profileForm.screenName = this.selectedMember.screenName;
      this.profileForm.groups = this.selectedMember.groups;
      this.profileForm.memberType = this.selectedMember.memberType;
    },
    saveChange(field) {
      this.$refs.formRef.validate(false).then(() => {
        this.$refs.formRef.validate(false)
          .then((result) => {
            if (result) {
              this.$axios.put(`/api/admin/members/${this.member.id}/profile/`, this.profileForm)
                .then(() => {
                  this.saved.error = false;
                  this.saved[field] = true;
                  // TODO: get list of updated profiles
                })
                .catch(() => {
                  this.saved.error = true;
                  this.saved[field] = true;
                });
            }
          });
      });
    },
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
        .then((response) => {
          if (response.data.success) {
            this.$q.dialog({
              title: this.$t('adminTools.makeMemberSuccess'),
              message: this.$t('adminTools.makeMemberSuccessDescription'),
            });
          } else {
            this.$q.dialog({
              title: this.$t('error.error'),
              message: this.$t(response.data.message),
            });
          }
        })
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
    ...mapGetters('config', ['groups', 'memberTypes']),
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

<style lang="scss" scoped>
.q-card {
  max-width: 100%;
}
</style>
