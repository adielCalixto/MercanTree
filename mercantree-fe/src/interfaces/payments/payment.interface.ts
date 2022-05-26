enum PaymentType {
    "SalePayment" = "SALE",
    "CashRegisterPayment" = "CHRG"
}


interface Payment {
    amount: string;
    is_paid: boolean;
    paid_amount?: string;
    id?: number;
    type?: PaymentType;
}

export default Payment
export { PaymentType }