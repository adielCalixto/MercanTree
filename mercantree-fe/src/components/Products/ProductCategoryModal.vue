<template>
    <div>
        <div class="modal modal-open">
            <div class="modal-box w-full max-w-xl">
                <h3 class="font-bold text-lg mb-4">Categorias</h3>

                <form @submit.prevent="addCategory()" class="mb-4">
                    <div class="form-control">
                        <div class="input-group justify-end">
                            <input
                            type="text"
                            placeholder="Adicionar categoria"
                            class="input input-sm input-bordered mr-2"
                            v-model="states.name" >

                            <button type="submit" class="btn btn-square btn-sm">
                                <font-awesome-icon icon="add" />
                            </button>
                        </div>
                    </div>
                </form>

                <div v-if="categories.count == 0">
                    Nenhuma categoria encontrada
                </div>
                
                <div class="overflow-y-auto max-h-48" v-else>
                    <mt-table :table="table">
                        <tr v-for="c in categories.results">
                            <td>
                                {{ c.id }}
                            </td>
                            <td class="w-8/12">
                                <div
                                v-if="states.editingFieldId === c.id"
                                class="flex items-center">
                                    <input
                                    class="input input-sm mr-2"
                                    type="text"
                                    :ref="(el) => { states.editingFields[c.id??0] = el}"
                                    v-model="c.name" />

                                    <button class="btn btn-sm btn-success btn-square" @click="editCategory(c.id)">
                                        <font-awesome-icon icon="check" />
                                    </button>
                                </div>

                                <div v-else @click="toggleEdit(c.id)">
                                    {{ c.name }}
                                </div>
                            </td>
                            <td>
                                <button
                                @click="deleteCategory(c.id)"
                                class="btn btn-sm btn-square btn-error ml-auto mr-2 flex">
                                    <font-awesome-icon icon="trash" />
                                </button>
                            </td>
                        </tr>
                    </mt-table>
                </div>
                
                <div class="modal-action">
                    <button @click="$emit('close')" class="btn btn-sm btn-ghost">
                        Fechar
                        <font-awesome-icon class="ml-2" icon="close" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineEmits, onMounted, reactive, ref, nextTick } from 'vue'
import { APIListResponse } from '../../interfaces/common/response.interface'
import Category from '../../interfaces/products/category.interface'
import categoryService from '../../services/categoryService'
import MtTable from '../MtTable.vue'
import swal from 'sweetalert'
import errorService from '../../services/errorService'

interface Emits {
    (e: 'close'): void;
}

interface CategoryState {
    name: string;
    editingFieldId?: number;
    editingFields: any[];
}

const table = ref({
    name: 'Categories',
    fields: [
        '',
        'Nome',
        ''
    ]
})
const emit = defineEmits<Emits>()
const categories = ref<APIListResponse<Category>>({ count: 0, results: [] })
const states = reactive<CategoryState>({
    name: '',
    editingFieldId: undefined,
    editingFields: [],
})

const getCategories = async () => {
    try {
        const response = await categoryService().list()
        categories.value = response
    }
    catch(e) {
        console.error(e)
    }
}

const addCategory = async () => {
    try {
        if(!states.name)
            return

        await categoryService().create({name: states.name})

        swal({
                title: 'Sucesso',
                text: 'Categoria criada',
                icon: 'success'
            })

        getCategories()
    }
    catch(e) {
        console.error(e)
    }
}

const deleteCategory = async (id?: number) => {
    try {
        if (!id) return

        errorService().onWarn()
        .then(async () => {
            await categoryService().destroy(id)
            getCategories()

            swal({
                title: 'Sucesso',
                text: 'Categoria deletada',
                icon: 'success'
            })
        })
        .catch(() => {
            return
        })
    }
    catch(e) {
        console.error(e)
    }
}

const editCategory = async (id?:number) => {
    try {
        if (!id) {
            return
        }

        if (states.editingFields[id].value) {
            await categoryService().update(id, { name: states.editingFields[id].value })
            states.editingFieldId = undefined
            await getCategories()

            swal({
                title: 'Sucesso',
                text: 'Categoria editada',
                icon: 'success'
            })
        }
    }
    catch(e) {
        console.error(e)
    }
}

const toggleEdit = async (id?: number) => {
    if(id) {
        states.editingFieldId = id

        await nextTick()

        if(states.editingFields[id].focus) {
            states.editingFields[id].focus()
        }
    }
    else {
        states.editingFieldId = undefined
    }
}

onMounted(async () => {
    await getCategories()
})

</script>