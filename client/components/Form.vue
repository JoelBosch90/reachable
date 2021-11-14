<template>
  <section>
    <p v-if="sent">
      Thank you for your response! The owner of this form has been notified.
    </p>
    <form v-else @submit.prevent="respond">
      <input
        v-for="field in fields"
        :key="field.name"
        v-model="inputs[field.name]"
        :name="field.name"
        :title="field.title"
      >
      <button>Submit</button>
      <p v-if="error">
        {{ error }}
      </p>
    </form>
  </section>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: 0
    },
    fields: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      inputs: {},
      sent: false,
      error: false
    }
  },
  methods: {
    // Method to send a response with the current form submission.
    async respond () {
      // Send the response.
      const response = await this.$axios.post('forms/response/', {
        form: this.id,
        inputs: this.inputs
      })

      // Check the response to see if any errors occurred.
      if (response.data === true) {
        // If not, confirm this to the user.
        this.sent = true
      } else {
        // Otherwise, show an error message.
        this.error = 'An error has occurred: your response has not been sent.'
      }
    }
  }
}
</script>
