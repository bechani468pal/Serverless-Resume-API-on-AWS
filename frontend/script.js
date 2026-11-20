const API_URL = "http://127.0.0.1:8000";
const API_KEY = "demo-resume-key";

const form = document.getElementById("resumeForm");
const preview = document.getElementById("resumePreview");
const message = document.getElementById("message");

// Add education fields
document.getElementById("addEducation").addEventListener("click", () => {
    const container = document.getElementById("educationFields");

    const item = document.createElement("div");
    item.className = "dynamic-item";

    item.innerHTML = `
        <input class="degree" placeholder="Degree">
        <input class="institution" placeholder="College / Institution">
        <input class="status" placeholder="Status">
        <button type="button" class="secondary remove-item">Remove</button>
    `;

    container.appendChild(item);
});

// Add experience fields
document.getElementById("addExperience").addEventListener("click", () => {
    const container = document.getElementById("experienceFields");

    const item = document.createElement("div");
    item.className = "dynamic-item";

    item.innerHTML = `
        <input class="company" placeholder="Company">
        <input class="role" placeholder="Job Role">
        <input class="duration" placeholder="Duration">
        <textarea class="description" placeholder="Work Description"></textarea>
        <button type="button" class="secondary remove-item">Remove</button>
    `;

    container.appendChild(item);
});

// Remove dynamically added sections
document.addEventListener("click", (event) => {
    if (event.target.classList.contains("remove-item")) {
        event.target.closest(".dynamic-item").remove();
    }
});

// Safely display user-entered text
function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[char]);
}

// Generate resume preview
function displayResume(data) {
    const p = data.personal;

    preview.innerHTML = `
        <h1>${escapeHTML(p.name)}</h1>
        <p>${escapeHTML(p.email)} | ${escapeHTML(p.phone)}</p>
        <p>${escapeHTML(p.location)}</p>

        <h3>Professional Summary</h3>
        <p>${escapeHTML(p.summary)}</p>

        <h3>Education</h3>
        <ul>
            ${data.education.map(item => `
                <li>
                    <strong>${escapeHTML(item.degree)}</strong><br>
                    ${escapeHTML(item.institution)}<br>
                    ${escapeHTML(item.status)}
                </li>
            `).join("")}
        </ul>

        <h3>Experience</h3>
        <ul>
            ${data.experience.map(item => `
                <li>
                    <strong>${escapeHTML(item.role)}</strong><br>
                    ${escapeHTML(item.company)}<br>
                    ${escapeHTML(item.duration)}<br>
                    ${escapeHTML(item.description)}
                </li>
            `).join("")}
        </ul>

        <h3>Skills</h3>
        <p>${data.skills.map(escapeHTML).join(" | ")}</p>
    `;
}

// Collect form data
function collectResume() {
    return {
        personal: {
            name: document.getElementById("name").value.trim(),
            email: document.getElementById("email").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            location: document.getElementById("location").value.trim(),
            summary: document.getElementById("summary").value.trim()
        },

        education: Array.from(document.querySelectorAll("#educationFields .dynamic-item"))
            .map(item => ({
                degree: item.querySelector(".degree").value.trim(),
                institution: item.querySelector(".institution").value.trim(),
                status: item.querySelector(".status").value.trim()
            }))
            .filter(item => item.degree || item.institution || item.status),

        experience: Array.from(document.querySelectorAll("#experienceFields .dynamic-item"))
            .map(item => ({
                company: item.querySelector(".company").value.trim(),
                role: item.querySelector(".role").value.trim(),
                duration: item.querySelector(".duration").value.trim(),
                description: item.querySelector(".description").value.trim()
            }))
            .filter(item => item.company || item.role || item.duration || item.description),

        skills: document.getElementById("skills").value
            .split(",")
            .map(skill => skill.trim())
            .filter(Boolean)
    };
}

// Submit resume to backend
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = collectResume();

    if (!data.personal.name || !data.personal.email) {
        message.textContent = "Please enter your name and email.";
        return;
    }

    message.textContent = "Saving your resume...";

    try {
        const response = await fetch(`${API_URL}/resume`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not save resume");
        }

        displayResume(result.resume);
        message.textContent = "Resume saved successfully!";

    } catch (error) {
        message.textContent = "Error: " + error.message;
        console.error(error);
    }
});

// Download / print resume as PDF
document.getElementById("downloadPDF").addEventListener("click", () => {
    if (!preview.querySelector("h1")) {
        message.textContent = "Please generate your resume first.";
        return;
    }

    window.print();
});

// Load existing resume from API
async function loadResume() {
    try {
        const response = await fetch(`${API_URL}/resume`, {
            headers: { "x-api-key": API_KEY }
        });

        if (!response.ok) {
            throw new Error("Could not load existing resume");
        }

        const result = await response.json();
        const data = result.resume;

        document.getElementById("name").value = data.personal.name || "";
        document.getElementById("email").value = data.personal.email || "";
        document.getElementById("phone").value = data.personal.phone || "";
        document.getElementById("location").value = data.personal.location || "";
        document.getElementById("summary").value = data.personal.summary || "";

        document.getElementById("skills").value = (data.skills || []).join(", ");

        // Populate education
        const educationContainer = document.getElementById("educationFields");
        educationContainer.innerHTML = "";

        (data.education || []).forEach(item => {
            const div = document.createElement("div");
            div.className = "dynamic-item";
            div.innerHTML = `
                <input class="degree" placeholder="Degree">
                <input class="institution" placeholder="College / Institution">
                <input class="status" placeholder="Status">
                <button type="button" class="secondary remove-item">Remove</button>
            `;

            div.querySelector(".degree").value = item.degree || "";
            div.querySelector(".institution").value = item.institution || "";
            div.querySelector(".status").value = item.status || "";

            educationContainer.appendChild(div);
        });

        // Populate experience
        const experienceContainer = document.getElementById("experienceFields");
        experienceContainer.innerHTML = "";

        (data.experience || []).forEach(item => {
            const div = document.createElement("div");
            div.className = "dynamic-item";
            div.innerHTML = `
                <input class="company" placeholder="Company">
                <input class="role" placeholder="Job Role">
                <input class="duration" placeholder="Duration">
                <textarea class="description" placeholder="Work Description"></textarea>
                <button type="button" class="secondary remove-item">Remove</button>
            `;

            div.querySelector(".company").value = item.company || "";
            div.querySelector(".role").value = item.role || "";
            div.querySelector(".duration").value = item.duration || "";
            div.querySelector(".description").value = item.description || "";

            experienceContainer.appendChild(div);
        });

        displayResume(data);

    } catch (error) {
        console.error("Loading error:", error);
        message.textContent = "Could not load saved resume. You can still create a new one.";
    }
}

loadResume();