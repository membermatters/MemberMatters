<template>
  <span v-if="!children">
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
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption>
          {{ caption }}
        </q-item-label>
      </q-item-section>
    </q-item>
  </span>

  <span v-else>
    <q-expansion-item
      group="mainMenuGroup"
      expand-separator
      :icon="icon"
      :label="title"
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
          <q-item-label>{{ child.title }}</q-item-label>
          <q-item-label caption>
            {{ child.caption }}
          </q-item-label>
        </q-item-section>
      </q-item>

    </q-expansion-item>
  </span>
</template>

<script>
export default {
  name: 'EssentialLink',
  props: {
    title: {
      type: String,
      required: true,
    },

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
  },
};
</script>
