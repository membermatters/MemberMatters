<template>
  <q-layout view="lHh Lpr lFf">
    <q-header
      elevated
      v-if="loggedIn || ($q.platform.is.mobile && loggedIn)"
    >
      <q-toolbar
        class="bg-toolbar"
      >
        <q-btn
          flat
          dense
          round
          icon="fal fa-bars"
          aria-label="Menu"
          @click="mainMenuOpen = !mainMenuOpen"
          v-if="loggedIn && !Platform.is.electron"
        />

        <q-toolbar-title class="row">
          <template
            v-if="loggedIn"
          >
            {{ this.toolbarTitle }}
          </template>
        </q-toolbar-title>

        <q-space />

        <q-icon
          v-if="$q.platform.is.electron"
          class="rotate-90"
          :name="connected ? icons.rfid : icons.rfidSlash"
        />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="mainMenuOpen"
      bordered
      class="column"
      v-if="loggedIn"
    >
      <router-link :to="{ name: 'profile' }">
        <q-img
          spinner-color="white"
          class="absolute-top"
          src="../assets/img/menu-bg/menu-bg.jpg"
          style="height: 150px"
        >
          <div
            class="absolute-bottom bg-transparent"
          >
            <q-avatar
              size="56px"
              class="q-mb-sm"
            >
              <q-icon :name="icons.profile" />
            </q-avatar>
            <div class="text-weight-bold">
              {{ profile.fullName }}
            </div>
            <div v-if="profile.screenName">
              ({{ profile.screenName }})
            </div>
          </div>
        </q-img>
      </router-link>

      <q-scroll-area
        :style="$q.platform.is.capacitor ? 'margin-top: 110px; height: calc(100% - 190px);' :
          'margin-top: 150px; height: calc(100% - 220px);'"
        style="border-right: 1px solid #ddd"
      >
        <q-list>
          <template
            v-for="link in filteredLinks"
          >
            <EssentialLink
              :key="link.title"
              v-bind="link"
            />
          </template>
        </q-list>
      </q-scroll-area>

      <q-space />

      <div class="footer q-pt-md">
        <q-img
          contain
          src="../assets/img/logo/HSBNE_logo.png"
          style="max-height: 40px; cursor: pointer;"
          @click="aboutMemberMatters = true"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <fade-transition>
        <router-view />
      </fade-transition>
    </q-page-container>

    <q-dialog v-model="aboutMemberMatters">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            {{ $t('about.title') }}
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          {{ $t('about.description') }}
          <br><br>
          <a
            :class="$q.dark.isActive ? 'text-white' : 'text-black'"
            href="https://github.com/membermatters/MemberMatters"
            target="_blank"
          >MemberMatters {{ $t('about.linkText') }}</a>
          <br>
          <a
            :class="$q.dark.isActive ? 'text-white' : 'text-black'"
            href="https://github.com/jabelone"
            target="_blank"
          >Jaimyn Mayer {{ $t('about.linkText') }}</a>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            label="OK"
            color="primary-btn"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink';
import { mapActions, mapGetters } from 'vuex';
import Transitions, { FadeTransition } from 'vue2-transitions';
import Vue from 'vue';
import { Platform } from 'quasar';
import icons from '../icons';
import MainMenu from '../pages/pageAndRouteConfig';
import mainMixin from '../mixins/mainMixin';

Vue.use(Transitions);

export default {
  name: 'MainLayout',
  mixins: [mainMixin],
  components: {
    EssentialLink,
    FadeTransition,
  },
  data() {
    return {
      mainMenuOpen: !!Platform.is.electron,
      essentialLinks: MainMenu,
      aboutMemberMatters: false,
    };
  },
  methods: {
    ...mapActions('profile', ['getProfile']),
  },
  computed: {
    Platform() {
      return Platform;
    },
    ...mapGetters('profile', ['loggedIn', 'profile']),
    ...mapGetters('config', ['siteName']),
    ...mapGetters('rfid', ['connected']),
    icons() {
      return icons;
    },
    toolbarTitle() {
      const nameKey = `menuLink.${this.$route.meta.title}`;
      const name = `${this.$t(nameKey)}`;
      return this.$route.meta.title ? name : this.$t('error.pageNotFound');
    },
    filteredLinks() {
      return this.essentialLinks.filter((link) => {
        let displayLink = true;

        if (link.loggedIn) {
          if (!this.loggedIn) displayLink = false;
        }
        if (!link.loggedIn) {
          if (this.loggedIn) displayLink = false;
        }
        if (this.$q.platform.is.electron && !link.kiosk) displayLink = false;
        if (link.admin && this.profile.permissions && !this.profile.permissions.admin) {
          displayLink = false;
        }

        return displayLink;
      });
    },
  },
  mounted() {
    if (this.loggedIn) this.getProfile();
  },
};
</script>

<style lang="sass" scoped>
  .footer
    height: 50px
    text-align: center

  .q-scrollarea
    border-right: none!important

  .fade-enter-active, .fade-leave-active
    transition: opacity .3s

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
    opacity: 0
</style>
