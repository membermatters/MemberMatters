<template>
  <span>
    <template v-if="!children && !hiddenMenu">
      <q-item
        clickable
        :to="{ name: name }"
      >
        <q-item-section
          v-if="icon"
          avatar
        >
          <q-icon :name="icon" />
        </q-item-section>

        <q-item-section>
          <q-item-label>{{ $t(`menuLink.${name}`) }}</q-item-label>
        </q-item-section>
      </q-item>
    </template>

    <template v-if="children && !hiddenMenu">
      <q-expansion-item
        group="mainMenuGroup"
        expand-separator
        :icon="icon"
        :label="$t(`menuLink.${name}`)"
      >
        <q-item
          v-for="child in children"
          clickable
          :inset-level="1"
          :to="{ name: child.name }"
          :key="child.name"
        >
          <q-item-section
            v-if="child.icon"
            avatar
          >
            <q-icon :name="child.icon" />
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ $t(`menuLink.${child.name}`) }}</q-item-label>
          </q-item-section>
        </q-item>

      </q-expansion-item>
    </template>
  </span>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'EssentialLink',
  props: {
    caption: {
      type: String,
      default: '',
    },

    name: {
      type: [String, Object],
      default: '/',
    },

    icon: {
      type: String,
      default: '',
    },

    children: {
      type: Array,
      default: null,
    },

    hiddenMenu: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters('profile', ['loggedIn']),
  },
};
</script>
