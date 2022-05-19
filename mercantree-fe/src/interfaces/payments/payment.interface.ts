interface Payment {
    amount: number;
    is_paid: boolean;
    paid_amount?: string;
    id?: number;
    type?: string;
}

export default Payment