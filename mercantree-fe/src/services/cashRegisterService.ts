import axios from "../boot/axios"
import useApi from "../composables/useApi"
import { APIListResponse } from "../interfaces/common/response.interface"
import CashRegister from "../interfaces/payments/cashregister.interface"
import CashRegisterStats from "../interfaces/payments/cashregisterstats.interface"
import { PaymentType } from "../interfaces/payments/payment.interface"
import Transaction from "../interfaces/payments/transaction.interface"
import errorService from "./errorService"
import PaymentService from "./paymentService"

export default function CashRegisterService() {
    const { list, retrieve, update, create, destroy } = useApi<CashRegister>('cashregister')

    const transactions = async (id: number, page: number = 1): Promise<APIListResponse<Transaction>> => {
        return axios.get(`api/cashregister/${id}/transactions/?page=${page}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {

            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const report = async (id: number): Promise<CashRegisterStats> => {
        return axios.get(`api/cashregister/${id}/report/`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {

            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const close = async (id: number, closed_amount: number, details: string): Promise<Transaction> => {
        return axios.patch(`api/cashregister/${id}/`, {
            open: false,
            closed_amount,
            details,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {

            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const getOpen = async (): Promise<APIListResponse<CashRegister>> => {
        return axios.get(`api/cashregister/?open=true`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {

            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const getClosed = async (): Promise<APIListResponse<CashRegister>> => {
        return axios.get(`api/cashregister/?open=false`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {

            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const deposit = async (id: number, amount: number, details: string): Promise<Transaction> => {
        // deposit cash into the cashregister
        return PaymentService().create({ amount: amount.toFixed(2), is_paid: true, type: PaymentType.CashRegisterPayment })
        .then(payment => {
            // try to create a payment and then pass the id to create a transaction
            if (payment.id) {
                return PaymentService().deposit(payment.id, amount, id, details)
                .then(transaction => {
                    // transaction created, return the data
                    return Promise.resolve(transaction.data)
                })
                .catch(e => {
                    // if cannot create the transaction, destroy the payment
                    if (payment.id)
                    PaymentService().destroy(payment.id)

                    errorService().onError(e)
                    return Promise.reject(e)
                })
            }
        })
        .catch(e => {

            errorService().onError(e)
            return Promise.reject(e)
        })
    }

    const withdraw = async (id: number, amount: number, details: string): Promise<Transaction> => {
        // withdraw cash from the cashregister
        return PaymentService().create({ amount: amount.toFixed(2), is_paid: true, type: PaymentType.CashRegisterPayment })
        .then(payment => {
            // try to create a payment and then pass the id to create a transaction
            if (payment.id) {
                return PaymentService().withdraw(payment.id, amount, id, details)
                .then(transaction => {
                    // transaction created, return the data
                    return Promise.resolve(transaction.data)
                })
                .catch(e => {
                    // if cannot create the transaction, destroy the payment
                    if (payment.id)
                    PaymentService().destroy(payment.id)

                    errorService().onError(e)
                    return Promise.reject(e)
                })
            }
        })
        .catch(e => {

            errorService().onError(e)
            return Promise.reject(e)
        })
    }

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
        transactions,
        report,
        close,
        deposit,
        withdraw,
        getOpen,
        getClosed,
    }
}