<template>
  <mt-container class="flex justify-center flex-col items-center">
    <div>
      <h1 class="text-black text-xl">Mercan<span class="text-green-400">Tree</span></h1>
    </div>
    <div>
      <p class="text-black">Count: {{count}}</p>
      <mt-button @click="count = count + 1">
        TEST
      </mt-button>
    </div>
  </mt-container>
</template>

<script>
import MtButton from '../MtButton.vue'
import MtContainer from '../MtContainer.vue'

export default {
  name: 'Home',
  components: {
    MtButton,
    MtContainer,
  },
  data: function() {
    return {
      count: 0,
    }
  }
}
</script>

<style>

</style>