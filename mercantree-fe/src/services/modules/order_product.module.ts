import axios from '../axios'
import OrderProduct from '../../interfaces/orders/order_product.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'


class OrderProductService {
    list(page: number = 1, search: string = '', ordering: string = ''): Promise<APIListResponse<OrderProduct>> {
        return axios.get(`api/items/?page=${page}&search=${search}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<OrderProduct> {
        return axios.get(`api/items/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({ order, quantity, product }: OrderProduct): Promise<OrderProduct> {
        return axios.post('api/items/', {
            order,
            quantity,
            product,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, { order, quantity, product }: OrderProduct): Promise<OrderProduct> {
        return axios.put(`api/items/${id}/`, {
            order,
            quantity,
            product,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/items/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }
}

export default new OrderProductService()