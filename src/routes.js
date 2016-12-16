import Cloud       from './components/Cloud'
import Association from './components/Association'
import Parser      from './components/Parser'

const Index = { template: '<div></div>' }

module.exports = [
  { path: '/',            name: '首頁',     component: Index },
  { path: '/cloud',       name: '文字雲',   component: Cloud },
  { path: '/association', name: '關聯分析', component: Association },
  { path: '/parser',      name: '資料蒐集', component: Parser }
]