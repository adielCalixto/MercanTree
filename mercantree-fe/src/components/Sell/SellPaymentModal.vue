<template>
    <div>
        <h1 class="text-xl text-base-content mb-8">Tipo de pagamento</h1>
        <div class="collapse collapse-open">
            <div class="collapse-title bg-primary text-primary-content">
                Dinheiro
            </div>
            <div class="collapse-content bg-base-200 text-nase-content"> 
                <form @submit.prevent="payOrder()">
                    <div class="flex items-center my-6">
                        <span class="text-xl mr-auto">Valor total: </span>
                        <p class="text-2xl">R${{ price.toFixed(2) }}</p>
                    </div>
                    <div class="flex relative items-center my-6">
                        <label class="label mr-auto">
                            <span class="text-xl">Valor recebido:</span>
                        </label>
                        <input type="number" step="any" v-model="state.received" class="input">
                        <div class="absolute text-sm transform translate-y-full right-0 bottom-0 ml-auto gap-2" v-if="v$.received.$error">
                            {{ v$.received.$errors[0].$message }}
                        </div>
                    </div>

                    <div
                    v-if="back < 0"
                    class="flex items-center my-6">
                        <span class="text-xl mr-auto">Falta:</span>
                        <p class="text-2xl">R${{ (-back).toFixed(2) }}</p>
                    </div>

                    <div
                    v-else
                    class="flex items-center my-6">
                        <span class="text-xl mr-auto">Troco:</span>
                        <p class="text-2xl">R${{ back.toFixed(2) }}</p>
                    </div>

                    <div class="bg-base-200 p-2 mt-8 flex justify-end">
                        <button type="submit" class="btn btn-sm btn-primary btn-outline">Confirmar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import useVuelidate from '@vuelidate/core'
    import { required, minValue, numeric } from '@vuelidate/validators'
    import { defineEmits, defineProps, computed, ref} from 'vue'
    import Payment from '../../interfaces/payments/payment.interface'
    import PaymentService from '../../services/paymentService'
    import { useStore } from '../../stores/cashregister'

    interface Emits {
        (e: 'close'): void
        (e: 'paid', amount: number): void
    }

    interface Props {
        payment: Payment;
    }

    const props = defineProps<Props>()
    const emit = defineEmits<Emits>()
    const price = computed(() => parseFloat(props.payment.amount))
    const state = ref({
        received: 0,
    })
    const back = computed(() => state.value.received - price.value)
    const paidAmount = computed(() => state.value.received - (back.value > 0 ? back.value : 0))
    const store = useStore()

    const rules = {
        received: { required, minValue: minValue(1), numeric, $autoDirty: true }
    }

    const v$ = useVuelidate(rules, state)

    const payOrder = async () => {
        if(props.payment.id) {
            try {
                await v$.value.$validate()
                if (v$.value.$error) return

                await store.getCashRegister()
                const cashRegisterId = store.cashRegister.id ? store.cashRegister.id : undefined
                await PaymentService().deposit(props.payment.id, paidAmount.value, cashRegisterId)
                emit('paid', paidAmount.value)
            }
            catch(e) {
                return
            }
        }
    }
</script>