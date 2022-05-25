import useApi from "../composables/useApi"
import Category from "../interfaces/products/category.interface"

export default function categoryService() {
    const { list, retrieve, update, create, destroy } = useApi<Category>('category')

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
    }
}