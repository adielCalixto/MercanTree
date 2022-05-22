<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useStore as useConfigStore } from './stores/config'

const configStore = useConfigStore()
onMounted(() => {
  configStore.getConfig()
  configStore.setTheme()
})

</script>

<template>
  <router-view />
</template>

<style>
</style>
