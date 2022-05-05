import Axios from 'axios'

const instance = Axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json',
    }
})

export default instance