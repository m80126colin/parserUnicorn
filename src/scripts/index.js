import $ from 'jquery'

const postForm = (url, form) => {
  return $.ajax({
    type:        'POST',
    url:         url,
    data:        form,
    processData: false,
    contentType: false
  })
}

export default {
  $postForm: postForm
}