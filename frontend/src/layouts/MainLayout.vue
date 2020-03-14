<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="fal fa-bars"
          aria-label="Menu"
          @click="mainMenuOpen = !mainMenuOpen"
        />

        <q-toolbar-title>
          {{ this.toolbarTitle }}
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="mainMenuOpen"
      bordered
      class="column"
    >
      <router-link :to="{ name: 'profile' }">
        <q-img
          spinner-color="white"
          class="absolute-top"
          src="../assets/img/menu-bg/menu-bg.jpg"
          style="height: 150px"
        >
          <div class="absolute-bottom bg-transparent">
            <q-avatar
              size="56px"
              class="q-mb-sm"
            >
              <q-icon :name="icons.profile" />
            </q-avatar>
            <div class="text-weight-bold">
              Jaimyn Mayer
            </div>
            <div>@jabelone</div>
          </div>
        </q-img>
      </router-link>

      <q-scroll-area
        style="height: calc(100% - 250px); margin-top: 150px; border-right: 1px solid #ddd"
      >
        <q-list>
          <template
            v-for="link in essentialLinks"
          >
            <template v-if="link.loggedIn === loggedIn">
              <EssentialLink
                :key="link.title"
                v-bind="link"
              />
            </template>
          </template>
        </q-list>
      </q-scroll-area>

      <q-space />

      <div class="footer">
        <q-toggle
          label="Dark Mode"
          v-model="darkMode"
        />
        <p
          class="content-end q-mb-none q-pa-md"
          style="text-decoration: underline; cursor: pointer;"
          @click="aboutMemberMatters = true"
        >
          {{ $t('about.title') }}
        </p>
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
            href="https://github.com/membermatters/MemberMatters"
            target="_blank"
          >MemberMatters {{ $t('about.linkText') }}</a>
          <br>
          <a
            href="https://github.com/jabelone"
            target="_blank"
          >Jaimyn Mayer {{ $t('about.linkText') }}</a>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            label="OK"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink';
import { mapGetters } from 'vuex';
import Transitions, { FadeTransition } from 'vue2-transitions';
import Vue from 'vue';
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
      darkMode: this.$q.dark.isActive,
      mainMenuOpen: true,
      essentialLinks: MainMenu,
      aboutMemberMatters: false,
    };
  },
  methods: {
    getMenuState() {
      return localStorage.getItem('menuState');
    },
    setMenuState() {
      localStorage.setItem('menuState', this.mainMenuOpen);
    },
    getDarkState() {
      return localStorage.getItem('darkMode');
    },
    setDarkState() {
      localStorage.setItem('darkMode', this.darkMode);
    },
  },
  watch: {
    mainMenuOpen() {
      this.setMenuState();
    },
    darkMode(value) {
      this.$q.dark.set(value);
      this.setDarkState();
    },
  },
  computed: {
    ...mapGetters('profile', ['loggedIn']),
    icons() {
      return icons;
    },
    toolbarTitle() {
      const nameKey = `menuLink.${this.$route.meta.title}`;
      const name = `${this.$t(nameKey)}`;
      return this.$route.meta.title ? name : this.$t('error.pageNotFound');
    },
  },
  mounted() {
    this.mainMenuOpen = this.getMenuState() === 'true';
    this.darkMode = this.getDarkState() === 'true';
  },
};
</script>

<style scoped>
  .footer {
    height: 100px;
    text-align: center;
  }

  p {
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .3s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
  {
    opacity: 0;
  }
</style>
