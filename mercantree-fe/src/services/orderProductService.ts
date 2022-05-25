import useApi from "../composables/useApi"
import OrderProduct from "../interfaces/orders/order_product.interface"

export default function OrderProductService() {
    const { list, retrieve, update, create, destroy } = useApi<OrderProduct>('items')

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
    }
}