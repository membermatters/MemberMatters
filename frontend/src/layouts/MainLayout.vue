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
          src="https://cdn.quasar.dev/img/material.png"
          style="height: 150px"
        >
          <div class="absolute-bottom bg-transparent">
            <q-avatar
              size="56px"
              class="q-mb-sm"
            >
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
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
          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
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
      <router-view />
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
import MainMenu from '../pages/pageAndRouteConfig';
import mainMixin from '../mixins/mainMixin';

export default {
  name: 'MainLayout',
  mixins: [mainMixin],
  components: {
    EssentialLink,
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
    toolbarTitle() {
      return this.$route.meta.title ? this.$route.meta.title : 'MemberMatters';
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
</style>
