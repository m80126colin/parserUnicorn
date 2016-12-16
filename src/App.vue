<template>
<div id="app">
  <div class="pure-g">
    <div class="pure-u-1-6"></div>
    <div class="pure-u-2-3">
      <navbar></navbar>
      <router-view></router-view>
    </div>
    <div class="pure-u-1-6"></div>
  </div>
</div>
</template>

<script>
import pure from './assets/pure-min.css'
import Navbar from './components/Navbar'

export default {
  name: 'app',
  components: { Navbar }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
