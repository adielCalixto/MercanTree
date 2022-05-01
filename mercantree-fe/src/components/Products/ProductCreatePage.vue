<template>
    <div>
        <h1 class="text-2xl mb-12">Adicionar produto</h1>
        <h2>Preencha todos os campos e escolha uma das ações.</h2>

        <form class="relative">
            <div class="form-control">
                <label class="label">
                    <span class="label-text">Nome</span>
                </label>
                <input type="text" placeholder="Nome" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Descrição</span>
                </label>
                <input type="text" placeholder="Descrição" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Categoria</span>
                </label>
                <select class="select select-sm select-bordered w-full max-w-xs">
                    <option disabled selected>Categoria</option>
                    <option>Grãos</option>
                    <option>Limpeza</option>
                    <option>Outros</option>
                </select>
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Preço</span>
                </label>
                <input type="number" placeholder="Preço" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Validade</span>
                </label>
                <input type="date" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Código de barras</span>
                </label>
                <input type="text" placeholder="Descrição" class="input max-w-md input-sm input-bordered">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Fornecedor</span>
                </label>
                <select class="select select-sm select-bordered w-full max-w-xs">
                    <option disabled selected>Fornecedor</option>
                    <option>Exemplo</option>
                </select>
            </div>
            <div class="flex justify-end gap-4 bg-gray-100 p-4">
                <button class="btn btn-secondary btn-sm">Salvar e adicionar outro</button>
                <button class="btn btn-primary btn-sm">Salvar</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">

import { defineComponent } from "vue"

export default defineComponent({
    name: 'MtPage',
    data() {
        return {
            data: [{
                name: 'sample'
            }]
        }
    },
})
</script>