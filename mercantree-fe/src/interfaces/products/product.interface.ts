interface Product {
    name: string;
    id?: number;
    description: string;
    expires_at: string;
    price: number;
    barcode: string;
    category: string;
    supplier_id?: number;
    supplier_price: number;
    quantity: number;
    stock_quantity?: number;
}

export type { Product }