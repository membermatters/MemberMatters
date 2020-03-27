<template>
  <q-page class="column flex content-center justify-start items-center">
    <profile-form />

    <q-btn-group push>
      <q-btn
        push
        color="toolbar"
        label="Digital ID"
      />
      <q-btn
        push
        color="primary"
        label="Change Password"
      />
      <q-btn
        push
        color="accent"
        label="Memberbucks"
      />
    </q-btn-group>
  </q-page>
</template>

<script>
import ProfileForm from '../components/ProfileForm';
import icons from '../icons';

export default {
  name: 'ProfilePage',
  components: { ProfileForm },
  data() {
    return {
      text: '',
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
