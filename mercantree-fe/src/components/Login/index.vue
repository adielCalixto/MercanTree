<template>
    <div class="bg-base-200 h-screen py-16">
        <div class="max-w-md mx-auto p-4 bg-primary rounded-box">
            <div class="text-center py-2 text-neutral">
                <h1 class="text-xl font-bold">Mercan<span class="text-green-500 font-bold">Tree</span> | Login</h1>
            </div>

            <form @submit.prevent="login" class="p-4">
                <div class="form-control w-full">
                    <label class="label">
                        <span class="label-text font-semibold">Email</span>
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
                        <span class="label-text font-semibold">Senha</span>
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
                <div class="form-control items-end">
                    <button type="submit" class="btn btn-success text-primary btn-sm w-1/3 ">Entrar</button>
                </div>
            </form>
        </div>
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