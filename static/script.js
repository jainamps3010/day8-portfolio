// Navbar scroll effect
window.addEventListener("scroll", function() {
    let navbar = document.getElementById("navbar")
    if (window.scrollY > 50) {
        navbar.style.background = "#0f0f1a"
    } else {
        navbar.style.background = "#1a1a2e"
    }
})

// Show success message if redirected after form submit
window.addEventListener("load", function() {
    if (window.location.hash === "#contact-success") {
        let msg = document.getElementById("contact-success")
        if (msg) {
            msg.style.display = "block"
            // Hide after 5 seconds
            setTimeout(function() {
                msg.style.display = "none"
            }, 5000)
        }
    }
})