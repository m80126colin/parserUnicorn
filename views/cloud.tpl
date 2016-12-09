<link rel="stylesheet" href="/public/pure-min.css">
<div class="pure-g">
  <div class="pure-u-1-6"></div>
  <div class="pure-u-2-3">
    <div class="pure-menu pure-menu-horizontal" style="height: 3rem">
      <ul class="pure-menu-list">
        <li class="pure-menu-item">
          <a href="/" class="pure-menu-link">回首頁</a>
        </li>
        <li class="pure-menu-item">
          <a href="/parser" class="pure-menu-link">資料蒐集</a>
        </li>
      </ul>
    </div>
    <form id="form" method="post" enctype="multipart/form-data" class="pure-form pure-form-stacked">
      <fieldset>
        <input class="pure-input-1" id="data" type="file" name="data" />
        <button type="submit" class="pure-button pure-button-primary">上傳</button>
      </fieldset>
    </form>
    <div id="count"></div>
    <div class="canvas-container" style="width: 100%">
      <canvas id="cloud" width="800" height="600"></canvas>
    </div>
  </div>
  <div class="pure-u-1-6"></div>
</div>
<script src="/public/wordcloud2.js"></script>
<script src="/public/jquery.min.js"></script>
<script>
  var link = '{{link}}'
  var list = {{!list}}
</script>
<script src="/public/cloud.js"></script>