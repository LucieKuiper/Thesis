function changeAnswer(id) {
	for (let i = 0; i < ANSWER_IDS.length; i++) {
		let question = document.getElementById(ANSWER_IDS[i]);
		if (question.classList.contains("active_answer")) {
			question.classList.remove("active_answer");
		}
	}

	document.getElementById(ANSWER_IDS[id]).classList.add("active_answer");
	if (id == 0){
	    document.getElementById("answer").value = "A"
	}
	else if (id == 1){
	    document.getElementById("answer").value = "B"
	}

	else if (id == 2){
	    document.getElementById("answer").value = "C"
	}


	else if (id == 3){
	    document.getElementById("answer").value = "D"
	}

	else {
	    document.getElementById("answer").value = "No Answer"
	}

}