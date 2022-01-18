<template>
  <CreateForm
    ref="form"
    :form="form"
    :inputs="inputs"
    @created="onCreated"
  />
</template>

<script>
export default {
  data () {
    return {
      form: {
        name: 'Contact me!',
        description: 'You can use the form below to contact me. Please' +
                     ' include your contact details if you want me to reach' +
                     ' back out to you!',
        email: ''
      },
      inputs: [{
        name: 'email',
        label: 'Email address',
        rules: [
          value => !!value || 'Please supply an email address to which we' +
                              ' can send this form\'s responses.',
          // Use a simple regex to check for the presence of an @-symbol and
          // a dot in the domain name.
          value => /.+@.+\..+/.test(value) || 'Please supply a valid email' +
                                              ' address.'
        ],
        hint: 'Any responses to the form will be sent to this email' +
              ' address.',
        required: true
      }]
    }
  },
  methods: {
    onCreated (key) {
      // Bubble up the created event.
      this.$emit('created', key)
    }
  }
}
</script>
