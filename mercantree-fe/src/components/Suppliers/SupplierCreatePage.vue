<template>
    <div>
        <h1 class="text-2xl mb-12">Adicionar fornecedor</h1>
        <h2 class="mb-4">Preencha todos os campos e escolha uma das ações.</h2>

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

            <div class="flex justify-end gap-4 bg-base-200 p-4">
                <button class="btn btn-secondary btn-outline btn-sm" @click.prevent="createProduct()">Salvar e adicionar outro</button>
                <button class="btn btn-primary btn-sm" @click.prevent="createProduct(true)">Salvar</button>
            </div>
        </form>
    </div>
</template>

<script lang="ts">

import useVuelidate from "@vuelidate/core"
import { email, maxLength, minLength, numeric, required } from "@vuelidate/validators"
import swal from "sweetalert"
import { computed, defineComponent, ref } from "vue"
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
        const router = useRouter()

        const createProduct = async (redirect: boolean = false) => {
            try {
                await v$.value.$validate()
                if (v$.value.$error) return

                isLoading.value = true
                const response = await SupplierService().create(supplier.value)
                isLoading.value = false

                await swal('Sucesso', 'Fornecedor criado', 'success')

                if(redirect) {
                    router.push('/suppliers')
                }
            } catch(e) {
                return
            }
        }

        return {
            supplier,
            isLoading,
            createProduct,
            v$,
        }
    },
})
</script>