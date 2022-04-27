<template>
    <div class="max-w-md mx-auto my-16 p-4">
        <div class="text-center mb-8">
            <h1 class="text-xl">Faça login no sistema</h1>
        </div>

        <div class="p-4 bg-white shadow-lg">
            <div class="form-control w-full">
                <label class="label">
                    <span class="label-text">Email</span>
                </label>
                <input type="email" placeholder="email" class="input input-bordered w-full">
            </div>
            <div class="form-control w-full my-4">
                <label class="label">
                    <span class="label-text">Senha</span>
                </label>
                <input type="password" placeholder="senha" class="input input-bordered w-full">
            </div>
            <div class="form-control w-full">
                <button class="btn btn-success btn-outline btn-block">Entrar</button>
            </div>
        </div>
    </div>
</template>

<script lang='ts'>
export default {

}
</script>

<style>

</style>