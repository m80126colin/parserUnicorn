<template>
<table class="ui celled definition table">
  <thead>
    <tr><th v-for="h in header">{{ h }}</th></tr>
  </thead>
  <tbody>
    <tr v-for="r in records[page]">
      <td>{{ r.id }}</td>
      <td v-if="r.post.state === 1">
        <a target="_blank" :href="facebookLink(r.post.result.postid)">
          {{ r.post.result.postid }}
        </a>
      <td v-else-if="r.post.state === -1" class="negative">失敗</td>
      <td v-else>
        <div class="ui loading basic segment"></div>
      </td>
      <td v-for="s in r.submits" v-if="s.state === 1">
        {{ s.result.count }}
        <a class="ui tiny primary button"
          target="_blank" 
          v-if="s.result.link"
          :href="downloadLink(s.result.link)">下載</a>
      </td>
      <td v-else-if="s.state === -1" class="negative">失敗</td>
      <td v-else>
        <div class="ui loading basic segment"></div>
      </td>
    </tr>
  </tbody>
  <tfoot>
  <tr>
    <th :colspan="header.length">
    <div class="ui right floated pagination menu">
      <a class="item"
        v-for="(p, idx) in records" :data-id="idx"
        @click="toPage">{{ idx + 1 }}</a>
    </div>
    </th>
  </tr>
  </tfoot>
</table>
</template>

<script>
import _ from 'lodash'
import $ from 'jquery'

export default {
  name: 'record',
  props: [ 'appdata' ],
  data() {
    return {
      page: 0
    }
  },
  computed: {
    records() {
      const rec = this.appdata.records
      return _.chunk(rec.data, rec.size)
    },
    header()  { return this.appdata.records.header }
  },
  methods: {
    facebookLink(postid) {
      return `https://www.facebook.com/${postid}`
    },
    downloadLink(link) {
      return `/api/download/${link}`
    },
    toPage(e) {
      const app = this
      app.page  = $(e.target).data('id')
    }
  }
}
</script>