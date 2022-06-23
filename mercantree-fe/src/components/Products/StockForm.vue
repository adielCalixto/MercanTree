<template>
    <form class="relative" @keydown="(e) => e.key == 'Enter' ? e.preventDefault() : e">
        <div class="flex gap-4">
            <label class="label">
                <span class="label-text">* Quantidade:</span>
            </label>

            <input
            v-model="state.quantity"
            type="text" 
            class="input max-w-md input-sm input-bordered">

            <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.quantity.$error">
                {{ v$.quantity.$errors[0].$message }}
            </div>
        </div>
        <div class="flex gap-4 w-full my-4">
            <label class="label">
                <span class="label-text">* Preço:</span>
            </label>

            <input
            v-model="state.price"
            type="text"
            class="input max-w-md input-sm input-bordered">

            <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.price.$error">
                {{ v$.price.$errors[0].$message }}
            </div>
        </div>
        <div class="flex gap-4 w-full my-4">
            <label class="label">
                <span class="label-text">* Preço de compra:</span>
            </label>

            <input
            v-model="state.purchase_price"
            type="text"
            class="input max-w-md input-sm input-bordered">

            <div class="badge badge-ghost rounded-none mt-1 gap-2" v-if="v$.purchase_price.$error">
                {{ v$.purchase_price.$errors[0].$message }}
            </div>
        </div>
        <div class="flex gap-4 w-full my-4">
            <label class="label">
                <span class="label-text">Data de validade:</span>
            </label>

            <input
            v-model="state.expires_at"
            type="date"
            class="input max-w-md input-sm input-bordered">
        </div>
        <div class="flex gap-4 w-full my-4">
            <label class="label">
                <span class="label-text">Fornecedor</span>
            </label>

            <v-select
            v-model="state.supplier"
            class="w-full max-w-xs z-20"
            label="name"
            :reduce="supplierReducer"
            :options="suppliers.results" />
        </div>
        <div class="flex gap-4 w-full my-4">
            <label class="label">
                <span class="label-text">Deletar quando o estoque chegar a 0</span>
            </label>

            <input
            v-model="state.delete_on_deplete"
            type="checkbox"
            class="input max-w-md input-sm input-bordered">
        </div>
        <div class="flex justify-end gap-4 bg-base-200 p-4">
            <slot name="extra-actions">

            </slot>

            <button
            class="btn btn-secondary btn-outline btn-sm"
            @click.prevent="$emit('cancel')">
                <slot name="cancel-message">
                    Cancelar
                </slot>
            </button>

            <button
            class="btn btn-primary btn-sm"
            @click.prevent="onSubmit()">
                Salvar
            </button>
        </div>
    </form>
</template>

<script setup lang="ts">

import useVuelidate from '@vuelidate/core'
import { required, numeric, minValue } from '@vuelidate/validators'
import { ref, computed } from 'vue'
import { APIListResponse } from '../../interfaces/common/response.interface'
import { Product } from '../../interfaces/products/product.interface'
import StockProduct from '../../interfaces/products/stock_product.interface'
import { Supplier } from '../../interfaces/suppliers/supplier.interface'
import SupplierService from '../../services/supplierService'


interface Props {
    state: StockProduct;
}

interface Emits {
    (e: 'cancel'): void;
    (e: 'submit', stockProduct: StockProduct): void;
}

const props = defineProps<Props>()
const emits = defineEmits<Emits>()

const state = ref<StockProduct>(props.state)

const rules = computed(() => ({
    quantity: { required, numeric, $autoDirty: true },
    price: { required, numeric, $autoDirty: true, minValue: minValue(state.value.purchase_price) },
    purchase_price: { required, numeric, $autoDirty: true },
}))

const v$ = useVuelidate(rules, state)

const isLoading = ref(false)
const suppliers = ref<APIListResponse<Supplier>>({ count: 0, results: [] })

const getSuppliers = async () => {
    try {
        isLoading.value = true
        const response = await SupplierService().list()
        suppliers.value = response
        isLoading.value = false
    }
    catch(e) {
        return
    }
}

const supplierReducer = (s: Supplier) => s.id

const onSubmit = async () => {
    await v$.value.$validate()
    if(v$.value.$error) return

    emits('submit', state.value)
}

await getSuppliers()

</script>