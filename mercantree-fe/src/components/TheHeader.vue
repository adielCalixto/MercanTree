<template>
    <div class="navbar bg-base-200 shadow-md fixed w-full z-30">
        <div class="flex-none lg:hidden">
            <button class="btn btn-square btn-ghost">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-5 h-5 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </div>
        <div class="flex-1">
            <a class="btn btn-ghost normal-case text-2xl">Mercan<span class="text-green-500">Tree</span></a>
        </div>
        <div class="flex-none">
            <a class="btn normal-case btn-sm">Bem vindo {{ username }}</a>
        </div>
    </div>
</template>

<script lang="ts">
    import { useStore } from '../stores/auth'
    import { computed } from 'vue'

    export default {
        name: 'TheHeader',
        setup() {
            const store = useStore()
            const username = computed(() => store.username)

            return {
                store,
                username,
            }
        }
    }
</script>

<style>

</style>