import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import Login from "../views/auth/Login.vue";

import Page401 from "../views/errors/Page401.vue";
import Page404 from "../views/errors/Page404.vue";
import Page500 from "../views/errors/Page500.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/401",
    component: Page401,
  },
  {
    path: "/404",
    component: Page404,
  },
  {
    path: "/500",
    component: Page500,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
