var html = ''
if (link !== '') {
  html = '<a class="pure-button" target="_blank" href="' + link + '">下載</a>'
}
$('#count').html(html)

list.sort(function (left, right) {
  return - (left[1] - right[1])
})
sublist = list.filter(function (item, i) {
  return i < 300
})

var factor = $('#cloud').width() / 1024

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