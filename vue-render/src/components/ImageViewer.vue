<script setup>
defineProps({
  image: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ image }}</h1>
  </div>
</template>

<style scoped>

</style>
