import Parser      from './components/Parser'
import Onepage     from './components/Onepage'
import Cloud       from './components/Cloud'
import Association from './components/Association'
import Intersect   from './components/Intersect'
import Like        from './components/Like'

const Index = { template: '<div></div>' }

module.exports = [
  { path: '/',            name: '首頁',         component: Index       },
  { path: '/parser',      name: '資料蒐集',     component: Parser      },
  { path: '/onepage',     name: '單頁資料擷取', component: Onepage     },
  { path: '/cloud',       name: '文字雲',       component: Cloud       },
  { path: '/association', name: '關聯分析',     component: Association },
  { path: '/intersect',   name: '交集分析',     component: Intersect   }
]