document.addEventListener("DOMContentLoaded", function () {

function setupPopup(config) {

    const popup = document.getElementById(config.popupId);

    if (!popup) {
        console.error(config.popupId + " popup HTML was not found.");
        return;
    }

    const openButtons = document.querySelectorAll(config.openSelector);
    const closeButtons = popup.querySelectorAll(config.closeSelector);


    // OPEN POPUP
    function openPopup() {
        popup.classList.add("is-open");
        popup.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";
    }


    // CLOSE POPUP
    function closePopup() {
        popup.classList.remove("is-open");
        popup.setAttribute("aria-hidden", "true");

        // Restore scrolling only when no popup remains open.
        const anotherPopupOpen = document.querySelector(
            ".popup-overlay.is-open"
        );

        if (!anotherPopupOpen) {
            document.body.style.overflow = "";
        }
    }


    // OPEN WHEN THE LINK IS CLICKED
    openButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {
            event.preventDefault();
            openPopup();
        });

    });


    // CLOSE USING THE X BUTTON
    closeButtons.forEach(function (button) {

        button.addEventListener("click", function () {
            closePopup();
        });

    });


    // CLOSE WHEN CLICKING OUTSIDE THE POPUP
    popup.addEventListener("click", function (event) {

        if (event.target === popup) {
            closePopup();
        }

    });


    // CLOSE WHEN PRESSING ESCAPE
    document.addEventListener("keydown", function (event) {

        if (
            event.key === "Escape" &&
            popup.classList.contains("is-open")
        ) {
            closePopup();
        }

    });


    console.log(config.popupId + " initialized.");
    console.log("Opening buttons found:", openButtons.length);

}


// =====================================
// ABOUT POPUP
// =====================================

setupPopup({
    popupId: "aboutPopup",
    openSelector: '[data-open-popup="about"]',
    closeSelector: "[data-close-popup]"
});


// =====================================
// HOW IT WORKS POPUP
// =====================================

setupPopup({
    popupId: "howItWorksPopup",
    openSelector: '[data-open-popup="how-it-works"]',
    closeSelector: "[data-close-how-it-works]"
});


});
