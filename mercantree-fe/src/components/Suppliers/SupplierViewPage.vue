<template>
    <div>
        <h1 class="text-2xl mb-12">Alterar fornecedor</h1>
        <h2 class="font-bold text-xl mb-8">{{ supplier.name }}</h2>

        <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">* Nome:</span>
                </label>
                <input
                v-model="supplier.name"
                type="text"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.name.$error">
                    {{ v$.name.$errors[0].$message }}
                </div>
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">* Responsável:</span>
                </label>
                <input
                v-model="supplier.responsable"
                type="text"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.responsable.$error">
                    {{ v$.responsable.$errors[0].$message }}
                </div>
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Email:</span>
                </label>
                <input
                v-model="supplier.email"
                type="email"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.email.$error">
                    {{ v$.email.$errors[0].$message }}
                </div>
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">Telefone:</span>
                </label>
                <input
                v-model="supplier.phone"
                type="text"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.phone.$error">
                    {{ v$.phone.$errors[0].$message }}
                </div>
            </div>

            <div class="flex gap-4 my-4">
                <label class="label">
                    <span class="label-text">* Cidade:</span>
                </label>
                <input
                v-model="supplier.city"
                type="text"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.city.$error">
                    {{ v$.city.$errors[0].$message }}
                </div>
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
                <input
                v-model="supplier.cnpj"
                type="text"
                class="input max-w-md input-sm input-bordered">
                <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.cnpj.$error">
                    {{ v$.cnpj.$errors[0].$message }}
                </div>
            </div>

            <div class="flex justify-end gap-4 my-4 bg-base-200 p-4">
                <button class="btn btn-error btn-outline btn-sm" @click.prevent="deleteProduct()">Deletar</button>
                <button class="btn btn-secondary btn-sm" @click.prevent="updateProduct()">Salvar</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">

import swal from "sweetalert"
import { computed, defineComponent, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { Supplier } from "../../interfaces/suppliers/supplier.interface"
import SupplierService from "../../services/supplierService"
import useVuelidate from "@vuelidate/core"
import { email, maxLength, minLength, numeric, required } from "@vuelidate/validators"
import errorService from "../../services/errorService"

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

        const rules = computed(() => ({
            name: { required, $autoDirty: true },
            responsable: { required, $autoDirty: true },
            city: { required, $autoDirty: true },
            cnpj: { numeric, maxLength: maxLength(14), minLength: minLength(14), $autoDirty: true },
            email: { email, $autoDirty: true },
            phone: { numeric, $autoDirty: true },
        }))

        const v$ = useVuelidate(rules, supplier)

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
                await v$.value.$validate()
                if (v$.value.$error) return

                const response = await SupplierService().update(id, supplier.value)
                supplier.value = response

                await swal('Sucesso', 'Fornecedor editado', 'success')

                router.push('/suppliers')
            } catch(e) {
                return
            }
        }

        const deleteProduct = async () => {
            try {
                await errorService().onWarn()

                const response = await SupplierService().destroy(id)

                await swal('Sucesso', 'Fornecedor deletado', 'success')

                router.push('/suppliers')
            } catch(e) {
                return
            }
        }

        return {
            supplier,
            isLoading,
            updateProduct,
            deleteProduct,
            v$,
        }
    },
})
</script>