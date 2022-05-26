<template>
    <div class="navbar bg-base-200 shadow-md px-4 fixed w-full z-30">
        <div class="flex-none print:hidden lg:hidden">
            <button @click="openSidebar()" class="btn btn-square btn-ghost">
                <font-awesome-icon icon='bars' />
            </button>
        </div>
        <div class="flex-1">
            <a class="text-2xl font-bold">Mercan<span class="text-green-500">Tree</span></a>
        </div>
        <div class="flex-none relative print:hidden">
            <a @click="showUserInfo = !showUserInfo" class="btn btn-neutral btn-square btn-sm"><font-awesome-icon icon="user-check" /></a>

            <div v-if="showUserInfo" class="bg-neutral rounded text-center text-neutral-content p-2 absolute mt-1 right-0 top-full w-40">
                <p class="text-lf font-bold">{{ username }}</p>
                <router-link to="/account" class="link text-sm mt-4">
                    Detalhes 
                    <font-awesome-icon class="ml-1" icon="external-link" />
                </router-link>

                <div class="divider divider-horizontal my-4"></div>

                <button @click="logOut()" class="btn btn-sm btn-ghost btn-block">Sair</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { useStore } from '../stores/auth'
    import { computed, ref } from 'vue'
    import { useRouter } from 'vue-router'

    export default {
        name: 'TheHeader',
        setup() {
            const store = useStore()
            const username = computed(() => store.username)
            const showUserInfo = ref(false)
            const router = useRouter()

            const openSidebar = () => {
                document.body.classList.toggle('sidebar--open')
            }

            const logOut = async () => {
                store.logoutUser()
                router.push('/login')
            }

            return {
                store,
                username,
                openSidebar,
                showUserInfo,
                logOut,
            }
        }
    }
</script>

<style>

</style>