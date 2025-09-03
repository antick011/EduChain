// main.js

document.addEventListener("DOMContentLoaded", function () {
    const chatbotForm = document.getElementById("chatbot-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    if (chatbotForm) {
        chatbotForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message === "") return;

            appendMessage("You", message);
            userInput.value = "";

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();
                appendMessage("EduBot", data.reply);
            } catch (error) {
                appendMessage("EduBot", "Something went wrong. Please try again.");
            }
        });
    }

    function appendMessage(sender, message) {
        const div = document.createElement("div");
        div.classList.add("message");
        div.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
