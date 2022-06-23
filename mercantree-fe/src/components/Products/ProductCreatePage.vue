<template>
    <div>
        <div v-if="step === 1">
            <h1 class="text-2xl mb-12">Adicionar produto</h1>
            <h2 class="mb-4">Preencha todos os campos e escolha uma das ações.</h2>

            <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
                <div class="flex gap-4">
                    <label class="label">
                        <span class="label-text">* Nome:</span>
                    </label>

                    <input
                    v-model="state.name"
                    type="text" 
                    class="input max-w-md input-sm input-bordered">

                    <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.name.$error">
                        {{ v$.name.$errors[0].$message }}
                    </div>
                </div>
                <div class="flex gap-4 w-full my-4">
                    <label class="label">
                        <span class="label-text">Descrição:</span>
                    </label>

                    <input
                    v-model="state.description"
                    type="text"
                    class="input max-w-md input-sm input-bordered">
                </div>
                <div class="flex gap-4 w-full my-4">
                    <label class="label">
                        <span class="label-text">Categoria:</span>
                    </label>

                    <v-select
                    v-model="state.category"
                    class="w-full max-w-xs"
                    label="name"
                    :reduce="categoryReducer"
                    :options="categories.results" />
                    
                    <button type="button" @click="editCategories = true" class="btn btn-sm btn-square">
                        <font-awesome-icon icon="edit" />
                    </button>
                </div>
                <div class="flex gap-4 w-full my-4">
                    <label class="label">
                        <span class="label-text">Código de barras:</span>
                    </label>

                    <input
                    v-model="state.barcode"
                    type="text"
                    class="input max-w-md input-sm input-bordered">
                </div>
                <div class="flex justify-end gap-4 bg-base-200 p-4">
                    <button class="btn btn-primary btn-sm" @click.prevent="createProduct()">Salvar</button>
                </div>
            </form>

            <ProductCategoryModal
            v-if="editCategories"
            @close="editCategories = false, getCategories()" />
        </div>

        <div v-if="step === 2">
            <h1 class="text-2xl mb-12">Adicionar estoque ao produto</h1>
            <h2 class="mb-4">Preencha todos os campos e escolha uma das ações.</h2>

            <StockForm
            v-if="stockProduct.product"
            :state="stockProduct"
            @submit="state => createStockProduct(state)"
            @cancel="skipStock()">            
                <template #cancel-message>
                    Não adicionar estoque agora
                </template>
            </StockForm>
        </div>
    </div>
</template>

<script setup lang="ts">

import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import swal from "sweetalert"
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { APIListResponse } from "../../interfaces/common/response.interface"
import Category from "../../interfaces/products/category.interface"
import { Product } from "../../interfaces/products/product.interface"
import StockProduct from "../../interfaces/products/stock_product.interface"
import categoryService from "../../services/categoryService"
import ProductService from "../../services/productService"
import StockProductService from "../../services/stockService"
import ProductCategoryModal from "./ProductCategoryModal.vue"
import StockForm from "./StockForm.vue"

const state = ref<Product>({
    name: '',
    description: '',
    barcode: '',
    supplier_id: undefined,
    category: '',
})

const rules = computed(() => ({
    name: { required, $autoDirty: true },
}))

const v$ = useVuelidate(rules, state)

const stockProduct = ref<StockProduct>({
    quantity: '0',
    price: '0',
    purchase_price: '0',
    delete_on_deplete: false,
    product: 0
})

const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
const isLoading = ref(false)
const step = ref(1)
const router = useRouter()
const editCategories = ref(false)

const createProduct = async () => {
    try {
        await v$.value.$validate
        if(v$.value.$error) return

        isLoading.value = true
        const response = await ProductService().create(state.value)

        if(response.id) {
            stockProduct.value.product = response.id
        }

        isLoading.value = false

        await swal('Sucesso', 'Produto criado', 'success')
        step.value = 2
    } catch(e) {
        return
    }
}

const createStockProduct = async (state: StockProduct) => {
    try {
        isLoading.value = true
        await StockProductService().create(state)
        isLoading.value = false

        await swal('Sucesso', 'Produto criado', 'success')

        router.push('/stock')
    } catch(e) {
        return
    }
}

const skipStock = () => {
    router.push('/stock/products')
}

const getCategories = async () => {
    try {
        const response = await categoryService().list()
        categories.value = response
    }
    catch(e) {
        return
    }
}

const categoryReducer = (c: Category) => c.name

onMounted(async () => {
    await getCategories()
})

</script>