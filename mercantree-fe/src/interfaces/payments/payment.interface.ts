interface Payment {
    amount: string;
    is_paid: boolean;
    paid_amount?: string;
    id?: number;
}

export default Payment