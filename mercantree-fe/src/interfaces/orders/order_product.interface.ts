import StockProduct from "../products/stock_product.interface"

interface OrderProduct {
    product: number;
    uid?: string;
    order?: number;
    sale_quantity: string;
    sale_price?: string;
    reference?: string;
}

interface ExpandedOrderProduct extends Omit<OrderProduct, 'product'> {
    product: StockProduct;
}

export default OrderProduct
export type { ExpandedOrderProduct }