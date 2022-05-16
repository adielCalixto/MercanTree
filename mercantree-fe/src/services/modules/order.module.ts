import axios from '../axios'
import Order from '../../interfaces/orders/order.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'


class OrderService {
    list(page: number = 1, search: string = '', ordering: string = '', omit: string = ''): Promise<APIListResponse<Order>> {
        return axios.get(`api/orders/?page=${page}&search=${search}&ordering=${ordering}&omit=${omit}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<Order> {
        return axios.get(`api/orders/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({ user, payment, products }: Order): Promise<Order> {
        return axios.post('api/orders/', {
            user,
            payment,
            products,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, { user, payment, products }: Order): Promise<Order> {
        return axios.put(`api/orders/${id}/`, {
            user,
            payment,
            products,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/orders/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }
}

export default new OrderService()