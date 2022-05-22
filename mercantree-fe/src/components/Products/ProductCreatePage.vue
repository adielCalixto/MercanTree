<template>
    <div>
        <h1 class="text-2xl mb-12">Adicionar produto</h1>
        <h2 class="mb-4">Preencha todos os campos e escolha uma das ações.</h2>

        <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
            <div class="flex gap-4">
                <label class="label">
                    <span class="label-text">Nome:</span>
                </label>
                <input v-model="product.name" type="text"  class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Descrição:</span>
                </label>
                <input v-model="product.description" type="text" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Categoria:</span>
                </label>

                <v-select
                v-model="product.category"
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
                    <span class="label-text">Preço:</span>
                </label>
                <input v-model="product.price" type="number" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Preço de compra:</span>
                </label>
                <input v-model="product.supplier_price" type="number" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Quantidade:</span>
                </label>
                <input v-model="product.quantity" type="number" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Validade:</span>
                </label>
                <input v-model="product.expires_at" type="date" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Código de barras:</span>
                </label>
                <input v-model="product.barcode" type="text" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text">Fornecedor</span>
                </label>

                <v-select
                v-model="product.supplier_id"
                class="w-full max-w-xs"
                label="name"
                :reduce="supplierReducer"
                :options="suppliers.results" />
            </div>
            <div class="flex justify-end gap-4 bg-base-200 p-4">
                <button class="btn btn-secondary btn-outline btn-sm" @click.prevent="createProduct()">Salvar e adicionar outro</button>
                <button class="btn btn-primary btn-sm" @click.prevent="createProduct(true)">Salvar</button>
            </div>
        </form>

        <ProductCategoryModal
        v-if="editCategories"
        @close="editCategories = false, getCategories()" />
    </div>
</template>

<script lang="ts">

import { defineComponent, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { APIListResponse } from "../../interfaces/common/response.interface"
import Category from "../../interfaces/products/category.interface"
import { Product } from "../../interfaces/products/product.interface"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"
import categoryService from "../../services/modules/category.module"
import ProductService from "../../services/modules/products.module"
import supplierModule from "../../services/modules/supplier.module"
import ProductCategoryModal from "./ProductCategoryModal.vue"

export default defineComponent({
    components: {
        ProductCategoryModal,
    },
    setup() {
        const product = ref<Product>({
            name: '',
            description: '',
            price: 0,
            barcode: '',
            supplier_id: undefined,
            supplier_price: 0.0,
            quantity: 0,
            category: '',
            expires_at: '2021-12-01',
        })
        const suppliers = ref<APIListResponse<Supplier>>({ count: 0, results: [] })
        const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
        const error = ref()
        const isLoading = ref(false)
        const router = useRouter()
        const editCategories = ref(false)

        const createProduct = async (redirect: boolean = false) => {
            try {
                isLoading.value = true
                const response = await ProductService.create(product.value)
                isLoading.value = false

                if(redirect) {
                    router.push('/products')
                }
            } catch(e) {
                error.value = e
            }
        }

        const getSuppliers = async () => {
            try {
                const response = await supplierModule.list()
                suppliers.value = response
            }
            catch(e) {
                console.error(e)
            }
        }

        const getCategories = async () => {
            try {
                const response = await categoryService().list()
                categories.value = response
            }
            catch(e) {
                console.error(e)
            }
        }

        const categoryReducer = (c: Category) => c.name
        const supplierReducer = (s: Supplier) => s.id

        onMounted(async () => {
            await getSuppliers()
            await getCategories()
        })

        return {
            product,
            isLoading,
            error,
            createProduct,
            suppliers,
            editCategories,
            categories,
            getCategories,
            categoryReducer,
            supplierReducer,
        }
    },
})
</script>