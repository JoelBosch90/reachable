<template>
  <v-text-field
    v-model="input"
    :label="label"
    :required="required"
    :hint="hint"
    @input="onInput"
  />
</template>

<script>
export default {
  props: {
    // This is the label that names the field.
    label: {
      type: String,
      default: ''
    },
    // This is the optional hint that's displayed underneath the field.
    hint: {
      type: String,
      default: ''
    },
    // Should the user be able to submit the form without completing this field?
    required: {
      type: Boolean,
      default: true
    },
    // This is the initial value.
    value: {
      type: String,
      default: ''
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
      // elements can use 'v-model on these input components.
      this.$emit('input', this.input)
    }
  }
}
</script>
