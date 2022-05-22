import Payment from "../payments/payment.interface";
import OrderProduct from "./order_product.interface";

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
}

export default Order
export { OrderStatus }