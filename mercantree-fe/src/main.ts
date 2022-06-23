import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from './boot/axios'
import vSelect from 'vue-select'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTruck, faUser, faHome, faCashRegister, faCog, faBook, faSearch, faDollar, faBars, faUserCheck, faAdd, faRemove, faExternalLink, faWarning, faArrowLeft, faCheck, faEdit, faTrash, faChartBar } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faAdd, faChartBar, faTrash, faRemove, faCheck, faExternalLink, faUser, faHome, faCashRegister, faCog, faBook, faSearch, faDollar, faTruck, faBars, faUserCheck, faWarning, faArrowLeft, faEdit)

import App from './App.vue'
import "vue-select/dist/vue-select.css"
import './index.css'
import router from './router'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.config.globalProperties.$axios = {...axios}
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('v-select', vSelect)
app.mount('#app')