<template>
  <div>
    <the-header />
    <div class="flex overflow-hidden bg-white pt-16">      
      <the-sidebar />
      <router-view />
    </div>
  </div>
</template>

<script>

import TheHeader from '../TheHeader.vue'
import TheSidebar from '../TheSidebar.vue'

export default {
  name: 'Home',
  components: {
    TheHeader,
    TheSidebar,
  },
  data: function() {
    return {
    }
  },
}
</script>

<style>

</style>