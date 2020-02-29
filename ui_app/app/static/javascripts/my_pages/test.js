var current_question_id = "";
var current_question_index = -1;
var total_questions = -1;
var answers = {};

function fill_answer() {
	selected_option = '';
	if (current_question_index in answers) {
		selected_option = answers[current_question_index]['selected'];
	}

	$('.option_div').data('selected', 0);
	$('.option_div').css({'border': '2px solid #DDDDDD'});
	if (selected_option != '') {
		selected_option_div = $('.option_div[data-id=' + selected_option + ']');
		selected_option_div.data('selected', 1);
		selected_option_div.css({'border': '2px solid teal'});
	}
}

function show_button_options() {
	$('.review_button').show();
	if (current_question_index > 1) {
		$('.previous_button').show();
	} else {
		$('.previous_button').hide();
	}
	if (current_question_index !== total_questions) {
		$('.next_button').show();
	} else {
		$('.next_button').hide();
	}
}

function fill_question_button_color(eventType, marked) {
	if (eventType == 'selected') {
		current_ques_button = $('.question_button[data-index=' + current_question_index + ']')
		if (marked == 0) {
			current_ques_button.removeClass('teal');
		}
		if (marked == 1) {
			current_ques_button.addClass('teal');
		}

		if (marked == 2) {
			current_ques_button.removeClass('orange');	
		}
		if (marked == 3) {
			current_ques_button.addClass('orange');	
		}
	}
}

$('.question_button').on('click', function(){
	$('.question_button').css({'border': '2px solid #DDDDDD'});
	$('.instruction_button').css({'border': '2px solid #DDDDDD'});
	$(this).css({'border': '2px solid black'});

	$('.instructions_div').hide();
	$('.error_div').hide();
	$('.begin_button').hide();
	$('.loader').addClass('active');

	var question_id = $(this).data('question_id');
	var index = $(this).data('index');
	current_question_index = index

	if (current_question_id !== question_id) {
		current_question_id = question_id;
		$.ajax({
			url: 'http://localhost:5000/question/'+question_id,
			data: {
				format: 'json'
			},
			error: function() {
				$('.error_div').html('<p>An error has occurred</p>');
			},
			success: function(data) {
				$('#question').html(data.question_data.question_text);
				$('#option1').html(data.question_data.options[0]);
				$('#option2').html(data.question_data.options[1]);
				$('#option3').html(data.question_data.options[2]);
				$('#option4').html(data.question_data.options[3]);
				$('.question_div').show();
				show_button_options();
				fill_answer();
			},
			type: 'GET'
		});
	}
	$('.loader').removeClass('active');
});

$('.instruction_button').on('click', function(){
	$('.question_button').css({'border': '2px solid #DDDDDD'});
	$(this).css({'border': '2px solid black'});

	$('.question_div').hide();
	$('.error_div').hide();
	$('.instructions_div').show();
});

$('.begin_button').on('click', function(){
	$('.question_button').children().first().click();
	$(this).hide();
});

$('.previous_button').on('click', function(){
	var prev_index = current_question_index - 1;
	$('.question_button[data-index=' + prev_index + ']').click()
});

$('.next_button').on('click', function(){
	var prev_index = current_question_index + 1;
	$('.question_button[data-index=' + prev_index + ']').click()
});

$('.review_button').on('click', function(){
	if (current_question_index in answers) {
		answers[current_question_index]['review'] = 1
	} else {
		answers[current_question_index] = {'selected':'', 'review': 1}
	}
	fill_question_button_color()
});

$('.option_div').hover(
	function(){
		if ($(this).data('selected') !== 1) {
			$(this).css({'border': '2px solid black'});
		}
	},
	function() {
		if ($(this).data('selected') === 1) {
			$(this).css({'border': '2px solid teal'});
		} else {
			$(this).css({'border': '2px solid #DDDDDD'});
		}
	}
);

$('.option_div').on('click', function(){
	if ($(this).data('selected') == 0) {
		$('.option_div').data('selected', 0);
		$('.option_div').css({'border': '2px solid #DDDDDD'});
		$(this).data('selected', 1);
		$(this).css({'border': '2px solid teal'});
		fill_question_button_color('selected', 1)
	} else {
		$('.option_div').data('selected', 0);
		$('.option_div').css({'border': '2px solid #DDDDDD'});
		fill_question_button_color('selected', 0)
	}
	if (current_question_index in answers) {
		answers[current_question_index]['selected'] = $(this).data('id')
	} else {
		answers[current_question_index] = {'selected':$(this).data('id'), 'review': 0}
	}
});

$(document).ready(function(){
	$('.question_div').hide();
	$('.previous_button').hide();
	$('.review_button').hide();
	$('.next_button').hide();
 	$('.loader').removeClass('active');

 	total_questions = $('.test_mapping').data('total_questions');
});
