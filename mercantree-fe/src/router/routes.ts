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
            path: '/sell',
            component: MtModelPage,
            name: 'Vendas',
            children: [
                {
                    path: '',
                    name: 'Listar vendas',
                    component: () => import('../components/Sell/SellPage.vue'),
                },
                {
                    path: 'create',
                    name: 'Criar venda',
                    component: () => import('../components/Sell/SellCreatePage.vue'),
                },
            ] 
        },
        { 
            path: '/products',
            component: MtModelPage,
            name: 'Produtos',
            children: [
                {
                    path: '',
                    name: 'Listar produto',
                    component: () => import('../components/Products/ProductsPage.vue'),
                },
                {
                    path: 'create',
                    name: 'Criar produto',
                    component: () => import('../components/Products/ProductCreatePage.vue'),
                },
                {
                    path: 'product/:id',
                    name: 'Alterar produto',
                    component: () => import('../components/Products/ProductViewPage.vue'),
                },
            ] 
        },
        { 
            path: '/suppliers',
            component: MtModelPage,
            name: 'Fornecedores',
            children: [
                {
                    path: '',
                    name: 'Listar fornecedor',
                    component: () => import('../components/Suppliers/SuppliersPage.vue'),
                },
                {
                    path: 'create',
                    name: 'Criar fornecedor',
                    component: () => import('../components/Suppliers/SupplierCreatePage.vue'),
                },
                {
                    path: 'supplier/:id',
                    name: 'Alterar fornecedor',
                    component: () => import('../components/Suppliers/SupplierViewPage.vue'),
                },
            ] 
        },
    ] },
    { path: '/login', component: Login },
]

export default routes