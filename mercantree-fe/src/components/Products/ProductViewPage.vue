<template>
    <div>
        <h1 class="text-2xl mb-12">Alterar produto</h1>
        <h2 class="font-bold text-xl mb-8">{{ product?.name }}</h2>

        <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
            <div class="flex gap-4">
                <label class="label">
                    <span class="label-text font-semibold">Nome:</span>
                </label>

                <input
                v-model="product.name"
                type="text" 
                class="input max-w-md input-sm input-bordered">

                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.name.$error">
                    {{ v$.name.$errors[0].$message }}
                </div>
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Descrição:</span>
                </label>

                <input
                v-model="product.description"
                type="text"
                class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Categoria:</span>
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
                    <span class="label-text font-semibold">Preço:</span>
                </label>

                <input
                min="0"
                v-model="product.price"
                type="number"
                class="input max-w-md input-sm input-bordered">

                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.price.$error">
                    {{ v$.price.$errors[0].$message }}
                </div>
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Preço de custo:</span>
                </label>

                <input
                min="0"
                v-model="product.supplier_price"
                type="number"
                class="input max-w-md input-sm input-bordered">

                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.supplier_price.$error">
                    {{ v$.supplier_price.$errors[0].$message }}
                </div>
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Quantidade:</span>
                </label>

                <input
                min="0"
                v-model="product.quantity"
                type="number"
                class="input max-w-md input-sm input-bordered">

                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.quantity.$error">
                    {{ v$.quantity.$errors[0].$message }}
                </div>
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Quantidade em estoque:</span>
                </label>

                <input
                min="0"
                v-model="product.stock_quantity"
                type="text"
                class="input max-w-md input-sm input-bordered"
                readonly>
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Validade:</span>
                </label>
                <input
                v-model="product.expires_at"
                type="date"
                class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Código de barras:</span>
                </label>

                <input
                v-model="product.barcode"
                type="text"
                class="input max-w-md input-sm input-bordered">
            </div>
            <div class="flex gap-4 w-full my-4">
                <label class="label">
                    <span class="label-text font-semibold">Fornecedor</span>
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
                <button class="btn btn-success btn-sm text-primary" @click.prevent="updateProduct()">Salvar</button>
            </div>
        </form>

        <ProductCategoryModal
        v-if="editCategories"
        @close="editCategories = false, getCategories()" />
    </div>
</template>

<script lang="ts">

import { computed, defineComponent, onMounted, reactive, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import productsService from "../../services/productService"
import { Product } from '../../interfaces/products/product.interface'
import ProductCategoryModal from "./ProductCategoryModal.vue"
import { APIListResponse } from "../../interfaces/common/response.interface"
import Category from "../../interfaces/products/category.interface"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"
import categoryService from "../../services/categoryService"
import SupplierService from "../../services/supplierService"
import swal from "sweetalert"
import useVuelidate from "@vuelidate/core"
import { decimal, minValue, numeric, required } from "@vuelidate/validators"
import errorService from "../../services/errorService"

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
            price: '0.00',
            barcode: '',
            supplier_id: undefined,
            category: '',
            expires_at: undefined,
            supplier_price: '0.0',
            quantity: 0,
        })

        const rules = computed(() => ({
            name: { required, $autoDirty: true },
            price: { required, decimal, minValue: minValue(product.value.supplier_price), $autoDirty: true },
            supplier_price: { required, decimal, minValue: minValue(0), $autoDirty: true },
            quantity: { required, numeric, minValue: minValue(1), $autoDirty: true },
        }))

        const v$ = useVuelidate(rules, product)
        
        const editCategories = ref(false)
        const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
        const suppliers = ref<APIListResponse<Supplier>>({ count: 0, results: [] })

        const isLoading = ref(false)

        const getProduct = async () => {
            try {
                isLoading.value = true
                const response = await productsService().retrieve(id)
                product.value = response
                isLoading.value = false
            } catch(e) {
                router.push('/products')
            }
        }

        const updateProduct = async () => {
            try {
                await v$.value.$validate()
                if (v$.value.$error) return

                const response = await productsService().update(id, product.value)
                product.value = response
                
                await swal('Sucesso', 'Produto editado', 'success')

                router.push('/products')
            } catch(e) {
                return
            }
        }

        const deleteProduct = async () => {
            try {
                await errorService().onWarn()

                const response = await productsService().destroy(id)

                await swal('Sucesso', 'Produto deletado', 'success')

                router.push('/products')
            } catch(e) {
                return
            }
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

        const getSuppliers = async () => {
            try {
                const response = await SupplierService().list()
                suppliers.value = response
            }
            catch(e) {
                return
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
            v$,
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