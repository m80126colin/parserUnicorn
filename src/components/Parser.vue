<template>
<section id="parser">
  <header class="ui header">
    <h1>資料蒐集</h1>
  </header>
  <article class="ui basic segment">
    <header class="ui dividing header">
      <h2>粉絲專頁</h2>
    </header>
    <form id="form" class="ui equal width form">
      <div class="fields">
        <token :appdata="appdata"></token>
        <div class="field">
          <label for="url">粉絲專頁連結</label>
          <input type="text" name="url" v-model="req.url">
        </div>
        <div class="field">
          <label for="since">開始時間</label>
          <input type="date" name="since" v-model="req.since">
        </div>
        <div class="field">
          <label for="until">結束時間</label>
          <input type="date" name="until" v-model="req.until">
        </div>
      </div>
      <div class="field">
        <button class="ui primary button"
          @click.prevent="getAllPosts">送出</button>
      </div>
    </form>
    <div v-if="result.length" class="ui basic segment">
      <p>共有 {{ result.length }} 筆結果。</p>
    </div>
    <table v-if="result.length" class="ui table">
    <thead>
      <tr>
      <th v-for="h in header">{{ h }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, i) in result" :key="i">
        <td>{{ i }}</td>
        <td>{{ row.time }}</td>
        <td>{{ row.count.shares }}</td>
        <td>{{ row.count.likes }}</td>
        <td>{{ row.count.comments }}</td>
        <td>
          <a class="ui button" target="_blank"
            :href="facebookLink(row.id)">連結</a>
          <button class="ui primary button parser-download"
            :data-id="row.id" @click="downloadListener">下載</button>
        </td>
      </tr>
    </tbody>
    </table>
  </article>
</section>
</template>

<script>
import Token from './Token'

import _ from 'lodash'
import $ from 'jquery'
import moment from 'moment'

const header = ['#', '貼文時間', '分享數', '按讚數', '留言數', '操作']

export default {
  name: 'parser',
  props: [ 'appdata' ],
  components: { Token },
  data() {
    return {
      header: header,
      fetch:  false,
      result: [],
      req: {
        url:   '',
        since: '',
        until: ''
      }
    }
  },
  methods: {
    clearRequest() {
      const app = this
      app.req.url   = ''
      app.req.since = ''
      app.req.until = ''
    },
    getAllPosts(e) {
      const app  = this
      const data = _.assign({ token: app.appdata.store.token }, app.req)
      // send POST /allposts request
      $.ajax({
        type:        'POST',
        url:         '/api/allposts',
        data:        JSON.stringify(data),
        contentType: 'application/json',
        dataType:    'json'
      })
      .done(res => {
        app.result = _(res)
          .map(row => {
            return {
              id:    row.id,
              time:  moment(row.created_time).format('YYYY/MM/DD HH:mm:ss ZZ'),
              count: {
                likes:    row.likes.summary.total_count,
                comments: row.comments.summary.total_count,
                shares:   row.shares ? row.shares.count : 0
              }
            }
          })
          .value()
      })
      // reset req
      app.clearRequest()
    },
    facebookLink(id) {
      return `https://www.facebook.com/${id}`
    },
    downloadListener(e) {
      var nodeId   = $(e.target).attr('data-id')
      var endpoint = '/api/allcomments/' + nodeId + '?token=' + $('#token').val()

      // send GET /allcomments/<nodeId> request
      window.open(endpoint, '_blank')
    }
  }
}
</script>

<style>
#parser {
  text-align: left;
}
</style>