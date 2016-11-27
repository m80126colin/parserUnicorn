<p>
	<input id="data" type="text" name="data" />
	<button id="submit">上傳</button>
</p>
<p>
	<canvas id="cloud" style="width: 1000px"></canvas>
</p>
<script src="/public/wordcloud2.js"></script>
<script src="/public/jquery.min.js"></script>
<script>
	$('#submit').click(function (e) {
		var data = $('#data').val()
		console.log(typeof data)
		console.log(data)
		$.ajax({
			type:        'POST',
			url:         '/cloud',
			data:        data,
			contentType: 'application/json',
			dataType:    'json'
		})
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