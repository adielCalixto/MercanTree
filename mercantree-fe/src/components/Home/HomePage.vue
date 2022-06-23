<template>
  <div class="relative overflow-y-auto md:ml-48 container max-w-full mx-auto">
    <div class="stats w-full gap-8">
        <div class="stat bg-success text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="dollar" />
            </div>
            <div class="stat-title">Vendas</div>
            <div class="stat-value">{{ get_price(orderWeekPayments) }}</div>
            <div class="stat-desc">Quantitativo da semana</div>
        </div>
        <div class="stat bg-primary text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="book" />
            </div>
            <div class="stat-title">Produtos</div>
            <div class="stat-value">{{ productCount }}</div>
            <div class="stat-desc">Cadastrados</div>
        </div>
        <div class="stat bg-error text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="book" />
            </div>
            <div class="stat-title">Produtos</div>
            <div class="stat-value">0</div>
            <div class="stat-desc">Sem estoque</div>
        </div>        
        <div class="stat bg-primary text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="dollar" />
            </div>
            <div class="stat-title">Vendas</div>
            <div class="stat-value">{{ get_price(orderWeekPayments) }}</div>
            <div class="stat-desc">Quantitativo do mês</div>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 my-12 gap-8">
        <div class="bg-base-200">
            <div class="flex gap-2 items-center mb-4 p-4">
                <font-awesome-icon icon="chart-bar" class="text-3xl bg-info p-2 text-white" />
                <p class="text-xl">Estatisticas de vendas</p>
            </div>

            <div class="mx-4 md:mx-12">
                <Bar
                    v-if="!isLoading"
                    :height="250"
                    :chart-data="chartData"
                />
            </div>
        </div>

        <div class="bg-base-200">
            <div class="flex gap-2 items-center mb-4 p-4">
                <font-awesome-icon icon="warning" class="text-3xl bg-warning p-2 text-white" />
                <p class="text-xl">Alertas</p>
            </div>
            
            <div class="px-8 py-4">
                <div v-if="productsNextToExpiration.count == 0">
                    Nenhum alerta
                </div>

                <div v-else>
                    <h2 class="text-sm font-bold mb-4">Produtos perto da data de validade:</h2>

                    <div>
                        <div
                        v-for="p of productsNextToExpiration.results"
                        class="alert alert-warning shadow-md alert-sm">
                            <div>
                                <font-awesome-icon icon="warning" />
                                <p>{{ p.product.name }}</p>
                                <router-link :to="`/stock/?search=${p.product.name}`" class="ml-auto btn btn-sm btn-ghost btn-square">
                                    <font-awesome-icon icon="external-link" />
                                </router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <p class="text-center text-sm text-base-content mt-10 bg-base-200 shadow p-4">
      &copy; 2022 <a href="#" class="hover:underline" target="_blank">MultiTech</a>. All rights reserved.
    </p>
  </div>
</template>

<script setup lang="ts">

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import ProductService from '../../services/productService'
import OrderService from '../../services/orderService'
import { onBeforeMount, ref } from 'vue'
import get_price from '../../utils/get_price'
import { APIListResponse } from '../../interfaces/common/response.interface'
import { RouterLink } from 'vue-router'
import StockService from '../../services/stockService'
import StockProduct from '../../interfaces/products/stock_product.interface'
import { Product } from '../../interfaces/products/product.interface'

const isLoading = ref(false)

const orderWeekPayments = ref('0.00')
const orderMonthPayments = ref('0.00')
const productsPaidAmount = ref('0.00')
const productCount = ref(0)
const productsNextToExpiration = ref<APIListResponse<StockProduct & { product: Product }>>({ count: 0, results: [] })

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = ref()

const getProfit = (finalAmount: string, initialAmount: string) => {
    const x = parseFloat(finalAmount)
    const y = parseFloat(initialAmount)

    if(x < y)
        return 0.00

    return (x - y)
}

const getData = async () => {
    isLoading.value = true

    try {

        const response = await ProductService().list()
        productCount.value = response.count

        const response2 = await OrderService().paymentAmount('week')
        orderWeekPayments.value = response2.amount

        const response3 = await OrderService().paymentAmount()
        orderMonthPayments.value = response3.amount

        const response1 = await StockService().paidAmount()
        productsPaidAmount.value = response1.amount

        const response4 = await StockService().nextToExpire()
        productsNextToExpiration.value = response4

        chartData.value = {
            labels: ['Lucro (R$)', 'Valor estimado em produtos (R$)', 'Valor estimado em vendas (R$)'],
            datasets: [
                {
                    label: 'Total',
                    backgroundColor: ['#03FCBA', '#F15946', '#53B3CB'],
                    data: [
                        getProfit(orderMonthPayments.value, productsPaidAmount.value),
                        parseFloat(productsPaidAmount.value),
                        parseFloat(orderMonthPayments.value),
                    ]
                }
            ]
        }
    }
    catch(e) {
        return
    }

    isLoading.value = false
}

onBeforeMount(async () => {
    await getData()
})

</script>

<style>
</style>