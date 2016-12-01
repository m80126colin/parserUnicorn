<link rel="stylesheet" href="/public/pure-min.css">
<div class="pure-g">
  <div class="pure-u-1-6"></div>
  <div class="pure-u-2-3">
    <form id="form" method="post" enctype="multipart/form-data" class="pure-form pure-form-stacked">
      <fieldset>
        <input class="pure-input-1" id="data" type="file" name="data" />
        <button type="submit" class="pure-button pure-button-primary">上傳</button>
      </fieldset>
    </form>
    <p>
      <canvas id="cloud" style="width: 100%"></canvas>
    </p>
  </div>
  <div class="pure-u-1-6"></div>
</div>
<script src="/public/wordcloud2.js"></script>
<script src="/public/jquery.min.js"></script>
<script>
  WordCloud(document.getElementById('cloud'), {
    list:       {{!list}},
    color:      'random-dark',
    fontWeight: 'normal'
  })
</script>