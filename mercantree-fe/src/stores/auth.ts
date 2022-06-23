import { defineStore } from 'pinia'
import { LoggedUser, LoginUser } from '../interfaces/users/user.interface'
import authService from '../services/authService'
import axios from '../boot/axios'

export const useStore = defineStore('auth', {
    state: ():LoggedUser => {
        return {
            username: '',
            token: '',
            id: undefined,
        }
    },
    actions: {
        async loginUser(user: LoginUser) {
            return authService.login({ username: user.username, password: user.password })
            .then(response => {
                this.token = response.token
                this.username = response.user_name
                this.id = response.user_id
                axios.defaults.headers.common['Authorization'] = `Token ${response.token}`;
                window.sessionStorage.setItem('mercantree-auth', JSON.stringify(this.$state))
                return Promise.resolve()
            })
            .catch(error => {
                return Promise.reject(error)
            })
        },
        logoutUser() {
            delete axios.defaults.headers.common['Authorization'];
            window.sessionStorage.removeItem('mercantree-auth')

            this.token = ''
            this.username = ''
            this.id = undefined
        },
        restoreSession() {
            const prevState = window.sessionStorage.getItem('mercantree-auth')
            
            if(prevState != undefined) {
                const state: LoggedUser = JSON.parse(prevState)

                this.$reset
                this.$state = state
                axios.defaults.headers.common['Authorization'] = `Token ${state.token}`;
            }
        }
    }
})
