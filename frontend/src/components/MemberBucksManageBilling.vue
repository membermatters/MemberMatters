<template>
  <q-card :flat="flat">
    <template v-if="this.features.stripe.enabled">
      <template v-if="cardExists">
        <q-card-section>
          <div class="text-h6">
            {{ $t("memberbucks.savedCardTitle") }}
          </div>
          <div class="text-subtitle2">
            {{ $t("memberbucks.savedCardDescription") }}
          </div>
        </q-card-section>

        <q-card-section>
          <credit-card
            :name="profile.fullName"
            :expiry="profile.financial.memberBucks.savedCard.expiry"
            :last4="profile.financial.memberBucks.savedCard.last4"
            :brand="profile.financial.memberBucks.savedCard.brand"
            class="shadow-7"
          />

          <div class="row q-pt-md">
            <q-space />
            <q-btn
              id="card-button"
              :loading="removeLoading"
              :disable="removeLoading"
              color="primary"
              @click="removeCard"
            >
              {{ $t("memberbucks.removeCard") }}
            </q-btn>
            <q-space />
          </div>
        </q-card-section>
      </template>

      <template v-else>
        <member-bucks-add-card />
      </template>
    </template>
    <template v-else>
      <q-card-section>
        <div class="text-h6">
          {{ $t("menuLink.billing") }}
        </div>
        <div class="text-subtitle2">
          {{ $t("error.stripeNotConfiguredFeature") }}
        </div>
      </q-card-section>
    </template>
  </q-card>
</template>

<script>
import CreditCard from "components/CreditCard";
import { mapGetters, mapActions } from "vuex";
import MemberBucksAddCard from "components/MemberBucksAddCard";

export default {
  name: "MemberBucksManageBilling",
  components: { MemberBucksAddCard, CreditCard },
  props: {
    flat: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      removeLoading: false,
    };
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    removeCard() {
      this.removeLoading = true;
      this.$axios
        .delete("/api/billing/card/")
        .then(() => {
          this.getProfile();
        })
        .catch(() => {
          this.error = this.$t("memberbucks.removeCardError");
        })
        .finally(() => {
          this.removeLoading = false;
        });
    },
    onOKClick() {
      this.$emit("ok");
    },
  },
  mounted() {
    // by default set the saved card exists to false (v-model)
    this.$emit("card-exists", this.cardExists);
  },
  watch: {
    cardExists() {
      this.$emit("card-exists", this.cardExists);
    },
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
    ...mapGetters("config", ["features"]),
    cardExists() {
      return this.profile.financial.memberBucks.savedCard.last4;
    },
  },
};
</script>
