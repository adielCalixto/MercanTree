<template>
    <div class="max-w-md mx-auto py-16 p-4">
        <div class="text-center py-2 bg-primary text-gray-100">
            <h1 class="text-xl">Faça login no sistema</h1>
        </div>

        <form @submit.prevent="login" class="p-4 bg-base-100 shadow-lg">
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">Email</span>
                </label>
                <input type="email" v-model="data.email" placeholder="email" class="input input-bordered w-full">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Senha</span>
                </label>
                <input type="password" v-model="data.password" placeholder="senha" class="input input-bordered w-full">
            </div>
            <div class="form-control items-end">
                <button type="submit" class="btn btn-secondary btn-sm w-1/3 btn-outline">Entrar</button>
            </div>
        </form>
    </div>
</template>

<script lang='ts'>

import { useStore } from '../../stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
    name: 'Login',
    setup() {
        const store = useStore()
        const router = useRouter()

        const data = ref({
            email: '',
            password: '',
        })

        const login = () => {
            store.loginUser({username: data.value.email, password: data.value.password})
            .then(() => {
                router.push('/') 
            })
            .catch(error => {
                console.log(error)
            })
        }

        return {
            store,
            login,
            data,
        }
    },
}
</script>

<style>

</style>