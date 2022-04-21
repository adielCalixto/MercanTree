<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
import TheSidebar from './components/TheSidebar.vue'
</script>

<template>
  <div>
    <the-header />
    <div class="flex overflow-hidden bg-white pt-16">      
      <the-sidebar />
      <router-view />
    </div>
  </div>
</template>

<style>
</style>
