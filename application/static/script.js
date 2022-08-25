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

    function surveySelf(id) {
        for (let i = 0; i < SURVEY.length; i++) {
            let question = document.getElementById(SURVEY[i]);
            if (question.classList.contains("active_survey_self")) {
                question.classList.remove("active_survey_self");
            }
        }
      document.getElementById(SURVEY[id]).classList.add("active_survey_self");
      answers = ['0', '1', '2', '3', '4', '5', '6']
      document.getElementById("self").value = answers[id]
}


let SURVEY_OTHER = ['other_0', 'other_1', 'other_2', 'other_3', 'other_4', 'other_5', 'other_6'];
function surveyOther(id) {
	for (let i = 0; i < SURVEY_OTHER.length; i++) {
		let question = document.getElementById(SURVEY_OTHER[i]);
		if (question.classList.contains("active_survey_other")) {
			question.classList.remove("active_survey_other");
		}
	}
	document.getElementById(SURVEY_OTHER[id]).classList.add("active_survey_other");
	others = ['0', '1', '2', '3', '4', '5', '6']
    document.getElementById("other").value = others[id]
}