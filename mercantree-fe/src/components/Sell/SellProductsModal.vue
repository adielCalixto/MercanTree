<template>
    <div>
        <mt-table :table="table">
            <tr v-for="product in products.results">
                <th>
                    <button @click="$emit('selected', product)" class="btn btn-sm btn-square">
                        <font-awesome-icon icon="add" />
                    </button>
                </th>
                <th> {{ product.name }} </th>
                <th> {{ product.description }} </th>
                <th> {{ product.price }} </th>
                <th> {{ product.barcode }} </th>
                <th> {{ product.quantity }} </th>
                <th> {{ product.stock_quantity }} </th>
                <th> {{ product.category }} </th>
            </tr>
        </mt-table>
        <button @click="$emit('close')" class="btn btn-sm btn-outline mt-4">
            Close
            <font-awesome-icon class="ml-2" icon="close" />
        </button>
    </div>
</template>

<script setup lang="ts">
    import { ref, defineProps, computed, defineEmits, onMounted } from 'vue'
    import { Product } from '../../interfaces/products/product.interface'
    import { APIListResponse } from '../../interfaces/common/response.interface';
    import { PAGE_SIZE } from '../../consts'
    import { useStore as useConfigStore } from '../../stores/config';
    import MtTable from '../MtTable.vue'
    import ProductService from '../../services/productService';

    interface Props {
        search: string;
    }

    interface Emits {
        (e: 'selected', value: Product): void,
        (e: 'close'): void,
    }

    const error = ref()
    const emit = defineEmits<Emits>()
    const props = defineProps<Props>()
    const products = ref<APIListResponse<Product>>({ count: 0, results: [] })
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
            'Código de barras',
            'Quantidade',
            'Em estoque',
            'Categoria',
        ],
    }

    const listProducts = async () => {
        try {
            const response = await ProductService().list(activePage.value, props.search)
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