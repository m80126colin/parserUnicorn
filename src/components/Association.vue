<template>
<section id="association">
  <form id="form" class="ui form" method="post" enctype="multipart/form-data">
    <div v-for="(file, i) in files" :key="file.id" :data-tag="file.id" class="inline field">
      <label :for="'file' + i">檔案 {{ i }}</label>
      <input :id="'file' + i" class="pure-input-1-2" type="file" :name="'file' + i" />
      <button class="ui button"
        @click.prevent="delFile" :data-id="i">刪除</button>
    </div>
    <div class="field">
      <button class="ui button" @click.prevent="addFile">新增</button>
      <button class="ui primary button" @click.prevent="associHandler">送出</button>
    </div>
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
  </form>
</section>
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