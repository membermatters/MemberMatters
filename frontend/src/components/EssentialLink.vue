<template>
  <span v-if="linkVisible">
    <template v-if="!children && !hiddenMenu">
      <q-item clickable :to="{ name: name, params: defaultParams }">
        <q-item-section v-if="icon" avatar>
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
          v-for="child in visibleLinks.filter(
            (child) => child.hiddenMenu !== true
          )"
          :key="child.name"
          clickable
          :inset-level="1"
          :to="{ name: child.name, params: child.defaultParams }"
        >
          <template>
            <q-item-section v-if="child.icon" avatar>
              <q-icon :name="child.icon" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ $t(`menuLink.${child.name}`) }}</q-item-label>
            </q-item-section>
          </template>
        </q-item>
      </q-expansion-item>
    </template>
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "EssentialLink",
  props: {
    caption: {
      type: String,
      default: "",
    },
    name: {
      type: [String, Object],
      default: "/",
    },
    defaultParams: {
      type: Object,
      default: () => {
        {
        }
      },
    },
    icon: {
      type: String,
      default: "",
    },
    children: {
      type: Array,
      default: null,
    },
    hiddenMenu: {
      type: Boolean,
      default: false,
    },
    featureEnabledFlag: {
      type: String,
      default: "",
    },
  },
  computed: {
    ...mapGetters("profile", ["loggedIn"]),
    ...mapGetters("config", ["features"]),
    linkVisible() {
      return !(
        this.featureEnabledFlag.length &&
        this.features[this.featureEnabledFlag] === false
      );
    },
    visibleLinks() {
      return this.children.filter((link) => {
        // if we require being logged in to display it
        if (link.loggedIn === true) {
          if (!this.loggedIn) return false;
        }

        // if we are not allowed to display it in kiosk mode
        if (this.$q.platform.is.electron && !link.kiosk) {
          return false;
        }

        // all other feature flags
        if (
          link.featureEnabledFlag &&
          this.features[link.featureEnabledFlag] === false
        ) {
          return false;
        }

        return true;
      });
    },
  },
};
</script>
