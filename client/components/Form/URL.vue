<template>
  <v-card>
    <v-card-title>
      <h1 class="display-1">
        URL
      </h1>
    </v-card-title>
    <v-card-text>
      <v-text-field
        :value="link"
        readonly
      />
      URL that links to your form.
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="info"
        @click="copyLink"
      >
        Copy
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    link: {
      type: String,
      default: ''
    }
  },
  methods: {
    copyLink () {
      // Copy the current link to the clipboard so that the user can
      // immediately paste it elsewhere.
      navigator.clipboard.writeText(this.link)
    }
  }
}
</script>
