let ANSWER_IDS = ['answer_A', 'answer_B', 'answer_C', 'answer_D'];

function changeAnswer(id) {
	for (let i = 0; i < ANSWER_IDS.length; i++) {
		let question = document.getElementById(ANSWER_IDS[i]);
		if (question.classList.contains("active_answer")) {
			question.classList.remove("active_answer");
		}
	}

	document.getElementById(ANSWER_IDS[id]).classList.add("active_answer");
	answers = ['A', 'B', 'C', 'D']
    document.getElementById("answer").value = answers[id]



}