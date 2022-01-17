<template>
  <v-img content-class="r-center">
    <client-only>
      <vue-qrious
        ref="qr"
        v-model="value"
        :size="size"
        :padding="padding"
        :level="level"
        :mime="mime"
      />
    </client-only>
  </v-img>
</template>

<script>
import VueQrious from 'vue-qrious'
export default {
  components: {
    VueQrious
  },
  props: {
    link: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      // Sizing the QR code with the VueQrious library is a little tricky as you
      // can end up with some odd extra padding. These settings were carefully
      // chosen to avoid that.
      size: 420,
      level: 'H',
      padding: 30,
      mime: 'image/png',
      value: ''
    }
  },
  watch: {
    link: {
      immediate: true,
      // Make sure we update the link for the QR code image.
      handler () {
        this.value = this.link
      }
    }
  }
}
</script>

<style>
.r-center {
  display: flex;
  justify-content: center;
}
</style>
