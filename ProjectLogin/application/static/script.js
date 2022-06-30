let ANSWER_IDS = ['answer_A', 'answer_B', 'answer_C', 'answer_D'];


function changeAnswer(id) {
	for (let i = 0; i < ANSWER_IDS.length; i++) {
		let question = document.getElementById(ANSWER_IDS[i]);
		if (question.classList.contains("active_answer")) {
			question.classList.remove("active_answer");
		}
	}

	document.getElementById(ANSWER_IDS[id]).classList.add("active_answer");

}

 function getActiveAnswer() {
    var current_answer = null;
	for (let i = 0; i < ANSWER_IDS.length; i++) {
		let question = document.getElementById(ANSWER_IDS[i]);
		if (question.classList.contains("active_answer")) {
			//return ANSWER_IDS[i];
			alert(ANSWER_IDS[i]);
			//document.write(ANSWER_IDS[i]);
		}
	}

	//return null;
}

