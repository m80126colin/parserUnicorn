<template>
<nav id="navbar" class="pure-menu pure-menu-horizontal">
<ul class="pure-menu-list">
  <li v-for="route in routes" class="pure-menu-item">
    <router-link :to="route.path" class="pure-menu-link">
    {{ route.name }}
    </router-link>
  </li>
</ul>
</nav>
</template>

<script>
const routes = require('../routes')

export default {
  name: 'navbar',
  data() {
    return {
      routes: routes
    }
  }
}
</script>

<style>
#navbar {
  height: 3rem;
}
</style>