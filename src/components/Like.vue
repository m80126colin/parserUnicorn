<template>
<section id="like" class="pure-form">
<header><h1>按讚分析</h1></header>
  <div class="pure-control-group">
    <label for="token">Token</label>
    <input id="token" type="text" v-model="token">
    <span><a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取</a></span>
  </div>
  <table class="pure-table pure-table-horizontal">
  <thead>
    <tr>
      <th>#</th>
      <th>連結</th>
      <th>狀態</th>
      <th>按讚數</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(row, idx) in datarows" :key="row.id" :data-tag="row.id">
      <td>連結 {{ idx }}</td>
      <td>
        <input type="text" v-model="row.url"
          @input="likesHandler" :data-id="idx"
          :id="`row${idx}`" :name="`row${idx}`">
      </td>
      <td>{{ row.result.state | showState }}</td>
      <td>{{ row.result.likes | countLength }}</td>
      <td>
        <button class="pure-button pure-button-primary"
          v-if="row.result.state === 0"
          @click="downloadData" :data-id="idx">下載</button>
        <button class="pure-button"
          v-if="row.result.state === 0"
          @click="facebookLink" :data-id="idx">文章連結</button>
        <button class="pure-button"
          @click="deleteRow"    :data-id="idx">刪除</button>
      </td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
    <td colspan="5" class="pure-controls">
      <button class="pure-button pure-button-primary"
        @click="">全部送出</button>
      <button class="pure-button"
        @click="addRow">新增</button>
    </td>
    </tr>
  </tfoot>
  </table>
</section>
</template>

<script>
import _ from 'lodash'
import $ from 'jquery'

let counter = 0

window.$ = window.jQuery = $

export default {
  name: 'like',
  data() {
    return {
      token: '',
      datarows: []
    }
  },
  created() {
    this.addRow()
  },
  filters: {
    showState(state) {
      if (state === -1) return '初始化'
      if (state === 1 ) return '處理中'
      if (state === 2 ) return '處理錯誤'
      return '處理完成'
    },
    countLength(arr) {
      if (arr) return arr.length
      return ''
    }
  },
  methods: {
    addRow(e) {
      this.datarows.push({
        id:  counter,
        url: '',
        result: {
          state: -1,
          id: ''
        }
      })
      counter++
    },
    deleteRow(e) {
      const idx = $(e.target).attr('data-id')
      this.datarows.splice(idx, 1)
    },
    likesHandler(e) {
      let app   = this
      const idx = $(e.target).attr('data-id')
      let row   = app.datarows[idx]
      // init
      _.assign(row.result, { state: 1 })
      // send request
      return $.ajax({
        type:        'POST',
        url:         '/api/likes',
        data:        JSON.stringify({
          token: app.token,
          url:   row.url
        }),
        contentType: 'application/json',
        dataType:    'json'
      })
      .done(res => {
        _.assign(row.result, res)
        _.assign(row.result, { state: 0 })
      })
      .fail(xhr => {
        _.assign(row.result, { state: 2 })
      })
    },
    downloadData(e) {
      const idx      = $(e.target).attr('id')
      const result   = this.datarows[idx].result
      const endpoint = `/downloads/${result.link}`
      window.open(endpoint, '_blank')
    },
    facebookLink(e) {
      const idx      = $(e.target).attr('id')
      const result   = this.datarows[idx].result
      const endpoint = `https://www.facebook.com/${result.id}`
      window.open(endpoint, '_blank')
    }
  }
}
</script>