<template>
  <div>
    <div class="text-left">
      <p>{{ $t('form.name') }}: {{ kiosk.name }}</p>
      <p>{{ $t('form.lastSeen') }}: {{ kiosk.lastSeen }}</p>
      <p>{{ $t('kiosk.authorised') }}: {{ kiosk.authorised }}</p>
      <p>{{ $t('form.playTheme') }}: {{ kiosk.playTheme }}</p>
      <p>{{ $t('kiosk.kioskId') }}: {{ kiosk.kioskId }}</p>
      <p>{{ $t('form.ipAddress') }}: {{ kiosk.kioskIp }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KioskDetails',
  props: {
    kiosk: {
      type: Object,
      default: () => {
        {
        }
      },
    },
  },
};
</script>
