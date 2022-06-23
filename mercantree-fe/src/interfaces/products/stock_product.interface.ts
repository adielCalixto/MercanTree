interface StockProduct {
    id?: number;
    product: number;
    delete_on_deplete: boolean;
    price: string;
    purchase_price: string;
    quantity: string;
    expires_at?: string;
    supplier?: number;
    created?: string;
    updated?: string;
}

export default StockProduct