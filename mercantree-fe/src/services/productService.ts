import { Product } from '../interfaces/products/product.interface'
import useApi from '../composables/useApi'
import axios from '../boot/axios'
import errorService from './errorService'
import ProductsPaidAmount from '../interfaces/products/product_paid_amount.interface'
import { APIListResponse } from '../interfaces/common/response.interface'

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