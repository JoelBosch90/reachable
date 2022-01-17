<template>
  <v-sheet>
    <v-container
      class="fill-height title"
    >
      <v-row>
        <h1
          class="text-center display-4 hidden-xs-only"
        >
          Create a new form in seconds!
        </h1>
        <h1
          class="text-center display-2 hidden-sm-and-up"
        >
          Create a new form in seconds!
        </h1>
      </v-row>
    </v-container>
    <v-container
      class="form"
    >
      <h1
        class="display-1"
      >
        Quick contact form
      </h1>
      <p
        class="body-1"
      >
        Let people contact you without revealing your contact details.
        Created in a single click!
      </p>
      <ContactForm />
    </v-container>
  </v-sheet>
</template>

<script>
export default { layout: 'default' }
</script>

<style scoped>
.title
{
  padding: 3.5em;
}
.form
{
  max-width: 30em;
}
</style>
