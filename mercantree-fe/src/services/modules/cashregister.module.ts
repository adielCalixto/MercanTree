import axios from '../../boot/axios'
import CashRegister from '../../interfaces/payments/cashregister.interface'
import Transaction from '../../interfaces/payments/transaction.interface'
import { PaymentType } from '../../interfaces/payments/payment.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'
import paymentModule from './payment.module'
import CashRegisterStats from '../../interfaces/payments/cashregisterstats.interface'


class CashRegisterService {
    list(page: number = 1, open: boolean = false): Promise<APIListResponse<CashRegister>> {
        return axios.get(`api/cashregister/?page=${page}&open=${open}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<CashRegister> {
        return axios.get(`api/cashregister/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({ details, initial_amount, open, user }: CashRegister): Promise<CashRegister> {
        return axios.post('api/cashregister/', {
            user,
            details,
            initial_amount,
            open,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, { details, initial_amount, open, user }: CashRegister): Promise<CashRegister> {
        return axios.put(`api/cashregister/${id}/`, {
            user,
            details,
            initial_amount,
            open,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/cashregister/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    transactions(id: number, page: number = 1): Promise<APIListResponse<Transaction>> {
        return axios.get(`api/cashregister/${id}/transactions/?page=${page}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    report(id: number): Promise<CashRegisterStats> {
        return axios.get(`api/cashregister/${id}/report/`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    close(id: number, closed_amount: number, details: string): Promise<Transaction> {
        return axios.patch(`api/cashregister/${id}/`, {
            open: false,
            closed_amount,
            details,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    deposit(id: number, amount: number): Promise<Transaction> {
        // deposit cash into the cashregister
        return paymentModule.create({ amount, is_paid: true, type: PaymentType.CashRegisterPayment })
        .then(payment => {
            // try to create a payment and then pass the id to create a transaction
            if (payment.id) {
                return paymentModule.deposit(payment.id, amount, id)
                .then(transaction => {
                    // transaction created, return the data
                    return Promise.resolve(transaction.data)
                })
                .catch(e => {
                    // if cannot create the transaction, destroy the payment
                    if (payment.id)
                        paymentModule.destroy(payment.id)
                    return Promise.reject(e)
                })
            }
        })
        .catch(e => {
            return Promise.reject(e)
        })
    }

    withdraw(id: number, amount: number): Promise<Transaction> {
        // withdraw cash from the cashregister
        return paymentModule.create({ amount, is_paid: true, type: PaymentType.CashRegisterPayment })
        .then(payment => {
            // try to create a payment and then pass the id to create a transaction
            if (payment.id) {
                return paymentModule.withdraw(payment.id, amount, id)
                .then(transaction => {
                    // transaction created, return the data
                    return Promise.resolve(transaction.data)
                })
                .catch(e => {
                    // if cannot create the transaction, destroy the payment
                    if (payment.id)
                        paymentModule.destroy(payment.id)
                    return Promise.reject(e)
                })
            }
        })
        .catch(e => {
            return Promise.reject(e)
        })
    }
}

export default new CashRegisterService()