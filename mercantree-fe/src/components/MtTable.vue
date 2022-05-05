<template>
    <div class="overflow-x-auto w-full">
        <table class="table table-compact w-full">
            <thead>
                <tr>
                    <th v-for="field in table.fields">
                        {{ field }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <slot />
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { PropType, defineComponent } from "vue";

interface TableData {
    name: String;
    fields: String[];
}

export default defineComponent ({
    name: 'MtTable',
    props: {
        table: {
            type: Object as PropType<TableData>,
            required: true,
        },
    },
})

</script>