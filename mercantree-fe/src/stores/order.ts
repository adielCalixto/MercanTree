import { defineStore } from 'pinia'
import Order from '../interfaces/orders/order.interface'
import { Product } from '../interfaces/products/product.interface';
import CashRegisterService from '../services/cashRegisterService'
import OrderService from '../services/orderService'

interface ProductWithQuantity {
    quantity: number;
    data: Product;
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
