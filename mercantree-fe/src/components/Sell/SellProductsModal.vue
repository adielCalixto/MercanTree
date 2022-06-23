<template>
    <div>
        <div v-if="products.count === 0">
            <p class="text-lg font-semibold">Nenhum produto encontrado</p>
            <router-link to="/products/create">
                Cadastrar produto
                <font-awesome-icon icon="external-link" />
            </router-link>
        </div>
        <mt-table class="overflow-y-auto relative max-h-72" :table="table" v-else>
            <tr v-for="product in products.results">
                <th>
                    <button @click="$emit('selected', product)" class="btn btn-sm btn-square">
                        <font-awesome-icon icon="add" />
                    </button>
                </th>
                <th> {{ product.product.name }} </th>
                <th> {{ product.product.description }} </th>
                <th> {{ product.price }} </th>
                <th> {{ product.quantity }} </th>
                <th> {{ product.product.category }} </th>
                <th> {{ product.product.barcode }} </th>
            </tr>
        </mt-table>
        <button @click="$emit('close')" class="btn btn-sm btn-outline mt-4">
            Close
            <font-awesome-icon class="ml-2" icon="close" />
        </button>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, onMounted } from 'vue'
    import { APIListResponse } from '../../interfaces/common/response.interface'
    import { PAGE_SIZE } from '../../consts'
    import { useStore as useConfigStore } from '../../stores/config'
    import MtTable from '../MtTable.vue'
    import stockService from '../../services/stockService'
    import StockProduct from '../../interfaces/products/stock_product.interface'
    import { Product } from '../../interfaces/products/product.interface'

    interface Props {
        search: string;
    }

    interface Emits {
        (e: 'selected', value: StockProduct & { product: Product }): void,
        (e: 'close'): void,
    }

    const error = ref()
    const emit = defineEmits<Emits>()
    const props = defineProps<Props>()
    const products = ref<APIListResponse<StockProduct & { product: Product }>>({ count: 0, results: [] })
    const configStore = useConfigStore()
    const pages = computed(() => Math.floor((products.value.count + PAGE_SIZE - 1) / PAGE_SIZE))
    const activePage = ref(1)

    const table = {
        name: 'Produtos',
        fields: [
            '',
            'Nome',
            'Descrição',
            'Preço',
            'Em estoque',
            'Categoria',
            'Código de barras',
        ],
    }

    const listProducts = async () => {
        try {
            const response = await stockService().listExpanded(activePage.value, props.search)
            products.value = response

            if(configStore.add_product_to_order_when_unique) {
                if(products.value.count == 1) {
                    emit('selected', products.value.results[0])
                }
            }
        }
        catch(e) {
            error.value = e
        }
    }

    onMounted(listProducts)
</script>