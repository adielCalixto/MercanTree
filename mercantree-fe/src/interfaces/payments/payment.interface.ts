enum PaymentType {
    "SalePayment" = "SALE",
    "CashRegisterPayment" = "CHRG"
}


interface Payment {
    amount: number;
    is_paid: boolean;
    paid_amount?: string;
    id?: number;
    type?: PaymentType;
}

export default Payment
export { PaymentType }