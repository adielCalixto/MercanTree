enum TransactionType {
    "Depósito" = "CI",
    "Saque" = "CB"
}


interface Transaction {
    id?: number;
    amount: string;
    created?: string;
    payment: number;
    cash_register?: number;
    type: TransactionType;
    details?: string;
}

export default Transaction
export { TransactionType }