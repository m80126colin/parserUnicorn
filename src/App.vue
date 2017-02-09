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
        header: ['', '文章連結', '分享數', '按讚數', '留言數'],
        size:   10,
        data:   []
      }
    }
  },
  methods: {
    addRecord(url) {
      const app = this
      //
      const successState = (data) => {
        return { state: 1, result: data }
      }
      //
      const failState    = () => {
        return { state: -1 }
      }
      // make record
      let req = {
        id:   counter.record ++,
        post: { state: 0, result: {}, api: '/api/post/id'       },
        submits: [
              { state: 0, result: {}, api: '/api/post/shares'   },
              { state: 0, result: {}, api: '/api/post/likes'    },
              { state: 0, result: {}, api: '/api/post/comments' }
        ]
      }
      app.records.data = _.concat(req, app.records.data)
      // send requests
      postJson(req.post.api, {
        token: app.store.token,
        url:   url
      })
      .done(res => {
        _.assign(req.post, successState(res))
        _.forEach(req.submits, submit => {
          postJson(submit.api, {
            token:  app.store.token,
            postid: res.postid
          })
          .done(data => {
            _.assign(submit, successState(data))
          })
          .fail(xhr => {
            _.assign(submit, failState())
          })
        })
      })
      .fail(xhr => {
        _.assign(req.post, failState())
        _.forEach(req.submits, submit => {
          _.assign(submit, failState())
          window.console.log(submit.state)
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
