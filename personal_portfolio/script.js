const alertBtn = document.getElementById("alertBtn");

alertBtn.addEventListener("click", function () {
    alert("Thank you for visiting!");
});

const aboutBtn = document.getElementById("aboutBtn");
const aboutSection = document.getElementById("about");

aboutBtn.addEventListener("click", function () {
    if (aboutSection.style.display === "none") {
        aboutSection.style.display = "block";
    } else {
        aboutSection.style.display = "none";
    }
});

const contactBtn = document.getElementById("contactBtn");
const contactSection = document.getElementById("contact");

contactBtn.addEventListener("click", function () {
    contactSection.scrollIntoView({ behavior: "smooth" });
});
