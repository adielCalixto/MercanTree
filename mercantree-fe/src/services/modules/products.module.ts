import axios from '../../boot/axios'
import { Product } from '../../interfaces/products/product.interface'
import { APIListResponse } from '../../interfaces/common/response.interface'


class ProductService {
    list(page:number = 1, search:string = '', ordering:string = ''): Promise<APIListResponse<Product>> {
        return axios.get(`api/products/?page=${page}&search=${search}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    retrieve(id: number): Promise<Product> {
        return axios.get(`api/products/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    create({name, description, price, expires_at, barcode, category, supplier_id, supplier_price, quantity}: Product): Promise<Product> {
        return axios.post('api/products/', {
            name,
            description,
            price,
            expires_at,
            category,
            supplier_id,
            barcode,
            supplier_price,
            quantity,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    update(id:number, {name, description, price, expires_at, barcode, category, supplier_id, supplier_price, quantity}: Product): Promise<Product> {
        return axios.put(`api/products/${id}/`, {
            name,
            description,
            price,
            expires_at,
            category,
            supplier_id,
            barcode,
            supplier_price,
            quantity,
        })
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }

    destroy(id: number): Promise<String> {
        return axios.delete(`api/products/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            return Promise.reject(error)
        })
    }
}

export default new ProductService()