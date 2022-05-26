import { Product } from "../products/product.interface";

interface OrderProduct {
    product: number;
    quantity: number;
    id?: string;
    order?: number;
}

interface ExpandedOrderProduct extends Omit<OrderProduct, 'product'> {
    product: Product;
}

export default OrderProduct
export type { ExpandedOrderProduct }