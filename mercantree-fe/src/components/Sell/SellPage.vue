<template>
  <div>
        <h1 class="text-xl mb-12">Lista de Vendas</h1>

        <div class="my-4 flex justify-between">
            <router-link to="/sell/create" class="btn btn-success btn-sm">Adicionar</router-link>

            <select v-model="ordering"
            @change="listOrders()"
            class="select select-sm select-bordered ml-auto mr-4">
                <option value="" disabled selected>Ordenar</option>
                <option value="created">Data-ASC</option>
                <option value="-created">Data-DESC</option>
            </select>
            <div class="form-control">
                <div class="input-group">
                    <input
                    type="text"
                    placeholder="Search…"
                    class="input input-sm input-bordered"
                    v-model="search" >

                    <button @click="activePage = 1, listOrders()" class="btn btn-square btn-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </button>
                </div>
            </div>
        </div>

        <div v-if="orders.count == 0">
            Nenhuma venda encontrado
        </div>

        <mt-table :table="table" v-else >
            <tr v-for="order in orders.results">
                <th></th>
                <th>{{ order.user }}</th>
                <th>{{ order.payment }}</th>
                <th>
                    <router-link :to="`/products/product/${order.id}`" class="btn btn-primary btn-sm">View</router-link>
                </th>
            </tr>
        </mt-table>

        <div class="w-full flex justify-center mt-4">
            <div class="btn-group">
                <button class="btn btn-sm"
                v-for="page in pages"
                :class="{'btn-active': page == activePage}"
                @click="activePage = page, listOrders()">{{ page }}</button>
            </div>
        </div>

        <div class="modal modal-open" v-if="creationModal">
            <div class="modal-box max-w-2xl">
                <h3 class="font-bold text-lg">Nova venda</h3>
            </div>
        </div>
    </div>
</template>

<script lang="ts">

import MtTable from '../MtTable.vue'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { RouterLink } from 'vue-router'
import Order from '../../interfaces/orders/order.interface'
import OrderService from '../../services/modules/order.module'
import { APIListResponse } from '../../interfaces/common/response.interface'
import { PAGE_SIZE } from '../../consts'
import { computed } from '@vue/reactivity'

export default defineComponent({
    components: {
        MtTable,
    },
    setup() {
        const error = ref()
        const table = {
            name: 'Vendas',
            fields: [
                '',
                'Cadastrante',
                'Pagamento',
                '',
            ]
        }
        const isLoading = ref(false)
        const creationModal = ref(false)
        const search = ref('')
        const activePage = ref(1)
        const ordering = ref('')
        const orders = ref<APIListResponse<Order>>({count: 0, results: []})
        const pages = computed(() => Math.floor((orders.value.count + PAGE_SIZE - 1) / PAGE_SIZE))

        const listOrders = async () => {
            try {
                isLoading.value = true
                const response = await OrderService.list(activePage.value, search.value, ordering.value)
                isLoading.value = false

                orders.value = response
            }
            catch(e) {
                error.value = e
            }
        }

        onBeforeMount(listOrders)

        return {
            error,
            isLoading,
            orders,
            search,
            ordering,
            listOrders,
            pages,
            activePage,
            table,
            creationModal,
        }
    },
})

</script>

<style>
</style>