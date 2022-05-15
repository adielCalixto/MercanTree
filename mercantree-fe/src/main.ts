import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from './services/axios'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTruck, faUser, faHome, faCashRegister, faCog, faBook, faSearch, faDollar, faBars, faUserCheck, faAdd, faRemove, faExternalLink, faWarning, faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faAdd, faRemove, faExternalLink, faUser, faHome, faCashRegister, faCog, faBook, faSearch, faDollar, faTruck, faBars, faUserCheck, faWarning, faArrowLeft)

import App from './App.vue'
import './index.css'
import router from './router'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.config.globalProperties.$axios = {...axios}
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')