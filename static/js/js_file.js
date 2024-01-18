function showAnswer() {
    var user_input = document.getElementById("user_input").value;
    var answer = getAnswer(user_input);
    document.getElementById("answer").innerHTML = answer;
    document.getElementById("answer").style.display = "block";
}

function getAnswer(user_input) {
    // Here you can implement your logic to retrieve the answer based on the question
    // For simplicity, let's assume we have a predefined set of questions and answers
    var answers = {
        "What is the capital of France?": "Paris",
        "Who painted the Mona Lisa?": "Leonardo da Vinci",
        "What is the answer to life, the universe, and everything?": "42"
    };

    return answers[user_input] || "Sorry, I don't have the answer to that question.";
}
