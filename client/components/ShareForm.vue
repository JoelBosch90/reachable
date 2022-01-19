<template>
  <v-container
    class="my-8"
  >
    <v-card
      width="640"
      class="mx-auto"
    >
      <v-toolbar dense dark>
        <v-toolbar-title>
          Share this form
        </v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="selectForm">
          <v-icon>
            mdi-form-select
          </v-icon>
        </v-btn>
        <v-btn icon @click="selectQR">
          <v-icon>
            mdi-qrcode
          </v-icon>
        </v-btn>
        <v-btn icon @click="copyLink">
          <v-icon>
            mdi-content-copy
          </v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text v-if="selected == 'form'">
        <ResponseForm :form-key="formKey" />
      </v-card-text>
      <v-card-text v-if="selected == 'qr'">
        <FormQR :link="link" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  props: {
    linkKey: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      formKey: '',
      link: '',
      selected: 'form'
    }
  },
  watch: {
    // Load this component whenever we get a link key.
    linkKey: {
      handler: 'load'
    }
  },
  mounted () {
    // Load this component immediately if we already have a link key.
    if (this.linkKey) {
      this.load()
    }
  },
  methods: {
    // Load this component by setting the key for the response form and the link
    // for the qr code.
    load () {
      this.formKey = this.linkKey
      this.link = this.createLink()
    },
    selectForm () {
      this.selected = 'form'
    },
    selectQR () {
      this.selected = 'qr'
    },
    copyLink () {
      // Copy the current link to the clipboard so that the user can
      // immediately paste it elsewhere.
      navigator.clipboard.writeText(this.link)
    },
    createLink () {
      // Get the origin of the current page.
      const domain = location.origin

      // Get the relative URL to the form page with the key in the current URL.
      const href = this.$router.resolve({
        name: 'form-key',
        params: { key: this.formKey }
      }).href

      // Combine both for the complete URL to the form.
      return domain + href
    }
  }
}
</script>
