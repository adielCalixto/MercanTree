interface Product {
    name: string;
    id?: number;
    description: string;
    expires_at: Date;
    price: number;
    barcode: string;
    category: string;
    supplier_id?: number;
    supplier_price: number;
    quantity: number;
}

export type { Product }