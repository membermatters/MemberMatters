<template>
  <q-page class="column flex justify-start items-center">
    <profile-form class="q-mb-lg" />

    <q-btn-group push>
      <q-btn
        push
        color="toolbar"
        label="Digital ID"
        @click="digitalId = true"
      />
      <q-btn
        push
        color="primary"
        label="Change Password"
        @click="changePassword = true"
      />
    </q-btn-group>

    <q-dialog v-model="digitalId">
      <digital-id-card />
    </q-dialog>

    <q-dialog v-model="changePassword">
      <change-password-card />
    </q-dialog>
  </q-page>
</template>

<script>
import ProfileForm from "../components/ProfileForm";
import icons from "../icons";
import DigitalIdCard from "../components/DigitalIdCard";
import ChangePasswordCard from "../components/ChangePasswordCard";

export default {
  name: "ProfilePage",
  components: { ChangePasswordCard, DigitalIdCard, ProfileForm },
  data() {
    return {
      text: "",
      digitalId: false,
      changePassword: false,
    };
  },
  computed: {
    icons() {
      return icons;
    },
  },
};
</script>
