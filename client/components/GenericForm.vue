<template>
  <v-form @submit.prevent="onSubmit">
    <v-container>
      <slot />
    </v-container>
    <v-card-actions>
      <v-btn
        type="submit"
        color="success"
      >
        Submit
      </v-btn>
    </v-card-actions>

    <!-- <p v-if="error">
      {{ error }}
    </p> -->
  </v-form>
</template>

<script>
export default {
  props: {
    form: {
      type: Object,
      default: null
    }
  },
  methods: {
    onSubmit () {
      this.$emit('submit', this.form)
    }
  }
}
</script>
