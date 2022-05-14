<template>
    <div class="navbar bg-base-200 shadow-md fixed w-full z-30">
        <div class="flex-none lg:hidden">
            <button @click="openSidebar()" class="btn btn-square btn-ghost">
                <font-awesome-icon icon='bars' />
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

            const openSidebar = () => {
                document.body.classList.toggle('sidebar--open')
            }

            return {
                store,
                username,
                openSidebar,
            }
        }
    }
</script>

<style>

</style>