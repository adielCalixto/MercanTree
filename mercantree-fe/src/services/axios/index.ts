import Axios from 'axios'

const instance = Axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        'Accept-content': 'application/json'
    }
})

export default instance