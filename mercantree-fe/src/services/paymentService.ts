import axios from '../boot/axios'
import useApi from '../composables/useApi'
import Payment from '../interfaces/payments/payment.interface'
import errorService from './errorService'

export default function PaymentService() {
    const { list, retrieve, update, create, destroy } = useApi<Payment>('payments')

    const deposit = async (id: number, amount: number, cash_register?: number, details?: string): Promise<any> => {
        return axios.post(`api/payments/${id}/deposit/`, {
            amount,
            cash_register,
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

    const withdraw = async (id: number, amount: number, cash_register?: number, details?: string): Promise<any> => {
        return axios.post(`api/payments/${id}/withdraw/`, {
            amount,
            cash_register,
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

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
        deposit,
        withdraw,
    }
}
