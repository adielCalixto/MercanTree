<template>
    <div class="max-w-md mx-auto my-16 p-4">
        <div class="text-center mb-8">
            <h1 class="text-xl">Faça login no sistema</h1>
        </div>

        <div class="p-4 bg-white shadow-lg">
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
            <div class="form-control w-full">
                <button @click="login" class="btn btn-success btn-outline btn-block">Entrar</button>
            </div>
        </div>
    </div>
</template>

<script lang='ts'>

import { useStore } from '../../stores/auth'
import { ref } from 'vue'

export default {
    name: 'Login',
    setup() {
        const store = useStore()

        const data = ref({
            email: '',
            password: '',
        })

        return {
            store,
            data,
        }
    },
    methods: {
        login: function() {
            this.store.loginUser({username: this.data.email, password: this.data.password})
            .then(response => {
                this.$router.push('/') 
            })
            .catch(error => {
                
            })
        }
    }
}
</script>

<style>

</style>