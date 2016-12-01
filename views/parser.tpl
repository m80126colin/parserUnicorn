<link rel="stylesheet" href="/public/pure-min.css">
<div class="pure-g">
  <div class="pure-u-1-6"></div>
  <div class="pure-u-2-3">
    <form id="form" class="pure-form pure-form-aligned">
      <fieldset>
        <div class="pure-control-group">
          <label for="token">Token</label>
          <input type="text" id="token" placeholder="... token">
          <a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取</a>
        </div>
        <div class="pure-control-group">
          <label for="url">粉絲專頁連結</label>
          <input type="text" id="url" placeholder="... url">
        </div>
        <div class="pure-control-group">
          <label for="since">開始時間</label>
          <input type="date" id="since">
        </div>
        <div class="pure-control-group">
          <label for="until">結束時間</label>
          <input type="date" id="until">
        </div>
        <div class="pure-controls">
          <button type="submit" class="pure-button pure-button-primary">送出</button>
        </div>
      </fieldset>
    </form>
    <div id="result"></div>
  </div>
  <div class="pure-u-1-6"></div>
</div>
<script src="/public/jquery.min.js"></script>
<script src="/public/index.js"></script>
<script src="/public/parser.js"></script>