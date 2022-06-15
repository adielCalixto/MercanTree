import { Product } from '../interfaces/products/product.interface'
import useApi from '../composables/useApi'
import axios from '../boot/axios'
import errorService from './errorService'
import ProductsPaidAmount from '../interfaces/products/product_paid_amount.interface'
import { APIListResponse } from '../interfaces/common/response.interface'

export default function ProductService() {
    const { list, retrieve, update, create, destroy } = useApi<Product>('products')

    const paidAmount = async (): Promise<ProductsPaidAmount> => {
        return axios.get('api/products/paid_price/')
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const nextToExpire = async (): Promise<APIListResponse<Product>> => {
        return axios.get('api/products/next_to_expiration/')
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
        paidAmount,
        nextToExpire,
    }
}