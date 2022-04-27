<template>
  <div class="relative overflow-y-auto lg:ml-64 container mx-auto">
    
    <home-stats class="container__child" />

    <home-products-overview class="container__child" />

    <p class="text-center text-sm text-neutral mt-10 container__child">
      &copy; 2019-2021 <a href="#" class="hover:underline" target="_blank">MultiTech</a>. All rights reserved.
    </p>
  </div>
</template>

<script>

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