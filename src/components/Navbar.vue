<template>
<nav id="navbar" class="ui menu">
  <router-link v-for="route in routes" :to="route.path" class="item">
  {{ route.name }}
  </router-link>
</nav>
</template>

<script>
const routes = require('../routes')

export default {
  name: 'menu',
  data() {
    return {
      routes: routes
    }
  }
}
</script>

<style>
#navbar {
  margin-bottom: 3rem;
}
</style>