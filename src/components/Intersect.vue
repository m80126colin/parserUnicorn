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
  <div id="result" class="ui basic segment">
    <div id="apriori" v-if="link">
      <a class="ui button" target="_blank" :href="link">下載關聯矩陣</a>
    </div>
    <div id="apriori" v-if="link2">
      <a class="ui button" target="_blank" :href="link2">下載關聯規則</a>
    </div>
    <table v-if="result.length" class="ui table">
    <thead>
      <tr>
        <th>Rules</th>
        <th>Support</th>
        <th>Confident</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in result">
        <td>{{ row.itema }} => {{ row.itemb }}</td>
        <td>{{ row.support }}</td>
        <td>{{ row.confident }}</td>
      </tr>
    </tbody>
    </table>
  </div>
</section>
</template>

<script>
import $ from 'jquery'

let cnt = 1
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
      result: []
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
        app.link   = data.link
        app.link2  = data.link2
        app.result = JSON.parse(data.list)
      })
    }
  }
}
</script>