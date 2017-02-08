<template>
<section id="onepage">
  <header class="ui header">
    <h1>單頁資料擷取</h1>
  </header>
  <article class="ui basic segment">
    <header class="ui dividing header">
      <h2>單頁連結</h2>
    </header>
    <form class="ui equal width form">
    <div class="fields">
      <div class="field">
        <label for="token">Token</label>
        <input type="text" name="token"
          :value="appdata.store.token"
          @input="$emit('setToken', $event.target.value)" />
        <label for="token">
          <a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取 token</a>
        </label>
      </div>
      <div class="field">
        <label for="url">文章連結</label>
        <input type="text" name="url" v-model="url" />
      </div>
    </div>
    <div class="field">
      <button type="submit" class="ui primary button"
        @click.prevent="recordSubmit">送出</button>
      <button type="reset"  class="ui button">清除</button>
    </div>
    </form>
  </article>
  <div class="ui basic segment">{{ { token: token, url: url } }}</div>
  <article v-if="records.length">
    <header class="ui dividing header">
      <h2>擷取紀錄</h2>
    </header>
    <record :appdata="appdata"></record>
  </article>
</section>
</template>

<script>
import Record from './Record'

export default {
  name: 'onepage',
  props: [ 'appdata' ],
  components: { Record },
  data() {
    return {
      url: ''
    }
  },
  computed: {
    token()   { return this.appdata.store.token  },
    records() { return this.appdata.records.data }
  },
  methods: {
    recordSubmit(e) {
      const app = this
      app.$emit('addRecord', app.url)
      app.url = ''
    }
  }
}
</script>