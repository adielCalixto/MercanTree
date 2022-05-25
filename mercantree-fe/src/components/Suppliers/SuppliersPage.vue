<template>
    <div>
        <h1 class="text-xl mb-12">Lista de Fornecedores</h1>

        <div class="my-4 flex justify-between">
            <router-link
            :to="$route.fullPath + '/create' "
            class="btn btn-success btn-sm">
                Adicionar
            </router-link>

            <select v-model="ordering"
            @change="listSuppliers()"
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

                    <button @click="activePage = 1, listSuppliers()" class="btn btn-square btn-sm">
                        <font-awesome-icon icon="search" />
                    </button>
                </div>
            </div>
        </div>

        <div v-if="suppliers.count == 0">
            Nenhum fornecedor encontrado
        </div>

        <mt-table :table="table" v-else >
            <tr v-for="supplier in suppliers.results">
                <th> {{ supplier.id }}</th>
                <th> {{ supplier.name }} </th>
                <th> {{ supplier.responsable }} </th>
                <th> {{ supplier.email }} </th>
                <th> {{ supplier.phone }} </th>
                <th> {{ supplier.city }} </th>
                <th> {{ supplier.address }} </th>
                <th> {{ supplier.cnpj }} </th>
                <th>
                    <router-link :to="`/suppliers/supplier/${supplier.id}`" class="btn btn-primary btn-sm">View</router-link>
                </th>
            </tr>
        </mt-table>

        <div class="w-full flex justify-center mt-4">
            <div class="btn-group">
                <button class="btn btn-sm"
                v-for="page in pages"
                :class="{'btn-active': page == activePage}"
                @click="activePage = page, listSuppliers()">{{ page }}</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">

import { defineComponent, ref, computed, onBeforeMount } from 'vue'
import MtTable from "../MtTable.vue"
import { APIListResponse } from '../../interfaces/common/response.interface'
import { RouterLink } from 'vue-router'
import { Supplier } from '../../interfaces/suppliers/supplier.interface'
import { PAGE_SIZE } from '../../consts'
import SupplierService from '../../services/supplierService'

export default defineComponent({
    components: {
        MtTable,
        RouterLink,
    },
    async setup() {
        const table = {
            name: 'Fornecedores',
            fields: [
                '',
                'Nome',
                'Responsável',
                'Email',
                'Telefone',
                'Cidade',
                'Endereço',
                'CNPJ',
                ''
            ],
        }

        const search = ref('')
        const ordering = ref('')
        const error = ref()
        const suppliers = ref<APIListResponse<Supplier>>({count: 0, results: []})
        const isLoading = ref(false)
        const pages = computed(() => Math.floor((suppliers.value.count + PAGE_SIZE - 1) / PAGE_SIZE))
        const activePage = ref(1)

        const listSuppliers = async () => {
            try {
                isLoading.value = true
                const response = await SupplierService().list(activePage.value, search.value, ordering.value)
                suppliers.value = response
                isLoading.value = false
            } catch(e) {
                error.value = e
            }
        }

        onBeforeMount(listSuppliers)

        return {
            table,
            suppliers,
            error,
            search,
            listSuppliers,
            pages,
            activePage,
            ordering,
        }
    }
})

</script>