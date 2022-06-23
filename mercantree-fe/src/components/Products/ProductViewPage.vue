<template>
    <div>
        <h1 class="text-2xl mb-12">Alterar produto</h1>
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
        </form>
        
        <div class="flex justify-end gap-4 bg-base-200 p-4">
            <button
            class="btn btn-error btn-sm btn-outline"
            @click.prevent="deleteProduct()">
                Deletar
            </button>

            <button
            class="btn btn-primary btn-sm"
            @click.prevent="updateProduct()">
                Salvar
            </button>
        </div>

        <ProductCategoryModal
        v-if="editCategories"
        @close="editCategories = false, getCategories()" />
    </div>
</template>

<script setup lang="ts">

import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"
import swal from "sweetalert"
import { computed, onBeforeMount, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { APIListResponse } from "../../interfaces/common/response.interface"
import Category from "../../interfaces/products/category.interface"
import { Product } from "../../interfaces/products/product.interface"
import categoryService from "../../services/categoryService"
import errorService from "../../services/errorService"
import ProductService from "../../services/productService"
import ProductCategoryModal from "./ProductCategoryModal.vue"

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

const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
const isLoading = ref(false)
const route = useRoute()
const router = useRouter()
const editCategories = ref(false)

const id = parseInt(route.params.id.toString())

const getProduct = async () => {
    isLoading.value = true
    const response = await ProductService().retrieve(id)
    isLoading.value = false
    state.value = response
}

const updateProduct = async () => {
    try {
        await v$.value.$validate
        if(v$.value.$error) return

        isLoading.value = true
        const response = await ProductService().update(id, state.value)

        isLoading.value = false

        await swal('Sucesso', 'Produto editado', 'success')
    } catch(e) {
        return
    }
}

const deleteProduct = async () => {
            try {
                await errorService().onWarn()

                const response = await ProductService().destroy(id)

                await swal('Sucesso', 'Produto deletado', 'success')

                router.push('/products/outofstock')
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

const categoryReducer = (c: Category) => c.name

onBeforeMount(async () => {
    await getProduct()
    await getCategories()
})

</script>