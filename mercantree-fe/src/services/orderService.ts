import useApi from "../composables/useApi"
import Order from "../interfaces/orders/order.interface"

export default function OrderService() {
    const { list, retrieve, update, create, destroy } = useApi<Order>('orders')

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
    }
}