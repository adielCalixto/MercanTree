import Home from '../components/Home/index.vue'
import HomePage from '../components/Home/HomePage.vue'
import Login from '../components/Login/index.vue'

const routes = [
    { path: '/', component: Home, children: [
        {
            path: '/',
            component: HomePage,
        }
    ] },
    { path: '/login', component: Login },
]

export default routes