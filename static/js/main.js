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
  function updateCoursesButton() {
    if (showHideCoursesBtn && showCourses && hideCourses) {
      if (showHideCoursesBtn.getAttribute("aria-expanded") === "true") {
        showCourses.classList.add("d-none");
        hideCourses.classList.remove("d-none");
      } else {
        showCourses.classList.remove("d-none");
        hideCourses.classList.add("d-none");
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

  const showHideCoursesBtn = document.getElementById("show-hide-courses-btn");
  const showCourses = document.getElementById("show-courses");
  const hideCourses = document.getElementById("hide-courses");
  const loginToastElement = document.getElementById('loginToast');
  const honeypotDiv = document.getElementById("div_id_website");
  const honeypot = document.getElementById("id_website");

  if (showHideCoursesBtn) {
    showHideCoursesBtn.addEventListener("click", updateCoursesButton);
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
  
  showAccordionItem();
  autoCloseMessages();
});

if (typeof module !== "undefined" && module.exports) {
  module.exports = { showAccordionItem, autoCloseMessages };
}

