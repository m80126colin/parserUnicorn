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
import _      from 'lodash'
import Navbar from './components/Navbar'

require('semantic-ui-css/semantic.css')
require('semantic-ui-css/semantic.js')

let counter = {
  record: 0
}

window._ = _

const postJson = (url, data) => {
  return $.ajax({
    type:        'POST',
    url:         url,
    data:        JSON.stringify(data),
    contentType: 'application/json',
    dataType:    'json'
  })
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
      const app = this
      const api = [
        '/api/post/id',
        '/api/post/likes',
        '/api/post/likes',
        '/api/post/likes'
      ]
      // make record
      let req = {
        id:  counter.record ++,
        submits: [
          { state: 0, result: {} }, // /post/id    request
          { state: 0, result: {} }, // /post/likes request
          { state: 0, result: {} },
          { state: 0, result: {} }
        ]
      }
      app.records.data = _.concat(req, app.records.data)
      // send requests
      const configs = _.zip(api, req.submits)
      const first   = _.head(configs)
      postJson(first[0], {
        token: app.store.token,
        url:   url
      })
      .done(res => {
        _.assign(first[1], { state: 1, result: res })
        _(configs)
        .tail()
        .forEach(cfg => {
          postJson(cfg[0], {
            token:  app.store.token,
            postid: res.postid
          })
          .done(data => {
            _.assign(cfg[1], { state: 1, result: data })
          })
        })
      })
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
