<template>
  <v-text-field
    v-model="input"
    :label="label"
    :required="required"
    @input="onInput"
  />
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: ''
    },
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
