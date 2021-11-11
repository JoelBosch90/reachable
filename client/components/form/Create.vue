<template>
  <form @submit.prevent="createLink">
    <input name="" placeholder="Message">
    <input name="user" placeholder="Email">
    <button>Submit</button>
  </form>
</template>

<script>
export default {
  methods: {
    // On submit, we want to attempt to create a new link with the information
    // submitted in the form.
    createLink () {
      this.$axios.post('forms/', this.form)
    }
  }
}
</script>
