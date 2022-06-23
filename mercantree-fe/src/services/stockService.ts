import axios from '../boot/axios'
import useApi from '../composables/useApi'
import { APIListResponse } from '../interfaces/common/response.interface'
import { Product } from '../interfaces/products/product.interface'
import ProductsPaidAmount from '../interfaces/products/product_paid_amount.interface'
import StockProduct from '../interfaces/products/stock_product.interface'
import errorService from './errorService'

export default function StockService() {
    const { list, retrieve, update, create, destroy } = useApi<StockProduct>('stock')

    const listExpanded = async (page=1, search='', ordering=''): Promise<APIListResponse<StockProduct & {product: Product}>> => {
        return axios.get(`/api/stock/?expand=product&search=${search}&page=${page}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const paidAmount = async (): Promise<ProductsPaidAmount> => {
        return axios.get('api/stock/paid_price/')
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const nextToExpire = async (): Promise<APIListResponse<StockProduct & { product: Product }>> => {
        return axios.get('api/stock/next_to_expiration/?expand=product')
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
        listExpanded,
        nextToExpire,
        paidAmount,
    }
}