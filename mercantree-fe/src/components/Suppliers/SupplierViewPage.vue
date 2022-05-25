<template>
    <div>
        <h1 class="text-2xl mb-12">Alterar fornecedor</h1>
        <h2 class="font-bold text-xl mb-8">{{ supplier.name }}</h2>

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
            <div class="flex justify-end gap-4 my-4 bg-gray-100 p-4">
                <button class="btn btn-error btn-outline btn-sm" @click.prevent="deleteProduct()">Deletar</button>
                <button class="btn btn-secondary btn-sm" @click.prevent="updateProduct()">Salvar</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">

import swal from "sweetalert"
import { defineComponent, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"
import SupplierService from "../../services/supplierService"

export default defineComponent({
    name: 'MtPage',
    async setup() {
        const route = useRoute()
        const router = useRouter()
        const id = parseInt(route.params.id.toString())
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

        try {
            isLoading.value = true
            const response = await SupplierService().retrieve(id)
            supplier.value = response
            isLoading.value = false
        } catch(e) {
            router.push('/suppliers')
        }

        const updateProduct = async () => {
            try {
                const response = await SupplierService().update(id, supplier.value)
                supplier.value = response

                await swal('Sucesso', 'Fornecedor editado', 'success')

                router.push('/suppliers')
            } catch(e) {
                error.value = e
            }
        }

        const deleteProduct = async () => {
            try {
                const response = await SupplierService().destroy(id)

                await swal('Sucesso', 'Fornecedor deletado', 'success')

                router.push('/suppliers')
            } catch(e) {
                error.value = e
            }
        }

        return {
            supplier,
            error,
            isLoading,
            updateProduct,
            deleteProduct,
        }
    },
})
</script>