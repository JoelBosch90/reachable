<template>
  <component
    :is="type == 'textarea' ? 'v-textarea' : 'v-text-field'"
    v-model="input"
    :name="name"
    :label="label"
    :type="type"
    :required="required"
    :hint="hint"
    :rules="rules"
    :disabled="disabled"
    @input="onInput"
  />
</template>

<script>
export default {
  props: {
    // This is the field's name and identifier.
    name: {
      type: String,
      default: ''
    },
    // This is the field's visual name.
    label: {
      type: String,
      default: ''
    },
    // This is the optional hint that's displayed underneath the field.
    hint: {
      type: String,
      default: ''
    },
    // Should the user be able to submit the form without completing this
    // field?
    required: {
      type: Boolean,
      default: true
    },
    // Should this input field be disabled?
    disabled: {
      type: Boolean,
      default: false
    },
    // This is the initial value.
    value: {
      type: String,
      default: ''
    },
    // This is the input type.
    type: {
      type: String,
      default: 'text'
    },
    // Set the validation rules.
    rules: {
      type: Array,
      default () {
        return [
          // Check if we have input if that is required.
          value => this.required ? !!value || 'This field is required' : true,
          // Use a simple regex to check for the presence of an @-symbol and
          // a dot in the domain name if we're dealing with an email address.
          value => this.name === 'email'
            ? /.+@.+\..+/.test(value) || 'Please supply a valid email address.'
            : true
        ]
      }
    }
  },
  data () {
    return {
      // This is the actual value.
      input: this.value
    }
  },
  methods: {
    onInput () {
      // We should makes sure that we communicate all changes so that parent
      // elements can use v-model on these input components.
      this.$emit('input', this.input)
    }
  }
}
</script>
