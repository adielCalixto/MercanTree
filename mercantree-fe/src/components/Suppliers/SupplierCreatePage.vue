<template>
    <div>
        <h1 class="text-2xl mb-12">Adicionar fornecedor</h1>
        <h2 class="mb-4">Preencha todos os campos e escolha uma das ações.</h2>

        <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Nome:</span>
                </label>
                <input v-model="supplier.name" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Responsável:</span>
                </label>
                <input v-model="supplier.responsable" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Email:</span>
                </label>
                <input v-model="supplier.email" type="email" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Telefone:</span>
                </label>
                <input v-model="supplier.phone" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Cidade:</span>
                </label>
                <input v-model="supplier.city" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Endereço:</span>
                </label>
                <input v-model="supplier.address" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">CNPJ:</span>
                </label>
                <input v-model="supplier.cnpj" type="text" class="input max-w-md input-sm input-bordered">
            </div>

            <div class="flex justify-end gap-4 bg-base-200 p-4">
                <button class="btn btn-secondary btn-outline btn-sm" @click.prevent="createProduct()">Salvar e adicionar outro</button>
                <button class="btn btn-primary btn-sm" @click.prevent="createProduct(true)">Salvar</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">

import swal from "sweetalert"
import { defineComponent, ref } from "vue"
import { useRouter } from "vue-router"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"
import SupplierService from "../../services/supplierService"

export default defineComponent({
    setup() {
        const supplier = ref<Supplier>({
            name: '',
            email: '',
            phone: '',
            address: '',
            city: '',
            cnpj: '',
            responsable: '',
        })

        const error = ref()
        const isLoading = ref(false)
        const router = useRouter()

        const createProduct = async (redirect: boolean = false) => {
            try {
                isLoading.value = true
                const response = await SupplierService().create(supplier.value)
                isLoading.value = false

                await swal('Sucesso', 'Fornecedor criado', 'success')

                if(redirect) {
                    router.push('/suppliers')
                }
            } catch(e) {
                error.value = e
            }
        }

        return {
            supplier,
            isLoading,
            error,
            createProduct,
        }
    },
})
</script>