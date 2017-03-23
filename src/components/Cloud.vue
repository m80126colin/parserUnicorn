<template>
<section id="cloud" class="cloud">
  <form id="form" class="ui form" method="post" enctype="multipart/form-data" @submit.prevent="cloudHandler">
    <div class="inline field">
      <input type="file" name="data" />
      <button type="submit" class="ui primary button">上傳</button>
    </div>
  </form>
  <div v-if="link" class="ui basic segment">
    <a class="ui button" target="_blank" :href="link">下載</a>
  </div>
  <!--
  <div class="ui basic segment canvas-container">
    <canvas :width="width" :height="height"></canvas>
  </div>
  -->
</section>
</template>

<script>
import _ from 'lodash'
import $ from 'jquery'
import stat from 'simple-statistics'
import WordCloud from 'WordCloud'
import uni from '../scripts'

window.stat = stat

export default {
  name: 'cloud',
  data() {
    return {
      width: 1000,
      link: '',
      will: '',
      cloudData: []
    }
  },
  computed: {
    height() {
      return Math.floor(this.width * 0.75)
    },
    wont() {
      return (this.will || '').trim().split('\n')
             .map(str => str.trim().split(/\s+/))
    }
  },
  watch: {
    cloudData(newData) {
      /*
      if (!Array.isArray(newData) || newData.length === 0)
        return

      const app   = this
      const LIMIT = 10000

      const list = _
        .chain(newData)
        .map(item => {
          if (typeof item[1] !== 'number')
            item[1] = 0
          return item
        })
        .sort((a, b) => b[1] - a[1])
        .take(LIMIT)
        .value()


      const data   = _.map(list, item => item[1])
      const mean   = stat.mean(data)
      const stdDev = stat.standardDeviation(data)

      const factor = $('#cloud').width() / app.width
      const zScore = x => stat.zScore(x, mean, stdDev) || 0

      const range = zScore(stat.max(data))

      WordCloud(document.getElementById('cloud'), {
        list: list,
        // color:      'random-dark',
        // fontWeight: 'normal',
        fontFamily: 'Times, serif, 標楷體',
        rotateRatio: 0.5,
        gridSize: Math.round(6 * factor),
        weightFactor: size => 12 * factor * (7 * zScore(size) / range + 0.75)
      })
      */
    }
  },
  methods: {
    cloudHandler(e) {
      const app      = this
      const formData = new FormData( $('#form')[0] )

      uni.$postForm('/api/cloud', formData)
        .done(data => {
          window.console.log(data)
          const res = JSON.parse(data.list)
          app.link      = data.link
          app.cloudData = res
        })
    },
    visualizeData(e) {
      let app = this
      app.cloudData = _.map(app.wont, item => [item[0], parseInt(item[1]) || 0])
    }
  }
}
</script>