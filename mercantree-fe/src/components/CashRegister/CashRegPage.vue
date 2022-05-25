<template>
    <div>
        <div class="grid grid-cols-1 md:grid-cols-3 w-full my-8 gap-4">
            <div
            @click="async () => { await store.getStats(), openModal = modalList.CLOSE_CASH_REGISTER }"
            class="btn btn-ghost shadow btn-md">
                Fechar caixa
                <font-awesome-icon
                class="text-lg ml-2"
                icon="remove" />
            </div>

            <div
            @click="openModal = modalList.ADD_CASH"
            class="btn btn-ghost shadow btn-md">
                Adicionar dinheiro
                <font-awesome-icon
                class="text-lg ml-2"
                icon="plus" />
            </div>

            <div
            @click="openModal = modalList.REMOVE_CASH"
            class="btn btn-ghost shadow btn-md">
                Retirar dinheiro
                <font-awesome-icon
                class="text-lg ml-2"
                icon="dollar" />
            </div>

        </div>

        <div class="w-full">
            <h1 class="text-xl mb-12">Transações do caixa atual</h1>

            <div class="my-4 flex justify-between">
                <select @change=""
                class="select select-sm select-bordered ml-auto mr-4">
                    <option value="" disabled selected>Ordenar</option>
                    <option value="price">Preço-ASC</option>
                    <option value="-price">Preço-DESC</option>
                    <option value="created">Data-ASC</option>
                    <option value="-created">Data-DESC</option>
                </select>
            </div>

            <div v-if="store.transactions.count == 0">
                Nenhuma transação encontrada
            </div>

            <mt-table :table="table" v-else >
                <tr v-for="t in store.transactions.results">
                    <th>{{ t.id }}</th>
                    <th>{{ transactionDate(t.created ?? '') }}</th>
                    <th>{{ t.amount }}</th>
                    <th>{{ transactionType(t.type) }}</th>
                    <th>
                        <router-link
                        class="btn btn-sm"
                        to="/">
                            Detalhes
                            <font-awesome-icon class="ml-2" icon="external-link" />
                        </router-link>
                    </th>
                </tr>
            </mt-table>
        </div>

        <div>
            <div class="modal modal-open"
            v-if="openModal == modalList.ADD_CASH">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Adicionar dinheiro ao caixa</h3>

                    <div class="modal-action">
                        <a @click="depositCash()" class="btn btn-primary btn-sm">Salvar</a>
                        <a @click="openModal = modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>

                    <div class="divider"></div>

                    <div class="flex gap-4 justify-end">
                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            v-model="addInput">
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal modal-open"
            v-if="openModal == modalList.REMOVE_CASH">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Retirar dinheiro do caixa</h3>

                    <div class="modal-action">
                        <a @click="removeCash()" class="btn btn-primary btn-sm">Salvar</a>
                        <a @click="openModal=modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>

                    <div class="divider"></div>

                    <div class="flex gap-4 justify-end">
                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            v-model="removeInput">
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal modal-open"
            v-if="openModal == modalList.CLOSE_CASH_REGISTER">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Fechar caixa</h3>
                    <p class="text-md">Tem certeza que deseja fechar o caixa?</p>

                    <div class="my-4 flex gap-4">
                        <div>
                            <p class="text text-base-content text-lg">Valor inicial:</p>
                            <p class="text text-base-content font-bold text-xl">{{ store.stats?.initial_amount }}</p>
                        </div>

                        <div class="divider divider-horizontal"></div>

                        <div>
                            <p class="text text-base-content text-lg">Valor estimado final:</p>
                            <p class="text text-base-content font-bold text-xl">{{ store.stats?.final_amount }}</p>
                        </div>
                    </div>

                    <div class="flex justify-between gap-4">
                        <div class="form-control flex-1">
                            <label class="label">Observações:</label>
                            <textarea
                            class="textarea textarea-primary resize-none w-full"
                            rows="1"
                            v-model="closingForm.details"></textarea>
                        </div>
                        <div class="form-control">
                            <label class="label">Valor em caixa:</label>
                            <input
                            class="input input-primary input-sm"
                            type="number"
                            v-model="closingForm.closed_amount">
                        </div>
                    </div>

                    <div class="modal-action">
                        <a @click="close()"
                        class="btn btn-warning btn-sm">Confirmar</a>

                        <a @click="openModal=modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="modal" :class="{'modal-open': !store.hasCashRegister}">
            <div class="modal-box max-w-xl">
                <div class="flex gap-2 items-center">
                    <font-awesome-icon class="text-warning" icon="warning" />
                    <h3 class="font-bold text-lg">Caixa não aberto</h3>
                </div>

                <p class="text-md">Deseja abrir o caixa?</p>

                <div class="modal-action justify-between mt-12">
                    <a
                    class="btn btn-sm btn-ghost"
                    @click="$router.go(-1)">
                        <font-awesome-icon class="mr-2" icon="arrow-left" />
                        Voltar
                    </a>

                    <router-link
                    class="btn btn-sm btn-ghost"
                    to="/cashregister/open">
                        Prosseguir
                        <font-awesome-icon class="ml-2" icon="external-link" />
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { RouterLink, useRouter } from 'vue-router'
    import CashRegisterService from '../../services/cashRegisterService';
    import { useStore } from '../../stores/cashregister'
    import MtTable from '../MtTable.vue'

    const store = useStore()
    const router = useRouter()
    const table = {
        name: 'Transações',
        fields: [
            '',
            'Data',
            'Valor',
            'Tipo',
            ''
        ]
    }
    const addInput = ref(0)
    const removeInput = ref(0)
    const closingForm = ref({
        closed_amount: 0,
        details: '',
    })

    const transactionType = (type: string) => {
        switch(type) {
            case 'CI':
                return "Depósito";

            case 'CB':
                return "Saque"

            default:
                return "Tipo inválido"
        }
    }

    const transactionDate = (date: string) => {
        return new Date(date).toLocaleDateString('pt-BR', { month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric' })
    }

    const openModal = ref('')
    const modalList = ref({
        CLOSE_CASH_REGISTER: 'CCR',
        ADD_CASH: 'ACH',
        REMOVE_CASH: 'RCH',
        NONE: '',
    })


    const depositCash = async () => {
        try {
            if (!store.cashRegister)
                return

            if (!store.cashRegister.id)
                return

            const response = await CashRegisterService().deposit(store.cashRegister.id, addInput.value)
            openModal.value = modalList.value.NONE
            store.getTransactions()
        }
        catch(e) {
            console.error(e)
        }
    }

    const removeCash = async () => {
        try {
            if (!store.cashRegister)
                return

            if (!store.cashRegister.id)
                return

            const response = await CashRegisterService().withdraw(store.cashRegister.id, removeInput.value)
            openModal.value = modalList.value.NONE
            store.getTransactions()
        }
        catch(e) {
            console.error(e)
        }
    }

    const close = async () => {
        try {
            await store.close(closingForm.value.closed_amount,
            closingForm.value.details)

            openModal.value = modalList.value.NONE
            router.push('/')
        }
        catch(e) {
            console.error(e)
        }
    }

    onMounted(async () => {
        try {
            await store.getCashRegister()
            await store.getTransactions()
        }
        catch(e) {
            console.error(e)
        }
    })

</script>

<style>

</style>