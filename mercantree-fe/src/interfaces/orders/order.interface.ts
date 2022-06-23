import Payment from "../payments/payment.interface";
import { User } from "../users/user.interface";
import OrderProduct, { ExpandedOrderProduct } from "./order_product.interface";

enum OrderStatus {
    'Done' = 'DN',
    'Pending' = 'PD',
    'Closed' = 'CC'
}


interface Order {
    user: number;
    payment: Payment;
    products?: OrderProduct[] | any[];
    coupon?: string;
    id?: number;
    created?: string;
    status?: OrderStatus;
    details?: string;
}

interface ExpandedOrder extends Omit<Order, 'user'> {
    user: User;
}

export default Order
export type { ExpandedOrder }
export { OrderStatus }