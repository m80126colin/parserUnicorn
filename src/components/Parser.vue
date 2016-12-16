<template>
<div id="parser">
  <form id="form" class="pure-form pure-form-aligned">
  <fieldset>
    <div v-for="field in fields" class="pure-control-group">
      <label :for="field.id">{{ field.name }}</label>
      <input :type="field.type" :id="field.id">
      <span v-if="'after' in field" v-html="field.after"></span>
    </div>
    <div class="pure-controls">
      <button v-on:click="getAllPosts" class="pure-button pure-button-primary">送出</button>
    </div>
  </fieldset>
  </form>
  <div id="msg" v-if="fetch">
    <p>共有 {{ result.length }} 筆結果。</p>
  </div>
  <table id="result" v-if="result.length" class="pure-table pure-table-bordered">
  <thead>
    <tr>
      <th>#</th>
      <th v-for="key in Object.keys(result[0])">{{ key }}</th>
      <th>Link</th>
      <th>Download</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(row, i) in result" :key="i">
      <td>{{ i }}</td>
      <td v-for="item in Object.values(row)">{{ item }}</td>
      <td><a class="pure-button" target="_blank" :href="'https://www.facebook.com/' + row.id">連結</a></td>
      <td><button class="pure-button pure-button-primary parser-download" :data-id="row.id" v-on:click="downloadListener">下載</button></td>
    </tr>
  </tbody>
  </table>
</div>
</template>

<script>
import $ from 'jquery'

const fields = [
  { id: 'token', type: 'text', name: 'Token', after: '<a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取</a>' },
  { id: 'url',   type: 'text', name: '粉絲專頁連結' },
  { id: 'since', type: 'date', name: '開始時間' },
  { id: 'until', type: 'date', name: '結束時間' }
]

export default {
  data() {
    return {
      fields: fields,
      fetch:  false,
      result: []
    }
  },
  name: 'parser',
  methods: {
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