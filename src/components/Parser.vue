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
        <div v-for="field in fields" class="field">
          <label :for="field.id">{{ field.name }}</label>
          <input :type="field.type" :id="field.id">
          <label :for="field.id" v-if="'after' in field" v-html="field.after"></label>
        </div>
      </div>
      <div class="field">
        <button class="ui primary button"
          @click.prevent="getAllPosts">送出</button>
      </div>
    </form>
    <div id="msg" v-if="fetch" class="ui basic segment">
      <p>共有 {{ result.length }} 筆結果。</p>
    </div>
    <table id="result" v-if="result.length" class="ui table">
    <thead>
      <tr>
        <th>#</th>
        <th>id</th>
        <th>create time</th>
        <th>like count</th>
        <th>comment count</th>
        <th>share count</th>
        <th>Link</th>
        <th>Download</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, i) in result" :key="i">
        <td>{{ i }}</td>
        <td>{{ row.id }}</td>
        <td>{{ getTime(row.created_time) }}</td>
        <td>{{ row.likes.summary.total_count }}</td>
        <td>{{ row.comments.summary.total_count }}</td>
        <td>{{ row.shares.count }}</td>
        <td>
          <a class="ui button" target="_blank"
            :href="`https://www.facebook.com/${row.id}`">連結</a>
        </td>
        <td>
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
import $ from 'jquery'
import moment from 'moment'

const fields = [
  { id: 'token', type: 'text', name: 'Token', after: '<a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取 token</a>' },
  { id: 'url',   type: 'text', name: '粉絲專頁連結' },
  { id: 'since', type: 'date', name: '開始時間' },
  { id: 'until', type: 'date', name: '結束時間' }
]

export default {
  name: 'parser',
  props: [ 'appdata' ],
  data() {
    return {
      fields: fields,
      fetch:  false,
      result: []
    }
  },
  methods: {
    getTime(str) {
      return moment(str).format('YYYY/MM/DD HH:mm:ss ZZ')
    },
    getAllPosts(e) {
      let app = this
      // retrieve form data
      var keys = fields.map(item => item.id)
      var data = {}
      keys.forEach(key => {
        data[key] = $('#' + key).val()
      })
      // send POST /allposts request
      $.ajax({
        type:        'POST',
        url:         '/api/allposts',
        data:        JSON.stringify(data),
        contentType: 'application/json',
        dataType:    'json'
      })
      .done(res => {
        app.fetch  = true
        app.result = res
      })
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