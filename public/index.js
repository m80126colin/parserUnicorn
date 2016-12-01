var sendJSON = function(url, data, type) {
  if (typeof type === 'undefined')
    type = 'GET'
  return $.ajax({
    type:        type,
    url:         url,
    data:        JSON.stringify(data),
    contentType: 'application/json',
    dataType:    'json'
  })
}