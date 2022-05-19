interface Transaction {
    id?: number;
    amount: number;
    created?: string;
    payment: number;
    cash_register?: number;
    type: string;
}

export default Transaction