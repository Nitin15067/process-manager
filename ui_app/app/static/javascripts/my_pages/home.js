$(document).ready(function () {
	$('.sortable.table').tablesort();

	$('.process_row').on('click', function(){
		process_url = $(this).data('url');
		url_prefix = $(this).data('url_prefix');
		redirect_url = url_prefix + process_url
		window.location.href = redirect_url
	});

	$('.ui.search')
		.search({
			apiSettings: {
				url: 'http://localhost:5000/search/{query}'
			},
			fields: {
				results: 'result_data',
		    	title: 'name',
		    	url: 'html_url'
			}
		});

	
		

});
