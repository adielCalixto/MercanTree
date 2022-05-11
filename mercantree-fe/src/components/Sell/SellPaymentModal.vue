<template>
    <div>
        <h1 class="text-xl text-base-content mb-8">Tipo de pagamento</h1>
        <div class="collapse collapse-open">
            <div @click="e => { e.target?.parentNode.classList.toggle('collapse-open') }" class="collapse-title bg-primary text-primary-content">
                Dinheiro
            </div>
            <div class="collapse-content bg-base-200 text-nase-content"> 
                <form method="POST">
                    <div class="flex items-center my-4">
                        <span class="text-xl mr-auto">Valor total: </span>
                        <p class="text-2xl">${{ price }}</p>
                    </div>
                    <div class="flex items-center my-4">
                        <label class="label mr-auto">
                            <span class="text-xl">Valor recebido:</span>
                        </label>
                        <input type="number" v-model="received" class="input">
                    </div>
                    <div class="flex items-center my-4">
                        <span class="text-xl mr-auto">Troco:</span>
                        <p class="text-2xl">${{ back }}</p>
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
    import { defineComponent, defineEmits, defineProps, computed, ref} from 'vue'
    import Payment from '../../interfaces/payments/payment.interface';
    import paymentModule from '../../services/modules/payment.module';

    interface Emits {
        (e: 'close'): void
    }

    interface Props {
        payment: Payment;
    }

    const props = defineProps<Props>()
    const emit = defineEmits<Emits>()
    const price = computed(() => parseFloat(props.payment.amount))
    const received = ref(0)
    const back = computed(() => received.value - price.value)

    const payOrder = async () => {
        if(props.payment.id) {
            const response = await paymentModule.charge(props.payment.id, (received.value - back.value))
            emit('close')
        }
    }
</script>