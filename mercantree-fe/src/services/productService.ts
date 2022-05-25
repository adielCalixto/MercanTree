import { Product } from '../interfaces/products/product.interface'
import useApi from '../composables/useApi'

export default function ProductService() {
    const { list, retrieve, update, create, destroy } = useApi<Product>('products')

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
    }
}