<template>
  <transition name="fade">
    <div
      v-show="value"
      class="text-body1 text-center saved-message"
    >
      <template v-if="showText">
        {{ error ? $t('form.error') : $t('form.saved') }}
      </template>
      <q-icon
        :color="error ? 'fail' : 'success'"
        :name="error ? icons.fail : icons.success"
      />
    </div>
  </transition>
</template>

<script>
import icons from '../icons';

export default {
  name: 'SavedNotification',
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    error: {
      type: Boolean,
      default: false,
    },
    timeout: {
      type: Number,
      default: 1500,
    },
    showText: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    showNotification() {
      setTimeout(() => {
        this.$emit('input', false);
      }, this.timeout);
    },
  },
  watch: {
    value(value) {
      if (value) this.showNotification();
    },
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
  .fade-leave-active
    transition: opacity 0.5s ease-out

  .fade-enter-active
    transition: opacity 0.1s ease-in

  .fade-enter, .fade-leave-to
    opacity: 0
</style>
