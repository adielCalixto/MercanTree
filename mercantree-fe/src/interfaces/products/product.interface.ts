interface Product {
    name: String;
    id?: Number;
    description: String;
    expires_at: Date;
    price: Number;
    barcode: String;
    category: String;
    supplier_id?: Number;
    supplier_price: Number;
    quantity: Number;
}

export type { Product }