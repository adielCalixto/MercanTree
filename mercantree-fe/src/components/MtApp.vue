<template>
  <div>
    <the-header />
    <div class="flex overflow-hidden bg-base-100 pt-16">      
      <the-sidebar />
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">

import TheHeader from './TheHeader.vue'
import TheSidebar from './TheSidebar.vue'

export default {
  name: 'MtApp',
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