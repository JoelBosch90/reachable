<template>
  <v-container
    class="my-8"
  >
    <v-row>
      <v-col>
        <FormURL :link="link" />
      </v-col>
      <v-col>
        <FormQR :link="link" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      link: ''
    }
  },
  mounted () {
    this.link = this.createLink()
  },
  methods: {
    createLink () {
      // Get the origin of the current page.
      const domain = location.origin

      // Get the relative URL to the form page with the key in the current URL.
      const href = this.$router.resolve({
        name: 'form-key',
        params: {
          key: this.$route.params.key
        }
      }).href

      // Combine both for the complete URL to the form.
      return domain + href
    }
  }
}
</script>
