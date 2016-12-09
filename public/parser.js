// tag snippet helper
var addTag = function (tag, item) {
  return ['<', tag, '>', item, '</', tag, '>'].join('')
}
var addTdTag = function (item) { return addTag('td', item) }
var addThTag = function (item) { return addTag('th', item) }
var addTrTag = function (item) { return addTag('tr', item) }

// download listener
var downloadListener = function (e) {
  var nodeId   = $(e.target).attr('data-id')
  var endpoint = '/allcomments/' + nodeId + '?token=' + $('#token').val()

  // send GET /allcomments/<nodeId> request
  window.open(endpoint, '_blank')
}

var makeHtml = function(res) {
  return []
    .concat('<table class="pure-table pure-table-bordered">')
    .concat('<thead><tr>')
    .concat(
      [].concat('#')
        .concat( Object.keys(res[0]) )
        .concat('Link')
        .concat('Download')
        .map(addThTag)
      .join('')
    )
    .concat('</tr></thead>')
    .concat('<tbody>')
    .concat(
      res.map(function (row, i) {
        return []
          .concat(i)
          .concat( Object.values(row) )
          .concat('<a class="pure-button" target="_blank" href="https://www.facebook.com/' + row.id + '">連結</a>')
          .concat('<button class="pure-button pure-button-primary parser-download" data-id="' + row.id + '"">下載</button>')
          .map(addTdTag)
        .join('')
      })
      .map(addTrTag)
      .join('')
    )
    .concat('</tbody>')
    .concat('</table>')
    .join('')
}

$('#form').submit(function (e) {
  e.preventDefault()
  // retrieve form data
  var keys = ['token', 'url', 'since', 'until']
  var data = {}
  keys.forEach(function (key) {
    data[key] = $('#' + key).val()
  })
  // send POST /allposts request
  sendJSON('/allposts', data, 'POST')
  .done(function (res) {
    console.log(res)
    var html
    if (res.length !== 0) {
      html = makeHtml(res)
    }
    else html = ''
    $('#msg').html('<p>共有 ' + res.length + ' 筆結果。</p>')
    $('#result').html(html)
    $('#result .parser-download').click(downloadListener)
  })
})