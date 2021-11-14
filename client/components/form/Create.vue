<template>
  <form @submit.prevent="createLink">
    <input v-model="form.name" type="text" placeholder="Name">
    <input v-model="form.description" type="text" placeholder="Description">
    <input v-model="form.email" type="email" placeholder="Email">
    <button>Submit</button>
  </form>
</template>

<script>
export default {
  data () {
    return {
      form: {
        name: '',
        description: '',
        email: ''
      }
    }
  },
  methods: {
    // On submit, we want to attempt to create a new link with the information
    // submitted in the form.
    async createLink () {
      // Create the form, and get the key.
      const response = await this.$axios.post('forms/', this.form)

      // Redirect the user to the new form.
      this.$router.push({
        name: 'form-key',
        params: {
          key: response.data
        }
      })
    }
  }
}
</script>
