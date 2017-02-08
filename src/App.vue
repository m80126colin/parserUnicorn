<template>
<div id="app" class="ui centered grid">
  <div class="two wide column"></div>
  <div class="twelve wide column">
    <navbar></navbar>
    <router-view
      :appdata="$data"
      @addRecord="addRecord"
      @setRecordPageSize="setRecordPageSize"
      @setToken="setToken"></router-view>
  </div>
  <div class="two wide column"></div>
</div>
</template>

<script>
import Navbar from './components/Navbar'

require('semantic-ui-css/semantic.css')
require('semantic-ui-css/semantic.js')

let counter = {
  record: 0
}

export default {
  name: 'app',
  components: { Navbar },
  data() {
    return {
      store: {
        token: ''
      },
      records: {
        header: ['編號', '文章連結', '按讚數', '分享數', '留言數'],
        size:   10,
        data:   []
      }
    }
  },
  methods: {
    addRecord(url) {
      let app = this
      let req = {
        id:  counter.record ++,
        url: url,
        submits: [
          { state: 0, result: {} },
          { state: 0, result: {} },
          { state: 0, result: {} }
        ]
      }
      app.records.data = _.concat(req, app.records.data)
    },
    setRecordPageSize(num) {
      this.records.size = num
    },
    setToken(token) {
      this.store.token = token
    }
  }
}
</script>

<style>
#app {
  font-family: '微軟正黑體', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
