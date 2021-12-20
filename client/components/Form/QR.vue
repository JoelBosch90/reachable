<template>
  <v-card>
    <v-card-title>
      <h1 class="display-1">
        QR code
      </h1>
    </v-card-title>
    <v-img
      content-class="r-center"
    >
      <client-only>
        <vue-qrious
          ref="qr"
          :size="size"
          :value="link"
          :padding="padding"
          :level="level"
          :mime="mime"
        />
      </client-only>
    </v-img>
    <v-card-text>
      QR code that links to your form.
    </v-card-text>
  </v-card>
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
      size: 215,
      level: 'H',
      padding: 30,
      mime: 'image/png'
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
