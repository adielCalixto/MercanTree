<template>
    <div>
        <div class="grid grid-cols-2 md:grid-cols-4 w-full my-8 gap-4">
            <div
            @click="openModal = modalList.CLOSE_CASH_REGISTER"
            class="btn btn-ghost shadow btn-md">
                Fechar caixa
                <font-awesome-icon
                class="text-lg ml-2"
                icon="remove" />
            </div>

            <div
            @click="openModal = modalList.SHOW_STATS"
            class="btn btn-ghost shadow btn-md">
                Ver relatório
                <font-awesome-icon
                class="text-lg ml-2"
                icon="book" />
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

                <div class="form-control">
                    <div class="input-group">
                        <input
                        type="text"
                        placeholder="Search…"
                        class="input input-sm input-bordered">

                        <button @click="" class="btn btn-square btn-sm">
                            <font-awesome-icon icon="search" />
                        </button>
                    </div>
                </div>
            </div>

            <div v-if="0">
                Nenhuma transação encontrado
            </div>

            <mt-table :table="table" v-else >
                <tr>
                    <th>1</th>
                    <th>12:30</th>
                    <th>Vazio</th>
                    <th>Venda</th>
                    <th>R$200,00</th>
                    <th>R$0,00</th>
                    <th>R$200,00</th>
                    <th></th>
                </tr>
            </mt-table>

            <div class="w-full flex justify-center mt-4">
                <div class="btn-group">
                    <button class="btn btn-sm"
                    v-for="page in pages"
                    :class="{'btn-active': page == activePage}"
                    @click="activePage = page">{{ page }}</button>
                </div>
            </div>
        </div>

        <div>
            <div class="modal modal-open"
            v-if="openModal == modalList.ADD_CASH">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Adicionar dinheiro ao caixa</h3>

                    <div class="modal-action">
                        <a class="btn btn-primary btn-sm">Salvar</a>
                        <a @click="openModal = modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>

                    <div class="divider"></div>

                    <form
                    class="flex gap-4"
                    action="#"
                    method="post">                    
                        <div class="form-control w-full">
                            <label class="label">Observações</label>
                            <textarea
                            class="textarea textarea-ghost resize-none"
                            rows="1"
                            placeholder="Observações">
                            </textarea>
                        </div>

                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            value="0">
                        </div>
                    </form>
                </div>
            </div>

            <div class="modal modal-open"
            v-if="openModal == modalList.REMOVE_CASH">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Retirar dinheiro do caixa</h3>

                    <div class="modal-action">
                        <a class="btn btn-primary btn-sm">Salvar</a>
                        <a @click="openModal=modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>

                    <div class="divider"></div>

                    <form
                    class="flex gap-4"
                    action="#"
                    method="post">                    
                        <div class="form-control w-full">
                            <label class="label">Observações</label>
                            <textarea
                            class="textarea textarea-ghost resize-none"
                            rows="1"
                            placeholder="Observações">
                            </textarea>
                        </div>

                        <div class="form-control">
                            <label class="label">Valor</label>
                            <input
                            class="input input-sm input-primary"
                            type="number"
                            name="amount"
                            min="0"
                            value="0">
                        </div>
                    </form>
                </div>
            </div>

            <div class="modal modal-open"
            v-if="openModal == modalList.SHOW_STATS">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Detalhes do caixa</h3>

                    <div class="modal-action">
                        <a @click="openModal=modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>
                </div>
            </div>

            <div class="modal modal-open"
            v-if="openModal == modalList.CLOSE_CASH_REGISTER">
                <div class="modal-box max-w-xl">
                    <h3 class="font-bold text-lg">Fechar caixa</h3>
                    <p class="text-md">Tem certeza que deseja fechar o caixa?</p>

                    <div class="modal-action">
                        <a class="btn btn-warning btn-sm">Confirmar</a>
                        <a @click="openModal=modalList.NONE"
                        class="btn btn-outline btn-error btn-sm">Cancelar</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="warning">
            <div class="modal modal-open">
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
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { RouterLink } from 'vue-router'
    import MtTable from '../MtTable.vue'

    const pages = ref(1)
    const activePage = ref(1)
    const table = {
        name: 'Transações',
        fields: [
            '',
            'Hora',
            'Detalhes',
            'Tipo',
            'Valor',
            'Desconto',
            'Valor Pago',
        ]
    }

    const openModal = ref('')
    const modalList = ref({
        CLOSE_CASH_REGISTER: 'CCR',
        ADD_CASH: 'ACH',
        REMOVE_CASH: 'RCH',
        SHOW_STATS: 'SST',
        NONE: '',
    })

</script>

<style>

</style>