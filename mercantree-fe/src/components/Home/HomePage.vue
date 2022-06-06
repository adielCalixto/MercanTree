<template>
  <div class="relative overflow-y-auto md:ml-48 container max-w-full mx-auto">
    
    <home-stats class="p-2 bg-base-200" />

    <home-products-overview class="p-2 bg-base-200" />

    <p class="text-center text-sm text-neutral-content mt-10 container__child">
      &copy; 2019-2021 <a href="#" class="hover:underline" target="_blank">MultiTech</a>. All rights reserved.
    </p>
  </div>
</template>

<script lang="ts">

import HomeStats from './HomeStats.vue'
import HomeProductsOverview from './HomeProductsOverview.vue'

export default {
  name: 'HomePage',
  components: {
    HomeStats,
    HomeProductsOverview,
  },
  data: function() {
    return {
    }
  },
}
</script>

<style>
</style>