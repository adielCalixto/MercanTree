import Payment from "../payments/payment.interface";
import OrderProduct from "./order_product.interface";

interface Order {
    user: number;
    payment: Payment;
    products?: OrderProduct[] | any[];
    coupon?: string;
    id?: number;
    created?: Date;
    status?: 'string';
}

export default Order