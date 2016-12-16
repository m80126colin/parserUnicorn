<template>
<div id="association">
  <form id="form" class="pure-form pure-form-aligned" method="post" enctype="multipart/form-data">
    <fieldset>
      <div v-for="(file, i) in files" :key="file.id" :data-tag="file.id" class="pure-control-group">
        <label :for="'file' + i">檔案 {{ i }}</label>
        <input :id="'file' + i" class="pure-input-1-2" type="file" :name="'file' + i" />
        <button v-on:click.prevent="delFile" :data-id="i" class="pure-button">刪除</button>
      </div>
    </fieldset>
    <div class="pure-controls">
      <button v-on:click.prevent="addFile" class="pure-button">新增</button>
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
      ]
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
    }
  }
}
</script>