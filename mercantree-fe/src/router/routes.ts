import MtApp from '../components/MtApp.vue'
import MtModelPage from '../components/MtModelPage.vue'
import HomePage from '../components/Home/HomePage.vue'
import Login from '../components/Login/index.vue'

const routes = [
    { path: '/', component: MtApp, children: [
        {
            path: '/',
            component: HomePage,
        },
        { 
            path: '/products',
            component: MtModelPage,
            name: 'Produtos',
            children: [
            {
                path: '',
                name: 'Listar',
                component: () => import('../components/Products/ProductsPage.vue'),
            },
            {
                path: 'create',
                name: 'Criar',
                component: () => import('../components/Products/ProductCreatePage.vue'),
            },
            {
                path: 'product/:id',
                name: 'Alterar produto',
                component: () => import('../components/Products/ProductViewPage.vue'),
            },
        ] },
    ] },
    { path: '/login', component: Login },
]

export default routes