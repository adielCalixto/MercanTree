import axios from '../axios'
import Payment from '../../interfaces/payments/payment.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'


class PaymentService {
    list(page: number = 1, ordering: string = ''): Promise<APIListResponse<Payment>> {
        return axios.get(`api/payments/?page=${page}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<Payment> {
        return axios.get(`api/payments/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({ amount, is_paid, type }: Payment): Promise<Payment> {
        return axios.post('api/payments/', {
            amount,
            is_paid,
            type,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, { amount, is_paid }: Payment): Promise<Payment> {
        return axios.put(`api/payments/${id}/`, {
            amount,
            is_paid,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/payments/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    deposit(id: number, amount: number, cash_register?: number): Promise<any> {
        return axios.post(`api/payments/${id}/deposit/`, {
            amount,
            cash_register,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    withdraw(id: number, amount: number, cash_register?: number): Promise<any> {
        return axios.post(`api/payments/${id}/withdraw/`, {
            amount,
            cash_register,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }
}

export default new PaymentService()