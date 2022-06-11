<template>
    <div class="max-w-md mx-auto py-16 p-4">
        <div class="shadow-lg">
            <h1 class="text-center text-xl font-semibold">Mercan<span class="text-green-400">Tree</span> | Login</h1>
        </div>
        <form @submit.prevent="login" class="p-4 bg-base-100 shadow-lg">
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">Email</span>
                </label>

                <input
                type="email"
                v-model="state.email"
                placeholder="email"
                class="input input-bordered w-full">

                <div class="badge badge-ghost rounded-none mt-1 ml-auto gap-2" v-if="v$.email.$error">
                    {{ v$.email.$errors[0].$message }}
                </div>
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Senha</span>
                </label>

                <input
                type="password"
                v-model="state.password"
                placeholder="senha"
                class="input input-bordered w-full">

                <div class="badge badge-ghost rounded-none mt-1 ml-auto gap-2" v-if="v$.password.$error">
                    {{ v$.password.$errors[0].$message }}
                </div>
            </div>
            <div class="form-control">
                <button type="submit" class="btn btn-success btn-sm btn-block btn-outline">Entrar</button>
            </div>
        </form>
    </div>
</template>

<script lang='ts'>

import { useStore } from '../../stores/auth'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import { required, email } from '@vuelidate/validators'

export default {
    name: 'Login',
    setup() {
        const store = useStore()
        const router = useRouter()

        const state = reactive({
            email: '',
            password: '',
        })

        const rules = {
            email: { required, email, $autoDirty: true },
            password: { required, $autoDirty: true },
        }

        const v$ = useVuelidate(rules, state)

        const login = async () => {
            await v$.value.$validate()
            if(v$.value.$error) return

            store.loginUser({username: state.email, password: state.password})
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
            state,
            v$,
        }
    },
}
</script>

<style>

</style>