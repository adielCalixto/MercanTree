<template>
    <div class="lg:ml-64 mx-auto container relative">
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
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { RouterView, RouterLink } from "vue-router"

export default defineComponent({
    name: 'MtModelPage',
    components: {
        RouterView,
        RouterLink
    },
})
</script>