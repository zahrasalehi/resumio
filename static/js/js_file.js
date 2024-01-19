function showAnswer() {
    var user_input = document.getElementById("user_input").value;
    var answer = getAnswer(user_input);
    document.getElementById("answer").innerHTML = answer;
    document.getElementById("answer").style.display = "block";
}

function getAnswer(user_input) {

    fetch('/resume/get')  // Replace with your actual URL
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const answer = answer.key;

            // Use the extracted values as needed
            return answer
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
