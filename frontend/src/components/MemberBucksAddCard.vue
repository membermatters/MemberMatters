<template>
  <div>
    <q-card-section>
      <div class="text-h6">
        {{ $t("memberbucks.addCard") }}
      </div>

      {{ $t("memberbucks.addCardDescription") }}
    </q-card-section>

    <q-card-section>
      <div id="stripe-card-element" class="q-pa-sm" />

      <div class="row q-pa-sm">
        <q-space />
        <q-btn
          id="card-button"
          :disable="disableStripeForm"
          :loading="disableStripeForm"
          color="primary"
        >
          {{ $t("memberbucks.saveCard") }}
        </q-btn>
        <q-space />
      </div>

      <q-banner v-if="error" class="text-white bg-red">
        {{ error }}
      </q-banner>
    </q-card-section>
  </div>
</template>

<script>
import icons from "@icons";
import { mapGetters, mapActions } from "vuex";

export default {
  name: "MemberBucksAddCard",
  data() {
    return {
      stripe: null,
      disableStripeForm: false,
      error: null,
    };
  },
  watch: {
    async keys(value) {
      if (!this.stripe) await this.setupStripe(value.stripePublishableKey);
    },
  },
  async mounted() {
    if (!this.stripe && this.keys.stripePublishableKey) {
      await this.setupStripe(this.keys.stripePublishableKey);
    }
  },
  methods: {
    ...mapActions("profile", ["getProfile"]),
    async setupStripe(stripePublishableKey) {
      this.stripe = await window.Stripe(stripePublishableKey);

      const elements = this.stripe.elements();
      const cardElement = elements.create("card", this.$stripeElementsStyle());
      cardElement.mount("#stripe-card-element");

      const cardButton = document.getElementById("card-button");

      this.$axios
        .get("/api/billing/card/")
        .then((response) => {
          cardButton.addEventListener("click", async () => {
            this.disableStripeForm = true;
            this.error = null;
            const { setupIntent, error } = await this.stripe.confirmCardSetup(
              response.data.clientSecret,
              {
                payment_method: {
                  card: cardElement,
                  billing_details: {
                    name: this.profile.fullName,
                  },
                },
              }
            );
            this.disableStripeForm = false;

            if (error) {
              this.error = error.message;
            } else if (setupIntent.status === "succeeded") {
              this.$axios
                .post("/api/billing/card/", {
                  paymentMethodId: setupIntent.payment_method,
                })
                .then(() => {
                  this.getProfile();
                  this.hide();
                })
                .catch(() => {
                  this.error = this.$t("memberbucks.addCardError");
                });
            }
          });
        })
        .catch(() => {
          this.error = this.$t("memberbucks.addCardError");
        });
    },
    hide() {
      this.$emit("hide");
    },
  },
  computed: {
    ...mapGetters("profile", ["profile"]),
    ...mapGetters("config", ["keys"]),
    icons() {
      return icons;
    },
  },
};
</script>

<style scoped>
#stripe-card-element {
  border: solid gray 1px;
}
</style>
