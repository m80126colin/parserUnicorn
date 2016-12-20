<template>
<div id="association">
  <form id="form" class="pure-form pure-form-aligned" method="post" enctype="multipart/form-data">
    <fieldset>
      <div v-for="(file, i) in files" :key="file.id" :data-tag="file.id" class="pure-control-group">
        <label :for="'file' + i">檔案 {{ i }}</label>
        <input :id="'file' + i" class="pure-input-1-2" type="file" :name="'file' + i" />
        <button @click.prevent="delFile" :data-id="i" class="pure-button">刪除</button>
      </div>
    </fieldset>
    <div class="pure-controls">
      <button @click.prevent="addFile" class="pure-button">新增</button>
      <button @click.prevent="associHandler" class="pure-button pure-button-primary">送出</button>
    </div>
    <div id="result">
      <div id="apriori" v-if="link">
        <a class="pure-button" target="_blank" :href="link">下載關聯矩陣</a>
      </div>
      <div id="apriori" v-if="link2">
        <a class="pure-button" target="_blank" :href="link2">下載關聯規則</a>
      </div>
      <table v-if="result.length" class="pure-table pure-table-bordered">
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
  </form>
</div>
</template>

<script>
import $ from 'jquery'

let cnt = 1

export default {
  data() {
    return {
      files: [
        { id: 0 }
      ],
      link:  '',
      link2: '',
      result: []
    }
  },
  name: 'association',
  methods: {
    addFile(e) {
      let app = this
      app.files.push({ id: cnt })
      cnt++
    },
    delFile(e) {
      let app = this
      const id = $(e.target).attr('data-id')
      app.files.splice(id, 1)
    },
    associHandler(e) {
      let app = this
      let formData = new FormData( $('#form')[0] )

      $.ajax({
        type:        'POST',
        url:         '/api/associ',
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