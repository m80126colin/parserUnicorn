<template>
<div class="cloud">
  <form id="form" v-on:submit.prevent="cloudHandler" class="pure-form pure-form-stacked" method="post" enctype="multipart/form-data">
    <fieldset>
      <input class="pure-input-1" id="data" type="file" name="data" />
      <button type="submit" class="pure-button pure-button-primary">上傳</button>
    </fieldset>
  </form>
  <div id="count" v-if="link">
    <a class="pure-button" target="_blank" :href="link">下載</a>
  </div>
  <textarea id="dd" cols="30" rows="10" v-model="will"></textarea>
  <div id="rr">
    <table v-if="wont.length" class="pure-table pure-table-bordered">
    <tbody>
      <tr v-for="row in wont">
        <td v-for="ele in row">{{ ele }}</td>
      </tr>
    </tbody>
    </table>
  </div>
  <button v-on:click.prevent="visualizeData" class="pure-button pure-button-primary">GO</button>
  <div class="canvas-container">
    <canvas id="cloud" width="1024" height="768"></canvas>
  </div>
</div>
</template>

<script>
import $ from 'jquery'
import WordCloud from 'WordCloud'

const drawCanvas = list => {
  list.sort((left, right) => - (left[1] - right[1]))
  
  let sublist = list.filter((it, i) => i < 5000)

  const sum = (a, b) => a + b
  const dif = b => { return a => a - b }
  const sqr = a => a * a

  let dat = sublist.map(item => parseInt(item[1]))
  let avg = dat.reduce(sum) / dat.length
  let sig = Math.sqrt(dat.map(dif(avg)).map(sqr).reduce(sum)) / dat.length

  console.log(dat, avg, sig)

  const standard = x => (sig === 0) ? 0 : (x - avg) / sig

  let factor = $('#cloud').width() / 1024

  WordCloud(document.getElementById('cloud'), {
    list: sublist,
    // color:      'random-dark',
    // fontWeight: 'normal',
    fontFamily: 'Times, serif',
    rotateRatio: 0.5,
    gridSize: Math.round(16 * factor),
    weightFactor: size => factor * (standard(size) + 28)
  })
}

export default {
  data() {
    return {
      link: '',
      will: ''
    }
  },
  name: 'cloud',
  computed: {
    wont() {
      return this.will.trim().split('\n')
             .map(str => str.trim().split(/\s+/))
    }
  },
  methods: {
    cloudHandler(e) {
      let app = this
      let formData = new FormData( $('#form')[0] )

      $.ajax({
        type:        'POST',
        url:         '/api/cloud',
        data:        formData,
        processData: false,
        contentType: false
      })
      .done(data => {
        app.link = data.link
        let list = JSON.parse(data.list)
        drawCanvas(list)
      })
    },
    visualizeData(e) {
      drawCanvas(this.wont)
    }
  }
}
</script>