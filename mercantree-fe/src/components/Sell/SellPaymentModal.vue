<template>
    <div>
        <h1 class="text-xl text-base-content mb-8">Tipo de pagamento</h1>
        <div class="collapse collapse-open">
            <div class="collapse-title bg-primary text-primary-content">
                Dinheiro
            </div>
            <div class="collapse-content bg-base-200 text-nase-content"> 
                <form method="POST">
                    <div class="flex items-center my-4">
                        <span class="text-xl mr-auto">Valor total: </span>
                        <p class="text-2xl">R${{ price }}</p>
                    </div>
                    <div class="flex items-center my-4">
                        <label class="label mr-auto">
                            <span class="text-xl">Valor recebido:</span>
                        </label>
                        <input type="number" v-model="received" class="input">
                    </div>
                    <div class="flex items-center my-4">
                        <span class="text-xl mr-auto">Troco:</span>
                        <p class="text-2xl">R${{ back }}</p>
                    </div>
                </form>

                <div class="bg-base-200 p-2 mt-8 flex justify-end">
                    <button @click="payOrder" class="btn btn-sm btn-primary btn-outline">Confirmar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { defineEmits, defineProps, computed, ref} from 'vue'
    import Payment from '../../interfaces/payments/payment.interface'
    import PaymentService from '../../services/paymentService';
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
    const price = computed(() => props.payment.amount)
    const received = ref(0)
    const back = computed(() => received.value - price.value)
    const paidAmount = computed(() => received.value - (back.value > 0 ? back.value : 0))
    const store = useStore()

    const payOrder = async () => {
        if(props.payment.id) {
            try {
                await store.getCashRegister()
                const cashRegisterId = store.cashRegister.id ? store.cashRegister.id : undefined
                await PaymentService().deposit(props.payment.id, paidAmount.value, cashRegisterId)
                emit('paid', paidAmount.value)
            }
            catch(e) {
                console.error(e)
            }
        }
    }
</script>