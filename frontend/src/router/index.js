import Vue from 'vue'
import Router from 'vue-router'
import NotFound from '@/components/NotFound'
import GamePanel from '@/components/GamePanel'
import Board from '@/components/Board'
import Piece from '@/components/Piece'
import Space from '@/components/Space'
import Winner from '@/components/Winner'

const routerOptions = [
  { path: '*', name: '404', component: NotFound },
  { path: '/', name: 'GamePanel', component: GamePanel },
  { path: '/', name: 'Board', component: Board },
  { path: '/', name: 'Piece', component: Piece },
  { path: '/', name: 'Space', component: Space },
  { path: '/', name: 'Winner', component: Winner }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: route.component
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
