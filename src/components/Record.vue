<template>
<table class="ui celled table">
  <thead>
    <tr><th v-for="h in header">{{ h }}</th></tr>
  </thead>
  <tbody>
    <tr v-for="r in records[page]">
      <td>{{ r.id }}</td>
      <td>{{ r.url }}</td>
      <td v-for="s in r.submits">{{ s.state }}</td>
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
    toPage(e) {
      const app = this
      app.page  = $(e.target).data('id')
    }
  }
}
</script>