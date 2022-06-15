import axios from "../boot/axios"
import useApi from "../composables/useApi"
import Order, { ExpandedOrder } from "../interfaces/orders/order.interface"
import errorService from "./errorService"
import OrderPaymentAmount from "../interfaces/orders/order_payment_amount.interface"

export default function OrderService() {
    const { list, retrieve, update, create, destroy } = useApi<Order>('orders')

    const retrieveExpanded = async (id: number): Promise<ExpandedOrder> => {
        return axios.get(`api/orders/${id}?expand=user,products.product`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const paymentAmount = async (interval = ''): Promise<OrderPaymentAmount> => {
        return axios.get(`api/orders/payment_amount/?interval=${interval}`)
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
        retrieveExpanded,
        paymentAmount,
    }
}