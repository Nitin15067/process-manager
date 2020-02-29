$(document).ready(function () {
	$('input.name').on('input', function(){
		var name = $('.name').val()
		name = name.trim()
		if (name === "") {
			$('.name_field').addClass('error');
		} else {
			$('.name_field').removeClass('error')
		}
	});

	$('input.description').on('input', function(){
		var description = $('.description').val()
		description = description.trim()
		if (description === "") {
			$('.description_field').addClass('error');
		} else {
			$('.description_field').removeClass('error')
		}
	});

	$('.create_process').on('click', function(){
		var name = $('.name').val()
		var description = $('.description').val()
		if ((name !== "") && (description !== "")) {
			var request_data = new FormData();
    		request_data.append("process_name", name);
    		request_data.append("process_description", description);

			$.ajax({
		        type: "POST",
		        url: "/create_process",
		        success: function (data) {
		            if (data.status == true){
		            	window.location.replace(data.process_url);
		            } else {
		            	window.alert('Oops! This is standard error. Please check code _/\\_. \n\n' + data.error)
		            }
		        },
		        error: function (error) {
		            window.alert('Alert! System returned error. Please contact admin _/\\_. \n\n' + 'ERROR: ' + error)
		        },
		        async: true,
		        data: request_data,
		        cache: false,
		        contentType: false,
		        processData: false
		    });
		} else {
			if (name === ""){
				$('.name_field').addClass('error')
			}

			if (description === ""){
				$('.description_field').addClass('error')
			}
		}
	});
});
