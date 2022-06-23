<template>
    <aside 
    class="sidebar fixed hidden bg-base-200 z-20 h-screen top-0 left-0 pt-16 md:flex flex-shrink-0 flex-col w-full md:w-48 transition-width duration-75" 
    aria-label="Sidebar">
        <ul @click="hideNavbar()" class="menu px-2 py-4 rounded-box overflow-y-auto">
            <li class="sidebar__item">
                <router-link to="/home">
                    <font-awesome-icon icon="home" />
                    Home
                </router-link>
            </li>
            <li class="sidebar__item">
                <router-link to="/stock">
                    <font-awesome-icon icon="book" />
                    Estoque
                </router-link>
            </li>

            <li class="sidebar__item">
                <router-link to="/suppliers">
                    <font-awesome-icon icon="truck" />
                    Fornecedores
                </router-link>
            </li>

            <li class="sidebar__item">
                <router-link to="/sell">
                    <font-awesome-icon icon="dollar" />
                    Venda
                </router-link>
            </li>

            <li class="sidebar__item">
                <router-link to="/cashregister">
                    <font-awesome-icon icon="cash-register" />
                    Caixa
                </router-link>
            </li>

            <li class="sidebar__item">
                <router-link to="/cashregister/closed">
                    <font-awesome-icon icon="cash-register" />
                    Caixas Fechados
                </router-link>
            </li>

            <div class="divider"></div>

            <li class="sidebar__item">
                <router-link to="/config">
                    <font-awesome-icon icon="cog" />
                    Configurações
                </router-link>
            </li>

        </ul>
    </aside>
</template>

<script setup lang="ts">

import { RouterLink } from "vue-router"

const hideNavbar = () => {
    document.body.classList.remove('sidebar--open')
}

</script>

<style>

</style>