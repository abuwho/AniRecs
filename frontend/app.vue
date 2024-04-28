<script setup lang="ts">

useHead({
  htmlAttrs: {
    class: 'h-full bg-white'
  },
  bodyAttrs: {
    class: 'h-full'
  }
})

</script>

<template>
  <div>

    <NuxtPage :page-key="route => route.fullPath" />

  </div>
</template>
