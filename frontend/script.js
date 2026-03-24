window.onbeforeunload = function () {
    console.log("⚠️ PAGE IS RELOADING");
};

console.log("✅ PAGE LOADED");

const submitBtn = document.getElementById("submitBtn");
const resultBox = document.getElementById("resultBox");

submitBtn.addEventListener("click", async function (e) {

    e.preventDefault();

    console.log("🔥 BUTTON CLICKED");

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        subject: document.getElementById("subject").value,
        description: document.getElementById("description").value,
        product: document.getElementById("product")?.value || ""  
    };

    if (!data.email.includes("@")) {
        alert("Invalid email");
        return;
    }

    if (data.description.length < 10) {
        alert("Description too short");
        return;
    }

    try {

        submitBtn.innerText = "Submitting...";
        submitBtn.disabled = true;

        const response = await fetch("http://127.0.0.1:5000/submit_ticket", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        console.log("✅ RESPONSE:", result);

        if (result.error) {
            alert(result.error);
            return;
        }

        resultBox.innerHTML = `
            <div class="success-card">
                <h3>✅ Ticket Submitted Successfully</h3>
                <div class="prediction">
                    <p><strong>Category:</strong> ${result.predicted_category}</p>
                    <p><strong>Confidence:</strong> ${result.confidence}</p>
                    <p><strong>Priority:</strong> ${result.priority}</p>
                    <p><strong>Assigned Team:</strong> ${result.assigned_team}</p>
                </div>
            </div>
        `;

        resultBox.style.display = "block";

        resultBox.scrollIntoView({behavior:"smooth"});

        document.getElementById("ticketForm").reset();

        const email = localStorage.getItem("email");
        if(email){
            document.getElementById("email").value = email;
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    } finally {
        submitBtn.innerText = "Submit Ticket";
        submitBtn.disabled = false;
    }

});