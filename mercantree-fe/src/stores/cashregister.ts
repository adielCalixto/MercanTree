import { defineStore } from 'pinia'
import { APIListResponse } from '../interfaces/common/response.interface';
import CashRegister from '../interfaces/payments/cashregister.interface'
import CashRegisterStats from '../interfaces/payments/cashregisterstats.interface';
import Transaction from '../interfaces/payments/transaction.interface';
import CashRegisterService from '../services/cashRegisterService'

interface CashRegisterStore {
    cashRegister: CashRegister;
    transactions: APIListResponse<Transaction>;
    hasCashRegister: boolean;
    stats?: CashRegisterStats;
}

export const useStore = defineStore('cashregister', {
    state: (): CashRegisterStore => {
        return {
            cashRegister: {
                id: undefined,
                details: '',
                initial_amount: 0,
                open: false,
                created: undefined,
                closed_amount: undefined,
                user: undefined,
            },
            hasCashRegister: false,
            transactions: {
                count: 0,
                results: [],
            },
        }
    },
    actions: {
        getTransactions() {
            if (!this.cashRegister.id)
                return

            return CashRegisterService().transactions(this.cashRegister.id)
            .then(response => {
                this.transactions = response
            })
            .catch(e => {
                return Promise.reject(e)
            })
        },

        getCashRegister() {
            return CashRegisterService().getOpen()
            .then(response => {
                if (response.count > 0) {
                    this.hasCashRegister = true
                    this.cashRegister = response.results[0]
                }
                return Promise.resolve()
            })
            .catch(e => {
                return Promise.reject(e)
            })
        },

        getStats() {
            if (!this.cashRegister.id)
                return;

            return CashRegisterService().report(this.cashRegister.id)
            .then(response => {
                this.stats = response
                return Promise.resolve()
            })
            .catch(e => {
                return Promise.reject(e)
            })
        },

        close(closed_amount: number, details: string) {
            if (!this.cashRegister.id)
                return
    
            return CashRegisterService().close(this.cashRegister.id, closed_amount, details)
            .then(() => {
                this.$reset()
                return Promise.resolve()
            })
            .catch(e => {
                return Promise.reject(e)
            })
        }
    }
})
