interface Product {
    name: string;
    id?: number;
    description: string;
    barcode?: string;
    category: string;
    supplier_id?: number;
}

export type { Product }