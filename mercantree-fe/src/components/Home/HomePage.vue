<template>
  <div class="relative overflow-y-auto md:ml-48 container max-w-full mx-auto">
    <div class="stats w-full gap-8">
        <div class="stat bg-success text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="dollar" />
            </div>
            <div class="stat-title">Vendas</div>
            <div class="stat-value">31K</div>
            <div class="stat-desc">Quantitativo da semana</div>
        </div>
        <div class="stat bg-error text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="book" />
            </div>
            <div class="stat-title">Produtos</div>
            <div class="stat-value">31K</div>
            <div class="stat-desc">Sem estoque</div>
        </div>
        <div class="stat bg-primary text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="book" />
            </div>
            <div class="stat-title">Produtos</div>
            <div class="stat-value">31K</div>
            <div class="stat-desc">Cadastrados</div>
        </div>
        <div class="stat bg-primary text-white shadow-lg">
            <div class="stat-figure text-secondary">
                <font-awesome-icon class="text-white text-xl" icon="dollar" />
            </div>
            <div class="stat-title">Vendas</div>
            <div class="stat-value">31K</div>
            <div class="stat-desc">Quantitativo da semana</div>
        </div>
    </div>

    <div class="grid grid-cols-2 my-12 gap-8">
        <div class="bg-base-200">
            <div class="flex gap-2 items-center mb-4 p-4">
                <font-awesome-icon icon="chart-bar" class="text-3xl bg-info p-2 text-white" />
                <p class="text-xl">Estatisticas de vendas</p>
            </div>

            <div class="mx-auto px-12">
                <Bar
                    :height="200"
                    :chart-data="chartData"
                />
            </div>
        </div>

        <div class="bg-base-200">
            <div class="flex gap-2 items-center mb-4 p-4">
                <font-awesome-icon icon="warning" class="text-3xl bg-warning p-2 text-white" />
                <p class="text-xl">Alertas</p>
            </div>
        </div>
    </div>
    
    <p class="text-center text-sm text-neutral mt-10 container__child">
      &copy; 2022 <a href="#" class="hover:underline" target="_blank">MultiTech</a>. All rights reserved.
    </p>
  </div>
</template>

<script setup lang="ts">

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = {
    labels: [ 'Total pago em produtos', 'Total em vendas' ],
    datasets: [
        { 
            label: 'MercanTree',
            data: [4000, 2250],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
            ],
            barThickness: 50,
        },
    ]
}

</script>

<style>
</style>