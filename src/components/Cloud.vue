<template>
<div class="cloud">
  <form id="form" v-on:submit.prevent="cloudHandler" method="post" enctype="multipart/form-data" class="pure-form pure-form-stacked">
    <fieldset>
      <input class="pure-input-1" id="data" type="file" name="data" />
      <button type="submit" class="pure-button pure-button-primary">上傳</button>
    </fieldset>
  </form>
  <div id="count" v-if="link">
    <a class="pure-button" target="_blank" :href="link">下載</a>
  </div>
  <div class="canvas-container">
    <canvas id="cloud" width="800" height="600"></canvas>
  </div>
</div>
</template>

<script>
import $ from 'jquery'
import WordCloud from 'WordCloud'

export default {
  data() {
    return {
      link: ''
    }
  },
  name: 'cloud',
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

        list.sort((left, right) => - (left[1] - right[1]))
        
        let sublist = list.filter((item, i) => i < 300)
        let factor = $('#cloud').width() / 1024

        WordCloud(document.getElementById('cloud'), {
          list: sublist,
          // gridSize: 18,
          // weightFactor: 3,
          // color:      'random-dark',
          // fontWeight: 'normal',
          fontFamily: 'Times, serif',
          rotateRatio: 0.5,
          gridSize: Math.round(16 * factor),
          weightFactor: function (size) { return size * 3 * factor }
        })
      })
    }
  }
}
</script>