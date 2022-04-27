import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from './services/axios'

import App from './App.vue'
import Home from './components/Home/index.vue'
import HomePage from './components/Home/HomePage.vue'
import Login from './components/Login/index.vue'

import './index.css'

const routes = [
    { path: '/', component: Home, children: [
        {
            path: '/',
            component: HomePage,
        }
    ] },
    { path: '/login', component: Login },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

const app = createApp(App)
app.use(router)
app.config.globalProperties.$axios = {...axios}
app.mount('#app')