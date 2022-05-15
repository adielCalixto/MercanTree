<template>
    <div class="max-w-xl mx-auto p-4 shadow-md my-4">
        <div class="flex bg-base-200 px-4 py-2 mb-8 items-center text-base-content">            
            <font-awesome-icon
            class="text-4xl mr-4"
            icon="cash-register" />
            <p class="text-2xl">Abrir o caixa</p>
        </div>
        <div>
            <form method="POST">
                <div class="flex gap-4 w-full items-center">
                    <label>Valor inicial:</label>
                    <input
                    type="number"
                    min="0"
                    class="input input-sm input-primary">
                </div>
                <div class="flex gap-4 justify-end mt-8">
                    <button
                    class="btn btn-primary btn-outline"
                    type="submit">
                        Confirmar
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">

</script>

<style>

</style>