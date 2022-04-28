import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import { useStore } from '../stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/error']

    const store = useStore()

    const authRequired = !publicPages.includes(to.path)
    const loggedIn = store.token !== ''
    
    if (authRequired && !loggedIn) {
        return next('/login');
    }    
    next();
})

export default router