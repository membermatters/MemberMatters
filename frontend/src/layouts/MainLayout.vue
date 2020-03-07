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
          MemberMatters
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="mainMenuOpen"
      bordered
      content-class="bg-grey-1"
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
        style="height: calc(100% - 200px); margin-top: 150px; border-right: 1px solid #ddd"
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

      <p
        class="content-end q-mb-none q-pa-md"
        style="height: 50px; text-align: center;"
      >
        About MemberMatters
      </p>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from 'components/EssentialLink';
import MainMenu from './MainMenu.conf';
import mainMixin from '../mixins/mainMixin';

export default {
  name: 'MainLayout',
  mixins: [mainMixin],
  components: {
    EssentialLink,
  },
  data() {
    return {
      mainMenuOpen: true,
      essentialLinks: MainMenu,
    };
  },
  methods: {
    getMenuState() {
      return localStorage.getItem('menuState');
    },
    setMenuState() {
      localStorage.setItem('menuState', this.mainMenuOpen);
    },
  },
  watch: {
    mainMenuOpen() {
      this.setMenuState();
    },
  },
  mounted() {
    this.mainMenuOpen = this.getMenuState() === 'true';
  },
};
</script>
