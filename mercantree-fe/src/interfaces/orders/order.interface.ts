import OrderProduct from "./order_product.interface";

interface Order {
    user: number;
    payment: number;
    id?: Number;
}

export default Order