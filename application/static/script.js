if (window.history && history.pushState) {
    addEventListener('load', function() {
        history.pushState(null, null, null);
        addEventListener('popstate', function() {
            history.pushState(null, null, null);
        });
    });
}
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

let SURVEY = ['answer_0', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5', 'answer_6'];

    function survey(id) {
        for (let i = 0; i < SURVEY.length; i++) {
            let question = document.getElementById(SURVEY[i]);
            if (question.classList.contains("active_survey")) {
                question.classList.remove("active_survey");
            }
        }
      document.getElementById(SURVEY[id]).classList.add("active_survey");
      answers = ['0', '1', '2', '3', '4', '5', '6']
      document.getElementById("answer").value = answers[id]
}



