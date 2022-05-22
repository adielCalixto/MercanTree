<template>
    <div class="relative md:ml-48 overflow-y-auto container max-w-full">
        <div class="max-w-xl">
            <div class="mb-4 flex flex-col gap-4">
                <h1 class="text-2xl mb-8">Perfil</h1>

                <div class="grid grid-cols-2 text-md">
                    <p>Nome:</p>
                    <p class="font-semibold place-self-end">{{ authStore.username }}</p>
                </div>

                <div class="grid grid-cols-2 text-md">
                    <div>
                        <p>Pagina do administrador:</p>
                    </div>
                    <div class=" place-self-end">
                        <a
                        class="font-semibold link"
                        href="http://localhost:8000/admin"
                        target="_blank">
                            Admin
                            <font-awesome-icon icon="external-link" />
                        </a>
                    </div>
                </div>
            </div>

            <div class="divider"></div>

            <div class="profile-section mb-4 flex flex-col gap-4">
                <h1 class="text-2xl mb-8">Tema</h1>

                <div class="grid grid-cols-2 text-md">
                    <p>Tema escuro:</p>

                    <div class="form-control place-self-end">
                        <input
                        type="checkbox"
                        class="toggle toggle-primary"
                        v-model="state.theme"
                        @change="setTheme()" />
                    </div>
                </div>
            </div>

            <div class="divider"></div>

            <div class="profile-section mb-4 flex flex-col gap-4">
                <h1 class="text-2xl mb-8">Funcionalidades</h1>

                <div class="grid grid-cols-2 text-md">
                    <p>Auto adicionar produto na venda quando o resultado da busca for 1</p>

                    <div class="form-control place-self-end">
                        <input
                        type="checkbox"
                        class="toggle toggle-primary"
                        v-model="state.auto_add_product"
                        @change="setAutoAddProduct()" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useStore as useConfigStore } from '../../stores/config'
    import { useStore as useAuthStore } from '../../stores/auth';
    import { Theme } from '../../interfaces/config/config.interface'
    import { reactive } from 'vue'

    const configStore = useConfigStore()
    const authStore = useAuthStore()
    const state = reactive({
        theme: configStore.theme == Theme.DARK ? true : false,
        auto_add_product: configStore.add_product_to_order_when_unique,
    })

    const setTheme = () => {
        configStore.theme = state.theme ? Theme.DARK : Theme.LIGHT
        configStore.setTheme()
        configStore.saveConfig()
    }

    const setAutoAddProduct = () => {
        configStore.add_product_to_order_when_unique = state.auto_add_product
        configStore.saveConfig()
    }

</script>