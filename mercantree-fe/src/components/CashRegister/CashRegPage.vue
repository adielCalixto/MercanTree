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
                    <th>{{ t.details || '---' }}</th>
                    <th>{{ get_price(t.amount) }}</th>
                    <th>{{ transactionType(t.type) }}</th>
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
                        <div class="form-control flex-1">
                            <label class="label">Detalhes</label>
                            <textarea
                            class="textarea resize-none"
                            placeholder="..."
                            rows="1"
                            v-model="state.addAmount.details" />
                        </div>

                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            v-model="state.addAmount.amount">
                            <div v-if="v$.addAmount.$error">
                                {{ v$.addAmount.amount.$errors[0].$message }}
                            </div>
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
                        <div class="form-control flex-1">
                            <label class="label">Detalhes</label>
                            <textarea
                            class="textarea resize-none"
                            placeholder="..."
                            rows="1"
                            v-model="state.removeAmount.details" />
                        </div>

                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            v-model="state.removeAmount.amount">
                            <div v-if="v$.removeAmount.$error">
                                {{ v$.removeAmount.amount.$errors[0].$message }}
                            </div>
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
                            <p class="text text-base-content font-bold text-xl">{{ get_price(store.stats?.initial_amount ?? '') }}</p>
                        </div>

                        <div class="divider divider-horizontal"></div>

                        <div>
                            <p class="text text-base-content text-lg">Valor estimado final:</p>
                            <p class="text text-base-content font-bold text-xl">{{ get_price(store.stats?.final_amount ?? '') }}</p>
                        </div>
                    </div>

                    <div class="flex justify-between gap-4">
                        <div class="form-control flex-1">
                            <label class="label">Observações:</label>
                            <textarea
                            class="textarea textarea-primary resize-none w-full"
                            rows="1"
                            v-model="state.close.details"></textarea>
                        </div>
                        <div class="form-control">
                            <label class="label">Valor em caixa:</label>
                            <input
                            class="input input-primary input-sm"
                            type="number"
                            min="0"
                            v-model="state.close.amount">
                            <div v-if="v$.close.$error">
                                {{ v$.close.amount.$errors[0].$message }}
                            </div>
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
    import useVuelidate from '@vuelidate/core';
    import { minValue, numeric, required } from '@vuelidate/validators';
    import { ref, onMounted, reactive, computed } from 'vue'
    import { RouterLink, useRouter } from 'vue-router'
    import CashRegisterService from '../../services/cashRegisterService';
    import errorService from '../../services/errorService';
    import { useStore } from '../../stores/cashregister'
    import MtTable from '../MtTable.vue'
    import get_price from '../../utils/get_price'

    const store = useStore()
    const router = useRouter()
    const table = {
        name: 'Transações',
        fields: [
            '',
            'Data',
            'Detalhes',
            'Valor',
            'Tipo',
        ]
    }

    const state = reactive({
        addAmount: {
            amount: 0,
            details: '',
        },
        removeAmount: {
            amount: 0,
            details: '',
        },
        close: {
            amount: 0,
            details: '',
        },
    })

    const rules = computed(() => ({
        addAmount: {
            amount: { required, numeric, minValue: minValue(1), $autoDirty: true },
        },
        removeAmount: {
            amount: { required, numeric, minValue: minValue(1), $autoDirty: true },
        },
        close: {
            amount: { required, numeric, minValue: minValue(0), $autoDirty: true },
        },
    }))

    const v$ = useVuelidate(rules, state)

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
            if (!store.cashRegister) return

            if (!store.cashRegister.id) return

            await v$.value.$validate()
            if (v$.value.addAmount.$error) return

            const response = await CashRegisterService().deposit(store.cashRegister.id, state.addAmount.amount, state.addAmount.details)
            openModal.value = modalList.value.NONE
            store.getTransactions()
        }
        catch(e) {
            return
        }
    }

    const removeCash = async () => {
        try {
            if (!store.cashRegister) return

            if (!store.cashRegister.id) return

            await v$.value.$validate()
            if (v$.value.removeAmount.$error) return

            const response = await CashRegisterService().withdraw(store.cashRegister.id, state.removeAmount.amount, state.removeAmount.details)
            openModal.value = modalList.value.NONE
            store.getTransactions()
        }
        catch(e) {
            return
        }
    }

    const close = async () => {
        try {
            await v$.value.$validate()
            if (v$.value.close.$error) return

            await errorService().onWarn()

            await store.close(state.close.amount,
            state.close.details)

            openModal.value = modalList.value.NONE
            router.push('/cashregister/closed')
        }
        catch(e) {
            return
        }
    }

    onMounted(async () => {
        try {
            await store.getCashRegister()
            await store.getTransactions()
        }
        catch(e) {
            return
        }
    })

</script>

<style>

</style>