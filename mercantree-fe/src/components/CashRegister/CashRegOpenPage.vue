<template>
    <div class="max-w-xl mx-auto p-4 shadow-md my-4">
        <div class="flex bg-base-200 px-4 py-2 mb-8 items-center text-base-content">            
            <font-awesome-icon
            class="text-4xl mr-4"
            icon="cash-register" />
            <p class="text-2xl">Abrir o caixa</p>
        </div>
        <div>
            <form @submit.prevent="openCashRegister()" method="POST">
                <div class="flex gap-4 w-full items-center">
                    <label>Valor inicial:</label>
                    <input
                    type="number"
                    min="0"
                    step="any"
                    v-model="state.amount"
                    class="input input-sm input-primary">
                </div>

                <div class="flex gap-4 justify-end mt-8">
                    <button
                    class="btn btn-primary btn-outline"
                    type="submit">
                        Confirmar
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { useStore } from '../../stores/auth'
    import { useRouter } from 'vue-router'
    import CashRegisterService from '../../services/cashRegisterService'
    import { minValue, numeric, required } from '@vuelidate/validators'
    import useVuelidate from '@vuelidate/core'

    const state = ref({
        amount: 0,
    })
    const store = useStore()
    const router = useRouter()

    const rules = {
        amount: { required, minValue: minValue(0), numeric, $autoDirty: true }
    }

    const v$ = useVuelidate(rules, state)

    const openCashRegister = async () => {
        try {
            await v$.value.$validate()
            if (v$.value.$error) return

            await CashRegisterService().create({
                details: '',
                open: true,
                initial_amount: state.value.amount,
                user: store.id,
            })

            router.push('/cashregister')
        }
        catch(e) {
            return
        }
    }
</script>

<style>

</style>