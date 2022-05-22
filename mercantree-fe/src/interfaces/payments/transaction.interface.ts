enum TransactionType {
    "CashDeposit" = "CI",
    "CashBack" = "CB"
}


interface Transaction {
    id?: number;
    amount: number;
    created?: string;
    payment: number;
    cash_register?: number;
    type: TransactionType;
}

export default Transaction
export { TransactionType }