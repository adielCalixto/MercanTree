<template>
    <div>
        <h1 class="text-xl mb-12">Estoque</h1>

        <div class="my-4 flex justify-between">
            <router-link to="/stock/products" class="btn btn-sm btn-outline">Produtos</router-link>
            <select v-model="ordering"
            @change="listProducts()"
            class="select select-sm select-bordered ml-auto mr-4">
                <option value="" disabled selected>Ordenar</option>
                <option value="product__name">Nome-ASC</option>
                <option value="-product__name">Nome-DESC</option>
                <option value="price">Preço-ASC</option>
                <option value="-price">Preço-DESC</option>
                <option value="expires_at">Data de validade-ASC</option>
                <option value="-expires_at">Data de validade-DESC</option>
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
            Nenhum produto em estoque
        </div>

        <mt-table :table="table" v-else >
            <tr v-for="p in products.results">
                <th> {{ p.id }}</th>
                <th> {{ p.product.name }} </th>
                <th> {{ p.product.description }} </th>
                <th> {{ format_date(p.expires_at) }} </th>
                <th> {{ get_price(p.price) }} </th>
                <th> {{ p.product.barcode }} </th>
                <th> {{ p.quantity }} </th>
                <th> {{ p.product.category }} </th>
                <th>
                    <router-link v-if="p.supplier" :to="`/suppliers/supplier/${p.supplier}`" class="btn btn-rounded btn-sm">
                        <font-awesome-icon icon="external-link" />
                    </router-link>
                </th>
                <th>
                    <button
                    @click="stockFormOpen = true,
                    selectedStock= { ...p, product: p.product.id ? p.product.id : 0}"
                    class="btn btn-sm btn-primary btn-outline btn-square">
                        <font-awesome-icon icon="edit" />
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
        v-if="stockFormOpen && selectedStock"
        class="modal modal-open">
            <div class="modal-box">
                <h2 class="text-xl">Alterar estoque do produto</h2>
                <p class="text-md mb-4 font-bold">
                    {{ products.results.find(p => p.id === selectedStock?.id)?.product.name }}
                </p>

                <stock-form
                :state="selectedStock"
                @cancel="closeModal()"
                @submit="state => updateStock(state)">

                    <template #extra-actions>
                        <button
                        @click.prevent="deleteStock()"
                        class="btn btn-sm btn-outline btn-error">
                            Deletar
                        </button>
                    </template>

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
import format_date from "../../utils/format_date"
import get_price from '../../utils/get_price'
import StockProductService from '../../services/stockService'
import StockProduct from '../../interfaces/products/stock_product.interface'
import { Product } from '../../interfaces/products/product.interface'
import swal from 'sweetalert'
import StockForm from './StockForm.vue'
import errorService from '../../services/errorService'

const table = {
    name: 'Produtos',
    fields: [
        '',
        'Nome',
        'Descrição',
        'Validade',
        'Preço',
        'Código de barras',
        'Quantidade',
        'Categoria',
        'Fornecedor',
        '',
    ],
}

const route = useRoute()
const search = ref(route.query.search?.toString())
const ordering = ref('')
const products = ref<APIListResponse<StockProduct & { product: Product }>>({count: 0, results: []})
const isLoading = ref(false)
const pages = computed(() => Math.floor((products.value.count + PAGE_SIZE - 1) / PAGE_SIZE))
const activePage = ref(1)

const selectedStock = ref<StockProduct | undefined>()
const stockFormOpen = ref(false)

const closeModal = () => {
    selectedStock.value = undefined
    stockFormOpen.value = false
}

const updateStock = async (state: StockProduct) => {
    if(!selectedStock.value) return
    if(!selectedStock.value.id) return

    try {
        await StockProductService().update(selectedStock.value.id, state)
        await listProducts()
        closeModal()
        swal('Sucesso', 'Estoque alterado', 'success')
    }
    catch(e) {
        return
    }
}

const deleteStock = async () => {
    if (!selectedStock.value) return
    if (!selectedStock.value.id) return

    try {
        const confirm = await errorService().onWarn()
        if(confirm) {
            await StockProductService().destroy(selectedStock.value.id)
            await listProducts()
            closeModal()
            swal('Sucesso', 'Estoque deletado', 'success')
        }
    }
    catch(e) {
        return
    }
}

const listProducts = async () => {
    try {
        isLoading.value = true
        const response = await StockProductService().listExpanded(activePage.value, search.value, ordering.value)
        products.value = response
        isLoading.value = false
    } catch(e) {
        return
    }
}

onBeforeMount(listProducts)
</script>