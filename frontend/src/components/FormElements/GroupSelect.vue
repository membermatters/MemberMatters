<template>
  <q-select
    v-model="groupsSelected"
    outlined
    :label="$t('groups')"
    use-input
    use-chips
    multiple
    :options="groups"
    option-value="id"
    option-label="name"
    :rules="[ val => validateNotEmpty(val) || $t('validation.cannotBeEmpty')]"
    @input="$emit('input', groupsSelected)"
  />
</template>

<script>
import { mapGetters } from 'vuex';
import icons from '../../icons';
import formMixin from '../../mixins/formMixin';

export default {
  name: 'GroupSelect',
  mixins: [formMixin],
  props: {
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      groupsSelected: [],
    };
  },
  mounted() {
    this.groupsSelected = this.value;
  },
  computed: {
    ...mapGetters('config', ['groups']),
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass">
  .profile-form
    max-width: $maxWidthMedium
    width: 100%
</style>
