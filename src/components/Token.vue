<template>
<div class="field">
  <label for="token">Token</label>
  <input type="text" id="token"
    :value="appdata.store.token" 
    @input="$root.$emit('set_token', $event.target.value)"/>
  <label for="token">
    <a target="_blank" href="https://developers.facebook.com/tools/explorer/">到此領取 token</a>
  </label>
</div>
</template>

<script>
export default {
  name: 'token',
  props: [ 'appdata' ]
}
</script>