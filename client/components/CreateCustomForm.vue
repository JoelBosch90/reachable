<template>
  <CreateForm
    ref="form"
    :form="form"
    @created="onCreated"
  />
</template>

<script>
export default {
  data () {
    return {
      form: {
        inputs: [
          {
            name: 'name',
            label: 'Name',
            rules: [
              value => !!value || 'Please name your form.'
            ],
            hint: 'This name is used in the form and in your UI.',
            required: true
          },
          {
            name: 'description',
            label: 'Description',
            rules: [],
            hint: 'This description will be shown near your form. You can use' +
                  ' this to explain the purpose of this form or to ask' +
                  ' questions to your respondents.',
            required: false
          },
          {
            name: 'email',
            label: 'Email address',
            rules: [
              value => !!value || 'Please supply an email address to which we' +
                                  ' can send the responses.',
              // Use a simple regex to check for the presence of an @-symbol and
              // a dot in the domain name.
              value => /.+@.+\..+/.test(value) || 'Please supply a valid email' +
                                                  ' address.'
            ],
            hint: 'Any responses to this form will be sent to this email' +
                  ' address.',
            required: true
          }
        ],
        disabled: false
      }
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
