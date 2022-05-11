<template>
    <div class="flex flex-col gap-4">
        <div class="form bg-base-200 p-2">
            <div class="flex flex-col items-center md:flex-row md:items-end gap-4 mb-8">
                <form @submit.prevent="createModalOpen = true" method="post">
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">(Nome, Código de barras, Descrição)</span>
                        </label>
                        <input type="text" v-model="search" class="input max-w-md input-sm input-bordered">
                    </div>
                </form>

                <div v-if="product != undefined">
                    {{ product.name }}
                </div>

                <div class="flex md:ml-auto">
                    <div>
                        <input type="number" v-model="quantity" placeholder="Quantidade" class="input max-w-md input-sm input-bordered">
                    </div>

                    <div>
                        <button @click="addProduct()" class="btn btn-square btn-sm">+</button>
                    </div>
                </div>
            </div>

            <table class="table table-compact w-full">
                <thead>
                    <tr>
                        <th></th>
                        <th>Produto</th>
                        <th>Quantidade</th>
                        <th>Preço unt.</th>
                    </tr>
                </thead>
                
                <tbody>
                    <tr v-for="p in products">
                        <td></td>
                        <td>{{ p.data.name }}</td>
                        <td>{{ p.quantity }}</td>
                        <td>{{ p.data.price }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="details bg-base-200">
                <textarea class="textarea textarea-primary w-full h-full resize-none" :readonly="true" placeholder="Detalhes..."></textarea>
            </div>

            <div class="prices bg-base-200">
                <div class="bg-base-300 p-4">
                    <div class="text-xs text-gray-600 flex justify-between">
                        <p>Subtotal</p>
                        <p>$40,00</p>
                    </div>

                    <div class="divider my-1"></div> 

                    <div class="text-xs text-gray-600 flex justify-between">
                        <p>Desconto</p>
                        <p>$10,00</p>
                    </div>

                    <div class="divider my-1"></div> 

                    <div class="text-md text-base-content flex justify-between">
                        <p>Total    =</p>
                        <p>${{ price }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-base-200 p-2 flex justify-end">
            <button @click="payOrder()" class="btn btn-sm btn-error btn-outline">Pagar</button>
        </div>

        <div class="modal modal-open" v-if="createModalOpen">
            <div class="modal-box max-w-2xl">
                <sell-products-modal :search="search" @close="createModalOpen = false" @selected="p => { preloadProduct(p) }" />
            </div>
        </div>

        <div class="modal modal-open" v-if="paymentModalOpen">
            <div class="modal-box max-w-2xl">
                <sell-payment-modal v-if="payment" :payment="payment" @close="paymentModalOpen = false" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent, ref, computed } from 'vue'
    import OrderService from '../../services/modules/order.module'
    import Order from '../../interfaces/orders/order.interface'
    import OrderProduct from '../../interfaces/orders/order_product.interface'
    import { Product } from '../../interfaces/products/product.interface'
    import { useStore } from '../../stores/auth'
    import SellProductsModal from './SellProductsModal.vue'
    import SellPaymentModal from './SellPaymentModal.vue'
    import paymentModule from '../../services/modules/payment.module'
    import Payment from '../../interfaces/payments/payment.interface'
import order_productModule from '../../services/modules/order_product.module'

    interface ProductWithQuantity {
        quantity: number;
        data: Product;
    }

    export default defineComponent({
    components: {
        SellProductsModal,
        SellPaymentModal,
    },
    setup() {
        const search = ref("");
        const quantity = ref(0)
        const error = ref();
        const store = useStore();
        const product = ref<Product>();
        const products = ref<ProductWithQuantity[]>([])
        const payment = ref<Payment>();
        const createModalOpen = ref(false);
        const paymentModalOpen = ref(false);
        const price = computed(() => {
            return products.value.reduce((prev: number, current) => {
                const price = prev + (current.data.price * current.quantity)
                return price
            }, 0)
        })

        const saveOrder = async () => {
            try {
                if (payment.value !== undefined) {
                    const order: Order = {
                        user: store.id,
                        payment: payment.value.id
                    }

                    const response = await OrderService.create(order);

                    products.value.map(async (p) => {
                        order_productModule.create({
                            order: response.id,
                            product: p.data.id,
                            quantity: p.quantity
                        })
                    })
                }
            }
            catch (e) {
                error.value = e;
            }
        }

        const payOrder = async () => {
            if(payment.value == undefined) {
                const response = await paymentModule.create({
                    amount: price.value.toFixed(2),
                    is_paid: false,
                })

                payment.value = response

                saveOrder()

                paymentModalOpen.value = true
            }
        }

        const preloadProduct = (p: Product) => {
            product.value = p
            createModalOpen.value = false
        }

        const addProduct = () => {
            if(product.value != undefined) {
                products.value.push({
                    data: product.value,
                    quantity: quantity.value,
                })
            }
        }

        return {
            search,
            product,
            error,
            saveOrder,
            payOrder,
            payment,
            createModalOpen,
            paymentModalOpen,
            addProduct,
            preloadProduct,
            quantity,
            products,
            price,
        };
    },
})
</script>