import { createRouter, createWebHistory } from 'vue-router'
import VueFlow from '../views/VueFlow.vue'
import CreateTextGraph from '../views/CreateTextGraph.vue'
import CreateEmptyGraph from '../views/CreateEmptyGraph.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/create_text_graph'
  }, 
  {
    path: '/create_text_graph',
    name: 'CreateTextGraph',
    component: CreateTextGraph
  },
  {
    path: '/create_empty_graph',
    name: 'CreateEmptyGraph',
    component: CreateEmptyGraph
  },
  {
    path: '/agent_:id(\\d+)',
    component: VueFlow
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
