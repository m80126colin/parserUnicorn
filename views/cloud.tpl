<link rel="stylesheet" href="/public/pure-min.css">
<div class="pure-g">
  <div class="pure-u-1-6"></div>
  <div class="pure-u-2-3">
    <form class="pure-form">
      <input class="pure-input-1" id="data" type="text" name="data" />
      <button type="submit" class="pure-button pure-button-primary">送出</button>
    </form>
    <p>
      <canvas id="cloud" style="width: 100%"></canvas>
    </p>
  </div>
  <div class="pure-u-1-6"></div>
</div>
<script src="/public/wordcloud2.js"></script>
<script src="/public/jquery.min.js"></script>
<script src="/public/index.js"></script>
<script>
  $('#submit').click(function (e) {
    var data = $('#data').val()
    sendJSON('/cloud', JSON.parse(data), 'POST')
    .done(function(res) {
      console.log(res)
      WordCloud(document.getElementById('cloud'), {
        list:       res,
        color:      'random-dark',
        fontWeight: 'normal'
      })
    })
  })
</script>