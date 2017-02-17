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
      <div class="item" v-for="(tot, i) in result.article_count">檔案 {{ i }}: {{ tot }} 筆</div>
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
          <td v-for="(d, j) in row" v-if="j < i">{{ d.length }}</td>
          <td v-else></td>
        </tr>
      </tbody>
    </table>
  </article>
  <article class="ui basic segment">
    <header class="ui dividing header">
      <h2>ID 交集</h2>
    </header>
    <div v-if="result.link">
      <a class="ui primary button"
        target="_blank" 
        v-if="result.link"
        :href="result.link">下載</a>
    </div>
    <div class="ui form">
      <div class="inline field">
        <label for="gap">計數條件</label>
        <input type="number" name="gap" min="0" :max="gapmax" v-model="gap" />
        <label for="gap">最大值: {{ gapmax }}</label>
      </div>
    </div>
    <table class="ui definition table" v-if="result.people">
      <thead>
        <th></th>
        <th v-for="(h, i) in tableheader" :data-tooltip="result.list[ h[0] ][0]">{{ i }}</th>
      </thead>
      <tbody>
        <tr v-for="(row, i) in tablebody">
          <td :data-tooltip="result.list[ tableheader[i][0] ][0]">{{ i }}</td>
          <td v-for="d in row">{{ d }}</td>
        </tr>
      </tbody>
    </table>
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
      link:  '',
      link2: '',
      datarows: [],
      result: {},
      gap: 0
    }
  },
  created() {
    this.addRow()
  },
  computed: {
    people() {
      const app = this
      return _.map(
        app.result.peo_list,
        (people, idx) => [people, idx])
    },
    gapmax() {
      const app = this
      if (app.result.list)
        return _.maxBy(app.result.list, people => people[1])[1]
      return 0
    },
    idlist() {
      const app = this
      return _.filter(
        app.people,
        obj => app.result.list[ obj[0] ][1] >= app.gap)
    },
    tableheader() {
      const app = this
      return _.take(app.idlist, 15)
    },
    tablebody() {
      const app = this
      let res = []
      for (let i = 0; i < app.tableheader.length; i++) {
        let tmp = []
        for (let j = 0; j < app.tableheader.length; j++) {
          tmp.push(app.result.people[ app.tableheader[i][1] ][ app.tableheader[j][1] ])
        }
        res.push(tmp)
      }
      return res
    }
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
      let app = this
      let formData = new FormData( $('#form')[0] )

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