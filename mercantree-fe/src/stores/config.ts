import { defineStore } from 'pinia'
import Config from '../interfaces/config/config.interface'
import { Theme } from '../interfaces/config/config.interface'

export const useStore = defineStore('config', {
    state: (): Config => {
        return {
            theme: Theme.LIGHT,
            add_product_to_order_when_unique: false,
        }
    },
    actions: {
        setTheme() {
            document.body.dataset['theme'] = this.theme
        },

        saveConfig() {
            window.localStorage.setItem('config', JSON.stringify(this.$state))
        },

        getConfig() {
            const config = window.localStorage.getItem('config')
            if (config) {
                this.$state = JSON.parse(config)
            }
        }
    }
})