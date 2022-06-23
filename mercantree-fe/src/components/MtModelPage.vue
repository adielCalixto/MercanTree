<template>
    <Suspense>
        <div class="md:ml-48 mx-auto container max-w-full min-h-screen relative overflow-y-hidden overflow-x-auto">
            <div class="text-sm breadcrumbs mb-4">
                <ul>
                    <li v-for="i in $route.matched.length - 2">
                        <router-link :to="$route.matched[i].path">{{ $route.matched[i].name }}</router-link>
                    </li>
                    <li>
                        {{ $route.name }}
                    </li>
                </ul>
            </div>
            <router-view />

        </div>
        <template #fallback>
            Loading...
        </template>
    </Suspense>
</template>

<script setup lang="ts">

import { Suspense } from "vue"
import { RouterView, RouterLink } from "vue-router"

</script>