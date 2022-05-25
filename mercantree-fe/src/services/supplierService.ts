import useApi from '../composables/useApi'
import { Supplier } from '../interfaces/suppliers/supplier.interface'

export default function SupplierService() {
    const { list, retrieve, update, create, destroy } = useApi<Supplier>('suppliers')

    return {
        list,
        retrieve,
        update,
        create,
        destroy,
    }
}