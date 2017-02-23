<template>
<section id="intersect">
  <form id="form" class="ui form" method="post" enctype="multipart/form-data">
    <div class="inline field" v-for="(row, idx) in datarows" :key="row.id" :data-tag="row.id">
      <label :for="`row${idx}`">檔案 {{ idx }}</label>
      <input :id="`row${idx}`" type="file" :name="`row${idx}`" />
      <button class="ui button"
        @click.prevent="deleteRow" :data-id="idx">刪除</button>
    </div>
    <div class="field">
      <button class="ui button"
        @click.prevent="addRow">新增</button>
      <button class="ui primary button"
        @click.prevent="intersectHandler">送出</button>
    </div>
  </form>
  <article class="ui basic segment" v-if="result.article">
    <header class="ui dividing header">
      <h2>文章交集</h2>
    </header>
    <h3 class="ui header">統計</h3>
    <div class="ui list">
      <div class="item" v-for="(tot, i) in result.count">檔案 {{ i }}: {{ tot }} 筆</div>
    </div>
    <h3 class="ui header">共同交集</h3>
    <table class="ui definition table">
      <thead>
        <tr>
          <th></th>
          <th v-for="(row, i) in result.article">檔案 {{ i }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in result.article">
          <td>檔案 {{ i }}</td>
          <td v-for="(d, j) in row" v-if="j < i">{{ d }}</td>
          <td v-else></td>
        </tr>
      </tbody>
    </table>
  </article>
  <article class="ui basic segment">
    <header class="ui dividing header">
      <h2>ID 交集</h2>
    </header>
    <div class="ui form">
      <div class="inline field">
        <label for="limit">篩選數量</label>
        <input type="number" min="1" v-model="limit" />
      </div>
    </div>
    <div v-if="result.link">
      <a class="ui primary button"
        target="_blank" 
        v-if="result.link"
        :href="result.link">下載矩陣</a>
      <a class="ui primary button"
        target="_blank" 
        v-if="result.link2"
        :href="result.link2">下載資料</a>
    </div>
  </article>
</section>
</template>

<script>
import _ from 'lodash'
import $ from 'jquery'

let counter = 0

export default {
  name: 'intersect',
  data() {
    return {
      files: [
        { id: 0 }
      ],
      datarows: [],
      result: {},
      limit: 100
    }
  },
  created() {
    this.addRow()
  },
  methods: {
    addRow(e) {
      this.datarows.push({ id: counter++ })
    },
    deleteRow(e) {
      const idx = $(e.target).attr('data-id')
      this.datarows.splice(idx, 1)
    },
    intersectHandler(e) {
      const app = this
      let formData = new FormData( $('#form')[0] )
      formData.set('limit', app.limit)

      $.ajax({
        type:        'POST',
        url:         '/api/intersect',
        data:        formData,
        processData: false,
        contentType: false
      })
      .done(data => {
        window.console.log(JSON.parse(data))
        app.result = JSON.parse(data)
      })
    }
  }
}
</script>