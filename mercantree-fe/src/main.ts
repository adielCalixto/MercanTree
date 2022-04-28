import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from './services/axios'

import App from './App.vue'
import './index.css'
import router from './router'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.config.globalProperties.$axios = {...axios}
app.mount('#app')