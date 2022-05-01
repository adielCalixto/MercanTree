<template>
    <div>
        <h1 class="text-xl mb-12">Lista de Produtos</h1>
        <div class="my-4 flex justify-between">
            <router-link :to="$route.fullPath + '/create'" class="btn btn-success btn-sm">Adicionar</router-link>
            <div class="form-control">
                <div class="input-group">
                    <input type="text" placeholder="Search…" class="input input-sm input-bordered">
                    <button class="btn btn-square btn-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </button>
                </div>
            </div>
        </div>
        <mt-table :table="table">
            <tr v-for="item in data">
                <th v-for="value in item">{{ value }}</th>
            </tr>
        </mt-table>
    </div>
</template>

<script lang="ts">

import { defineComponent } from "vue"
import MtTable from "../MtTable.vue"

export default defineComponent({
    name: 'MtPage',
    components: {
        MtTable,
    },
    data() {
        return {
            table: {
                name: 'Produtos',
                fields: ['Nome', 'Categoria', 'Preço', 'Validade', ''],
            },
            data: [{
                name: 'sample'
            }]
        }
    },
})
</script>