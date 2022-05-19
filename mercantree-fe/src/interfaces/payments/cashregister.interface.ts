interface CashRegister {
    details: string;
    initial_amount: number;
    closed_amount?: number;
    open: boolean;
    user?: number;
    created?: string;
    id?: number;
}

export default CashRegister