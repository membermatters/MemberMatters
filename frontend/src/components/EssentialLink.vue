<template>
  <span v-if="!children">
    <q-item
      clickable
      tag="a"
      target="_blank"
      :to="to"
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
      expand-separator
      :icon="icon"
      :label="title"
    >
      <q-item
        v-for="child in children"
        clickable
        tag="a"
        target="_blank"
        :inset-level="1"
        :to="child.to"
        :key="child.to"
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

    to: {
      type: Object,
      default: () => ({ name: 'index' }),
    },

    icon: {
      type: String,
      default: '',
    },

    children: {
      type: Object,
      default: null,
    },
  },
};
</script>
