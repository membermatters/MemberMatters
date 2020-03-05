<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="fas fa-bars"
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
    >
      <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
          <div class="text-weight-bold">Jaimyn Mayer</div>
          <div>@jabelone</div>
        </div>
      </q-img>

      <q-scroll-area
        style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd"
      >
        <q-list>
          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </q-scroll-area>
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
      mainMenuOpen: false,
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
