import axios from '../boot/axios'
import { APIListResponse } from '../interfaces/common/response.interface'
import errorService from '../services/errorService'

export default function useApi<T>(url: string) {
    const list = async (page: number = 1, search: string = '', ordering: string ='' ): Promise<APIListResponse<T>> => {
        return axios.get(`api/${url}/?page=${page}&search=${search}&ordering=${ordering}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const retrieve = async (id: number): Promise<T> => {
        return axios.get(`api/${url}/${id}`)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const create = async (form: T): Promise<T> => {
        return axios.post(`api/${url}/`, form)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const update = async (id:number, form: T): Promise<T> => {
        return axios.put(`api/${url}/${id}/`, form)
        .then(response => {
            return Promise.resolve(response.data)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    const destroy = async (id: number): Promise<String> => {
        return axios.delete(`api/${url}/${id}/`)
        .then(response => {
            return Promise.resolve(response.statusText)
        })
        .catch(error => {
            errorService().onError(error)
            return Promise.reject(error)
        })
    }

    return {
        list,
        create,
        retrieve,
        destroy,
        update,
    }
}