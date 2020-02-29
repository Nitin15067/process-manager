function add_tab_to_textarea(){
	var textareas = document.getElementsByTagName('textarea');
	var count = textareas.length;
	for(var i=0;i<count;i++){
	    textareas[i].onkeydown = function(e){
	        if(e.keyCode==9 || e.which==9){
	            e.preventDefault();
	            var s = this.selectionStart;
	            this.value = this.value.substring(0,this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
	            this.selectionEnd = s+1; 
	        }
	    }
	}
}

function get_script(){
	var request_data = new FormData();
    request_data.append("process_id", $('.info_div').data('pid'));
	$.ajax({
        type: "POST",
        url: "/get_script",
        success: function (data) {
            if (data.status == true){
            	$('.notes').empty()
            	for (i=0; i<data.script_data.length; i++){
            		$('.notes').append(data.script_data[i])	
            	}
            	$('.editor').dimmer('hide');
            } else {
            	window.alert('Oops! There was an issue while reading the script file. Please try uploading the script again _/\\_. \n\n' + data.error)
            }
        },
        error: function (error) {
            window.alert('Alert! System returned error. Please contact admin _/\\_. \n\n' + error)
        },
        async: true,
        data: request_data,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 60000
    });
}

function get_logs(){
	var request_data = new FormData();
    request_data.append("process_id", $('.info_div').data('pid'));
	$.ajax({
        type: "POST",
        url: "/get_logs",
        success: function (data) {
            if (data.status == true){
                
            	$('.logs').empty()
            	for (i=0; i<data.script_data.length; i++){
            		$('.logs').append(data.script_data[i])	
            	}
            	$('.editor_logs').dimmer('hide');

            } else {
            	window.alert('Oops! There was an issue while reading the script file. Please try uploading the script again _/\\_. \n\n' + data.error)
            }
        },
        error: function (error) {
            window.alert('Alert! System returned error. Please contact admin _/\\_. \n\n' + error)
        },
        async: true,
        data: request_data,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 60000
    });
}

var Upload = function (file) {
    this.file = file;
};
Upload.prototype.getType = function() {
    return this.file.type;
};
Upload.prototype.getSize = function() {
    return this.file.size;
};
Upload.prototype.getName = function() {
    return this.file.name;
};
Upload.prototype.doUpload = function () {
    var formData = new FormData();
    formData.append("file", this.file);

    $.ajax({
        type: "POST",
        url: "/upload/" + $('.info_div').data('pid'),
        success: function (data) {
            if (data.status == true){
            	$('.notes').empty()
            	for (i=0; i<data.script_data.length; i++){
            		$('.notes').append(data.script_data[i])	
            	}
            } else {
            	window.alert('Oops! There was an issue regarding file upload. Please try again _/\\_. \n\n' + data.error)
            }
        },
        error: function (error) {
            window.alert('Alert! System returned error. Please contact admin _/\\_. \n\n' + error)
        },
        async: true,
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        timeout: 60000
    });
};


$(document).ready(function () {
	$('.ui.file.input').find('input:text, .ui.button')
		.on('click', function(e) {
			$(e.target).parent().find('input:file').click();
		})
	;

	$('input:file', '.ui.file.input')
		.on('change', function(e) {
			var file = $(e.target);
			var name = '';

			for (var i=0; i<e.target.files.length; i++) {
				name += e.target.files[i].name + ', ';
			}
			name = name.replace(/,\s*$/, '');
			extension = name.split('.').pop()

			if (extension === 'py'){
				$('input:text', file.parent()).val(name);
				var upload = new Upload(e.target.files[0]);
				upload.doUpload();
			} else {
				window.alert('This is version 0! Only python files are accepted.')
			}
		})
	;

	$('.script_runner_button').on('click', function(){
		if ($('.notes').val() == "") {
			$(".error_message_1").show()
			$(".error_message_1").delay(3200).fadeOut(300);
		} else {
			var request_data = new FormData();
    		request_data.append("process_id", $('.info_div').data('pid'));
    		request_data.append("script_data", $('.notes').val());
			
			$.ajax({
		        type: "POST",
		        url: "/run_script",
		        success: function (data) {
		            if (data.status == true){
		            	$('.script_runner').hide()
                        $('.file_uploader').hide()
		            	$('.runner_message').show()
                        window.location.reload()
		            } else {
		            	window.alert('Oops! This is standard error. Please check code _/\\_. \n' + data.error)
		            }
		        },
		        error: function (error) {
		            window.alert('Alert! System returned error. Please contact admin _/\\_. \n' + 'ERROR: ' +error)
		        },
		        async: true,
		        data: request_data,
		        cache: false,
		        contentType: false,
		        processData: false
		    });
		}
	});

	$('.lines').linenumbers({start:1, digits:10});
	add_tab_to_textarea()
	$('.editor').dimmer('show');
	$('.editor_logs').dimmer('show');
	get_script()

	get_logs()
});
