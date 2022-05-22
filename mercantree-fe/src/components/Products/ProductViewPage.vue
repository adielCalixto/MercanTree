<template>
    <div>
        <h1 class="text-2xl mb-12">Alterar produto</h1>
        <h2 class="font-bold text-xl mb-8">{{ product.name }}</h2>

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
                <button class="btn btn-error btn-outline btn-sm" @click.prevent="deleteProduct()">Deletar</button>
                <button class="btn btn-secondary btn-sm" @click.prevent="updateProduct()">Salvar</button>
            </div>
        </form>

        <ProductCategoryModal
        v-if="editCategories"
        @close="editCategories = false, getCategories()" />
    </div>
</template>

<script lang="ts">

import { defineComponent, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import productsService from "../../services/modules/products.module"
import { Product } from '../../interfaces/products/product.interface'
import ProductCategoryModal from "./ProductCategoryModal.vue"
import { APIListResponse } from "../../interfaces/common/response.interface"
import Category from "../../interfaces/products/category.interface"
import categoryService from "../../services/modules/category.module"
import supplierModule from "../../services/modules/supplier.module"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"

export default defineComponent({
    components: {
        ProductCategoryModal,
    },
    async setup() {
        const route = useRoute()
        const router = useRouter()
        const id = parseInt(route.params.id.toString())
        const product = ref<Product>({
            name: '',
            description: '',
            price: 0,
            barcode: '',
            supplier_id: undefined,
            category: '',
            expires_at: '2022-01-01',
            supplier_price: 0.0,
            quantity: 0,
        })
        const editCategories = ref(false)
        const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
        const suppliers = ref<APIListResponse<Supplier>>({ count: 0, results: [] })

        const error = ref()
        const isLoading = ref(false)

        const getProduct = async () => {
            try {
                isLoading.value = true
                const response = await productsService.retrieve(id)
                product.value = response
                isLoading.value = false
            } catch(e) {
                router.push('/products')
            }
        }

        const updateProduct = async () => {
            try {
                const response = await productsService.update(id, product.value)
                product.value = response
                router.push('/products')
            } catch(e) {
                error.value = e
            }
        }

        const deleteProduct = async () => {
            try {
                const response = await productsService.destroy(id)
                router.push('/products')
            } catch(e) {
                error.value = e
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

        const getSuppliers = async () => {
            try {
                const response = await supplierModule.list()
                suppliers.value = response
            }
            catch(e) {
                console.error(e)
            }
        }

        const categoryReducer = (c: Category) => c.name
        const supplierReducer = (s: Supplier) => s.id

        onMounted(async () => {
            await getProduct()
            await getCategories()
            await getSuppliers()
        })

        return {
            product,
            error,
            isLoading,
            updateProduct,
            deleteProduct,
            categories,
            editCategories,
            getCategories,
            suppliers,
            categoryReducer,
            supplierReducer,
        }
    },
})
</script>