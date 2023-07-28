<template>
  <transition
    appear
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <div v-show="success" class="text-body1 text-center saved-message">
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
    success: {
      type: Boolean,
      default: false,
    },
    error: {
      type: Boolean,
      default: false,
    },
    showText: {
      type: Boolean,
      default: false,
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
