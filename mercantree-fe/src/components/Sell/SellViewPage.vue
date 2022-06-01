<template>
    <div>
        <h1 class="text-2xl font-semibold">Visualizar venda</h1>

        <div class="tabs mb-8 ml-4">
            <a
            @click="activeTab=0"
            class="tab tab-bordered"
            :class="{'tab-active': activeTab == 0}">Detalhes</a> 

            <a
            @click="activeTab=1"
            class="tab tab-bordered"
            :class="{'tab-active': activeTab == 1}">Pagamento</a>
        </div>

        <div v-if="activeTab == 0" class="bg-base-200">
            <h2 class="text-lg font-semibold mb-4">Detalhes:</h2>
            <div class="flex flex-col gap-1 text-base">
                <p>Data: <b>{{ new Date(order?.created ?? '').toLocaleString('pt-BR') }}</b></p>
                <p>Valor: <b>{{ get_price(order?.payment.amount ?? '') }}</b></p>
                <p>Valor pago: <b>{{ get_price(order?.payment.paid_amount ?? '') }}</b></p>
                <p>Cadastrante: <b>{{ order?.user.username }}</b></p>
                <p>Observações: <b>{{ order?.details }}</b></p>
            </div>

            <div class="mt-8">
                <h3 class="text-lg mb-4">Produtos:</h3>
                <div class="w-full">
                    <div v-for="p in order?.products" class="flex gap-4 text-lg border-b-2 border-base-300 mb-2">
                        <p>{{ order?.products.indexOf(p) }}</p>
                        <p>{{ p.product.name }}</p>
                        <div class="flex gap-4 ml-auto">
                            <p class="text-gray-500">{{ p.quantity }} X {{ get_price(p.product.price) }}</p>
                            <p class="font-bold">= R${{ (parseFloat(p.product.price) * p.quantity).toFixed(2) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-else-if="activeTab == 1" class="bg-base-200">
            <h2 class="text-lg font-semibold mb-4">Pagamento:</h2>

            <div>
                <p>Valor: <b>{{ get_price(order?.payment.amount ?? '') }}</b></p>
                <p>Valor pago: <b>{{ get_price(order?.payment.paid_amount ?? '') }}</b></p>
            </div>

            <form @submit.prevent="addAmount()" method="POST" class="flex gap-4 print:hidden my-4 justify-end">
                <div class="form-control">
                    <input
                    class="input input-sm input-success"
                    type="number"
                    v-model="formAmount">
                </div>
                <button type="submit" class="btn btn-success btn-sm text-primary">
                    Adicionar quantia
                    <font-awesome-icon icon="add" />
                </button>
            </form>

            <form @submit.prevent="addAmount()" method="POST" class="flex gap-4 print:hidden my-4 justify-end">
                <div class="form-control">
                    <input
                    class="input input-sm input-success"
                    type="number"
                    v-model="formAmount">
                </div>
                <button type="submit" class="btn btn-success btn-sm text-primary">
                    Devolução
                    <font-awesome-icon icon="add" />
                </button>
            </form>

        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { ExpandedOrder } from '../../interfaces/orders/order.interface'
import OrderService from '../../services/orderService'
import { useRoute } from 'vue-router'
import get_price from '../../utils/get_price'
import PaymentService from '../../services/paymentService'
import { useStore } from '../../stores/cashregister'
import swal from 'sweetalert'
import errorService from '../../services/errorService'

const order = ref<ExpandedOrder>()
const route = useRoute()
const store = useStore()
const id = computed(() => route.params.id.toString())
const formAmount = ref()
const activeTab = ref(0)

const getOrder = async () => {
    try {
        const response = await OrderService().retrieveExpanded(parseInt(id.value))
        order.value = response
    }
    catch(e) {
        return
    }
}

const addAmount = async () => {
    try {
        if(order.value?.payment.is_paid) {
            return swal('Atenção', 'Valor total já foi pago', 'warning')
        }

        errorService().onWarn('Tem certeza?', 'Você está prestes a depositar uma quantia nesta venda')
        .then(async () => {
            if (!order.value?.payment.id) return

            await store.getCashRegister()
            const cashRegisterId = store.cashRegister.id ? store.cashRegister.id : undefined
            await PaymentService().deposit(order.value.payment.id, formAmount.value, cashRegisterId)
            getOrder()
        })
        .catch(() => {
            return
        })

    }
    catch(e) {
        return
    }
}

onMounted(async () => {
    await getOrder()
})

</script>