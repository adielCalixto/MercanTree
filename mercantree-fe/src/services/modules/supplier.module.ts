import axios from '../../boot/axios'
import { APIListResponse } from '../../interfaces/common/response.interface'
import { Supplier } from '../../interfaces/suppliers/supplier.interface'


class SupplierService {
    list(page:number = 1, search:string = '', ordering:string = ''): Promise<APIListResponse<Supplier>> {
        return axios.get(`api/suppliers/?page=${page}&search=${search}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<Supplier> {
        return axios.get(`api/suppliers/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({ name, email, phone, cnpj, city, address, responsable }: Supplier): Promise<Supplier> {
        return axios.post('api/suppliers/', {
            name,
            email,
            phone,
            cnpj,
            city,
            address,
            responsable,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, { name, email, phone, cnpj, city, address, responsable }: Supplier): Promise<Supplier> {
        return axios.put(`api/suppliers/${id}/`, {
            name,
            email,
            phone,
            cnpj,
            city,
            address,
            responsable,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/suppliers/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }
}

export default new SupplierService()