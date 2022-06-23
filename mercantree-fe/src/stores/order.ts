import { defineStore } from 'pinia'
import Order from '../interfaces/orders/order.interface'
import { Product } from '../interfaces/products/product.interface'
import StockProduct from '../interfaces/products/stock_product.interface'
import OrderService from '../services/orderService'

interface ProductWithQuantity {
    quantity: number;
    data: StockProduct & { product: Product };
}

interface OrderStore {
    order?: Order;
    products: ProductWithQuantity[];
}

export const useOrderStore = defineStore('order', {
    state: (): OrderStore => {
        return {
            order: undefined,
            products: [],
        }
    },
    actions: {
        save() {
            if (!this.order) return
    
            return OrderService().create(this.order)
            .then((response) => {
                this.order = response
                return Promise.resolve()
            })
            .catch(e => {
                return Promise.reject(e)
            })
        }
    }
})
