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
        name: '',
        description: '',
        email: '',
        disabled: false
      },
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
                ' this to explain the form\'s purpose or ask questions to' +
                ' your respondents.',
          required: false
        },
        {
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
          hint: 'Any responses to this form will be sent to this email' +
                ' address.',
          required: true
        }
      ]
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
