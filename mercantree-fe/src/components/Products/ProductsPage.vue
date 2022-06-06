<template>
    <div>
        <h1 class="text-xl mb-12 font-bold">Lista de Produtos</h1>

        <div class="my-4 flex justify-between">
            <router-link :to="$route.fullPath + '/create'" class="btn btn-success btn-sm text-base-100">Adicionar</router-link>
            <select v-model="ordering"
            @change="listProducts()"
            class="select select-sm select-bordered ml-auto mr-4">
                <option value="" disabled selected>Ordenar</option>
                <option value="name">Nome-ASC</option>
                <option value="-name">Nome-DESC</option>
                <option value="price">Preço-ASC</option>
                <option value="-price">Preço-DESC</option>
            </select>
            <div class="form-control">
                <div class="input-group">
                    <input
                    type="text"
                    placeholder="Search…"
                    class="input input-sm input-bordered"
                    v-model="search" >

                    <button @click="activePage = 1, listProducts()" class="btn btn-square btn-sm">
                        <font-awesome-icon icon="search" />
                    </button>
                </div>
            </div>
        </div>

        <div v-if="products.count == 0">
            Nenhum produto encontrado
        </div>

        <mt-table :table="table" v-else >
            <tr v-for="product in products.results">
                <th> {{ product.id }}</th>
                <th> {{ product.name }} </th>
                <th> {{ product.description }} </th>
                <th> {{ format_date(product.expires_at) }} </th>
                <th> {{ product.price }} </th>
                <th> {{ product.barcode }} </th>
                <th> {{ product.quantity }} </th>
                <th> {{ product.category }} </th>
                <th>
                    <router-link v-if="product.supplier_id" :to="`/suppliers/supplier/${product.supplier_id}`" class="btn btn-rounded btn-sm">
                        <font-awesome-icon icon="external-link" />
                    </router-link>
                </th> 
                <th>
                    <router-link :to="`/products/product/${product.id}`" class="btn btn-success btn-sm text-base-100">View</router-link>
                </th>
            </tr>
        </mt-table>

        <div class="w-full flex justify-center mt-4">
            <div class="btn-group">
                <button class="btn btn-sm"
                v-for="page in pages"
                :class="{'btn-active': page == activePage}"
                @click="activePage = page, listProducts()">{{ page }}</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">

import { defineComponent, ref, computed, onBeforeMount } from 'vue'
import MtTable from "../MtTable.vue"
import ProductService from '../../services/productService'
import { Product } from '../../interfaces/products/product.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'
import { RouterLink } from 'vue-router'
import { PAGE_SIZE } from '../../consts'
import format_date from "../../utils/format_date"

export default defineComponent({
    components: {
        MtTable,
        RouterLink,
    },
    methods: {
        format_date,
    },
    async setup() {
        const table = {
            name: 'Produtos',
            fields: [
                '',
                'Nome',
                'Descrição',
                'Validade',
                'Price',
                'Código de barras',
                'Quantidade',
                'Categoria',
                'Fornecedor',
                '',
            ],
        }

        const search = ref('')
        const ordering = ref('')
        const error = ref()
        const products = ref<APIListResponse<Product>>({count: 0, results: []})
        const isLoading = ref(false)
        const pages = computed(() => Math.floor((products.value.count + PAGE_SIZE - 1) / PAGE_SIZE))
        const activePage = ref(1)

        const listProducts = async () => {
            try {
                isLoading.value = true
                const response = await ProductService().list(activePage.value, search.value, ordering.value)
                products.value = response
                isLoading.value = false
            } catch(e) {
                error.value = e
            }
        }

        onBeforeMount(listProducts)

        return {
            table,
            products,
            error,
            search,
            listProducts,
            pages,
            activePage,
            ordering,
        }
    }
})

</script>