document.addEventListener("DOMContentLoaded", function () {
  /**
   * Show accordion item if it is targeted from id in url
   */
  function showAccordionItem() {
    if (document.getElementById("course-list") && location.hash) {
      const id = location.hash.replace("#", "");
      let item = document.getElementById(`button-${id}`);
      if (item) {
        item.click();
        item.scrollIntoView();
      }
    }
  }

  /**
   * Update show/hide past courses button according to aria-expanded attribute
   */
  function updatePastCoursesButton() {
    if (pastCoursesBtn && showPastCourses && hidePastCourses) {
      if (pastCoursesBtn.getAttribute("aria-expanded") === "true") {
        showPastCourses.classList.add("d-none");
        hidePastCourses.classList.remove("d-none");
      } else {
        showPastCourses.classList.remove("d-none");
        hidePastCourses.classList.add("d-none");
      }
    }
  }

  /**
   * Auto close messages
   */
  function autoCloseMessages() {
    let messages = document.getElementsByClassName("msg");
    let timeoutDelay = 3000;
    for (let message of messages) {
      setTimeout(function () {
        message.remove();
      }, timeoutDelay);
    }
  }

  const pastCoursesBtn = document.getElementById("past-courses-btn");
  const showPastCourses = document.getElementById("show-past-courses");
  const hidePastCourses = document.getElementById("hide-past-courses");
  const loginToastElement = document.getElementById('loginToast');
  const honeypotDiv = document.getElementById("div_id_website");
  const honeypot = document.getElementById("id_website");

  if (pastCoursesBtn) {
    pastCoursesBtn.addEventListener("click", updatePastCoursesButton);
  }

  if (loginToastElement) {
    const loginToast = new bootstrap.Toast(loginToastElement);
    loginToast.show();
  }

  // Hide honeypot field in contact form
  if (honeypot) {
    honeypot.removeAttribute("required");
    honeypotDiv.classList.add("d-none");
  }
  
  console.log("honeypot");

  showAccordionItem();
  autoCloseMessages();
});

if (typeof module !== "undefined" && module.exports) {
  module.exports = { showAccordionItem, autoCloseMessages };
}

