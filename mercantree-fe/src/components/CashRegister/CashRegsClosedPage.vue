<template>
    <div>
        <h1 class="text-2xl mb-8">Caixas fechados</h1>

        <div v-if="cashRegisters.length == 0">
            Nenhum caixa encontrado
        </div>

        <div v-else>
            <div
            class="collapse shadow mb-4"
            v-for="cr in cashRegisters"
            :key="cr.cashRegister.id"
            :class="{'collapse-open': cr.open}">
                <div
                class="collapse-title flex items-center justify-between min-h-0 py-2 bg-base-300 text-base-content">
                    <p class="text-lg flex-1">Caixa do dia {{ format_date(cr.cashRegister.created) }}</p>

                    <div
                    v-if="cr.open"
                    class="tabs tabs-boxed p-0 mr-4">
                        <a
                        @click="cr.tab = crTab.Informações"
                        class="tab tab-sm"
                        :class="{'tab-active': cr.tab == crTab.Informações}">Informações</a> 
                        <a
                        @click="goToTransactions(cr.cashRegister.id)"
                        class="tab tab-sm"
                        :class="{'tab-active': cr.tab == crTab.Transações}">Transações</a>
                    </div>

                    <label
                    @click="cr.open = !cr.open"
                    class="cursor-pointer">
                        <font-awesome-icon class="transition-all" :icon="cr.open ? 'remove' : 'add' " />
                    </label>
                </div>
                <div class="collapse-content bg-base-200 text-base-content">
                    <div v-if="cr.tab == crTab.Informações" class="flex flex-col sm:flex-row gap-4 py-4">
                        <div class="w-1/3">
                            <h3 class="text-lg font-semibold text-gray-500 mb-2">Movimentação:</h3>
                            <p class="text-md my-1">
                                Valor inicial: <b>{{ cr.cashRegister.initial_amount }}</b>
                            </p>
                            <p class="text-md my-1">
                                Valor final: <b>{{ cr.cashRegister.closed_amount }}</b>
                            </p>
                        </div>
                        <div class="w-2/3">
                            <h3 class="text-lg font-semibold text-gray-500 mb-2">Outras informações:</h3>
                            <p class="text-lg my-1">
                                Usuário: <b>{{ cr.cashRegister.user }}</b>
                            </p>
                            <p class="text-lg my-1">
                                Observações: <b>{{ cr.cashRegister.details }}</b>
                            </p>
                        </div>
                    </div>

                    <div v-else class="">
                        <h3 class="text-lg font-semibold text-gray-500 my-4">Transações:</h3>
                        <div
                        class="text-sm font-semibold"
                        v-if="cr.transactions?.count == 0">
                            Nenhuma transação encontrada
                        </div>
                        <table class="w-full" align="center" v-else>
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Data</th>
                                    <th>Valor</th>
                                    <th>Tipo</th>
                                    <th>Detalhes</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="tr in cr.transactions?.results">
                                    <td>{{ tr.id }}</td>
                                    <td>{{ transactionDate(tr.created ?? '') }}</td>
                                    <td>{{ get_price(tr.amount) }}</td>
                                    <td>{{ transactionType(tr.type) }}</td>
                                    <td>{{ tr.details ?? '---' }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { onMounted, ref } from 'vue'
import { APIListResponse } from '../../interfaces/common/response.interface'
import CashRegister from '../../interfaces/payments/cashregister.interface'
import Transaction from '../../interfaces/payments/transaction.interface'
import CashRegisterService from '../../services/cashRegisterService'
import format_date from '../../utils/format_date'
import get_price from '../../utils/get_price'

enum crTab {
    "Transações" = "TR",
    "Informações" = "IF"
}

interface crExpanded {
    cashRegister: CashRegister;
    transactions?: APIListResponse<Transaction>;
    open: boolean;
    tab: crTab;
}

const cashRegisters = ref<crExpanded[]>([])

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

const getCashRegisters = async () => {
    try {
        const response = await CashRegisterService().getClosed()
        response.results.map(cr => {
            cashRegisters.value.push({
                cashRegister: cr,
                open: false,
                tab: crTab.Informações,
            })
        })
    }
    catch(e) {
        return
    }
}

const goToTransactions = async (id?: number) => {
    try {
        if (!id) return
        const cr = cashRegisters.value.find(cr => cr.cashRegister.id === id)
        if (cr) {
            if (!cr.transactions) {
                const transactions = await CashRegisterService().transactions(id)
                cr.transactions = transactions
            }
            cr.tab = crTab.Transações
        }
    }
    catch(e) {
        return
    }
}

onMounted(async () => {
    await getCashRegisters()
})

</script>