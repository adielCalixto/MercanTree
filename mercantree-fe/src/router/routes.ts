import MtApp from '../components/MtApp.vue'
import MtModelPage from '../components/MtModelPage.vue'
import HomePage from '../components/Home/HomePage.vue'
import ConfigPage from '../components/Config/ConfigPage.vue'
import Login from '../components/Login/index.vue'

const routes = [
    { path: '/', component: MtApp, redirect: '/home', children: [
        {
            path: '/home',
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
                {
                    path: 'order/:id',
                    name: 'Ver venda',
                    component: () => import('../components/Sell/SellViewPage.vue'),
                },
            ] 
        },
        { 
            path: '/stock',
            component: MtModelPage,
            name: 'Estoque',
            children: [
                {
                    path: '',
                    name: 'Listar Estoque',
                    component: () => import('../components/Products/StockProductsPage.vue'),
                },
                {
                    path: 'create',
                    name: 'Criar produto',
                    component: () => import('../components/Products/ProductCreatePage.vue'),
                },
                {
                    path: 'products',
                    name: 'Listar produtos',
                    component: () => import('../components/Products/ProductsPage.vue'),
                },
                {
                    path: 'products/product/:id',
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
        { 
            path: '/cashregister',
            component: MtModelPage,
            name: 'Caixa',
            redirect: '/cashregister',
            children: [
                {
                    path: '',
                    name: 'Caixa atual',
                    component: () => import('../components/CashRegister/CashRegPage.vue'),
                },
                {
                    path: 'closed',
                    name: 'Caixas fechados',
                    component: () => import('../components/CashRegister/CashRegsClosedPage.vue'),
                },
                {
                    path: 'open',
                    name: 'Abrir caixa',
                    component: () => import('../components/CashRegister/CashRegOpenPage.vue'),
                },
            ] 
        },
        { 
            path: '/config',
            component: ConfigPage,
            name: 'Configurações',
        },
    ] },
    { path: '/login', component: Login },
]

export default routes