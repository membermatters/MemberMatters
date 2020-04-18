<template>
  <div style="min-width: 300px">
    <q-card class="my-card">
      <div class="my-card-inner">
        <q-card-section class="full-height column items-start">
          <div class="credit-card-title q-ma-sm">
            Credit Card
          </div>

          <q-space />

          <div class="credit-card-number q-pa-sm">
            **** **** **** {{ last4 }}
          </div>

          <div class="credit-card-expiry q-pa-sm full-width row justify-center">
            Expiry: {{ expiry }}
          </div>

          <div class="credit-card-name q-pa-sm">
            {{ name }}
          </div>

          <div class="credit-card-logo">
            <q-img
              width="100%"
              :src="ccLogo"
            />
          </div>
        </q-card-section>
      </div>
    </q-card>
  </div>
</template>

<script>
import VisaLogo from 'src/statics/visa-logo.jpg';
import MastercardLogo from 'src/statics/mastercard-logo.png';
import AmexLogo from 'src/statics/amex-logo.png';
import icons from '../icons';

export default {
  name: 'CreditCard',
  props: {
    last4: {
      type: String,
      default: '_ _ _ _',
    },
    expiry: {
      type: String,
      default: '_ _/_ _',
    },
    name: {
      type: String,
      default: '_ _ _ _ _    _ _ _ _ _',
    },
    logo: {
      type: String,
      default: '',
    },
  },
  computed: {
    ccLogo() {
      if (this.logo === 'Visa') return VisaLogo;
      if (this.logo === 'MasterCard') return MastercardLogo;
      if (this.logo === 'American Express') return AmexLogo;

      return '';
    },
    icons() {
      return icons;
    },
  },
};
</script>

<style lang="sass" scoped>
  .my-card
    width: 100%
    padding-bottom: 63%
    border-radius: 10px

  .my-card-inner
    position: absolute
    width: 100%
    height: 100%

  .credit-card-title
    font-size: 140%

  .credit-card-logo
    position: absolute
    width: 15%
    right: 5%
    top: 10%
</style>
