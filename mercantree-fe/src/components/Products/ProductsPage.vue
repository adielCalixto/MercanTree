<template>
    <div>
        <h1 class="text-xl mb-12">Lista de Produtos</h1>

        <div class="my-4 flex justify-between">
            <router-link :to="'/stock/create'" class="btn btn-success btn-sm">Adicionar</router-link>
            <select v-model="ordering"
            @change="listProducts()"
            class="select select-sm select-bordered ml-auto mr-4">
                <option value="" disabled selected>Ordenar</option>
                <option value="name">Nome-ASC</option>
                <option value="-name">Nome-DESC</option>
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
            <tr v-for="p in products.results">
                <th> {{ p.id }}</th>
                <th> {{ p.name }} </th>
                <th> {{ p.description }} </th>
                <th> {{ p.barcode }} </th>
                <th> {{ p.category }} </th>
                <th>
                    <router-link
                    :to="`/stock/products/product/${p.id}`"
                    class="btn btn-sm btn-primary btn-outline btn-square">
                        <font-awesome-icon icon="edit" />
                    </router-link>
                </th>
                <th>
                    <button
                    @click="selectedProductId = p.id, stockFormOpen = true"
                    class="btn btn-sm btn-success">
                        <font-awesome-icon icon="add" />
                        Estoque
                    </button>
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

        <div
        v-if="stockFormOpen && selectedProductId"
        class="modal modal-open">
            <div class="modal-box">
                <h2 class="text-xl">Adicionar estoque ao produto</h2>
                <p class="text-md mb-4 font-bold">{{ products.results.find(p => p.id == selectedProductId)?.name }}</p>

                <stock-form
                @submit="state => createStock(state)"
                @cancel="closeModal()"
                :state="{ product: selectedProductId, quantity: '', price: '', purchase_price: '', delete_on_deplete: false }">
                    
                </stock-form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, computed, onBeforeMount } from 'vue'
import MtTable from "../MtTable.vue"
import { APIListResponse } from '../../interfaces/common/response.interface'
import { RouterLink, useRoute } from 'vue-router'
import { PAGE_SIZE } from '../../consts'
import { Product } from '../../interfaces/products/product.interface'
import ProductService from '../../services/productService'
import StockForm from './StockForm.vue'
import StockProduct from '../../interfaces/products/stock_product.interface'
import StockService from '../../services/stockService'
import swal from 'sweetalert'

const table = {
    name: 'Produtos',
    fields: [
        '',
        'Nome',
        'Descrição',
        'Código de barras',
        'Categoria',
        '',
        '',
    ],
}

const route = useRoute()
const search = ref(route.query.search?.toString())
const ordering = ref('')
const products = ref<APIListResponse<Product>>({ count: 0, results: [] })
const isLoading = ref(false)
const pages = computed(() => Math.floor((products.value.count + PAGE_SIZE - 1) / PAGE_SIZE))
const activePage = ref(1)

const stockFormOpen = ref(false)
const selectedProductId = ref<number | undefined>()

const listProducts = async () => {
    try {
        isLoading.value = true
        const response = await ProductService().list(activePage.value, search.value, ordering.value)
        products.value = response
        isLoading.value = false
    } catch(e) {
        return
    }
}

const closeModal = () => {
    stockFormOpen.value = false
    selectedProductId.value = undefined
}

const createStock = async (state: StockProduct) => {
    try {
        await StockService().create(state)
        closeModal()
        swal('Sucesso', 'Estoque adicionado ao produto', 'success')
    }
    catch(e) {
        return
    }
}

onBeforeMount(listProducts)

</script>