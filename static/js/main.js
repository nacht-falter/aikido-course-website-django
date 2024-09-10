/**
 * Show accordion item if it is targeted from id in url
 */
function showAccordionItem() {
  if (document.getElementById("course-list")) {
    // Get Course id from url:
    // https://stackoverflow.com/a/1036564
    const id = location.hash.replace("#", "");
    let item = document.getElementById(`button-${id}`);
    if (item) {
      item.click();
    }
  }
}

/**
 * Update show/hide past courses button according to aria-expanded attribute
 */
function updatePastCoursesButton() {
  if (pastCoursesBtn.getAttribute("aria-expanded") === "true") {
    showPastCourses.classList.add("d-none");
    hidePastCourses.classList.remove("d-none");
  } else {
    showPastCourses.classList.remove("d-none");
    hidePastCourses.classList.add("d-none");
  }
}

/**
 * Auto close messages (Adapted from CI DjangoBlog tutorial)
 */
function autoCloseMessages() {
  let messages = document.getElementsByClassName("msg");
  let timeoutDelay = 3000;
  for (let message of messages) {
    setTimeout(function () {
      message.remove();
    }, timeoutDelay);
    timeoutDelay += 3000;
  }
}

const pastCoursesBtn = document.getElementById("past-courses-btn");
const showPastCourses = document.getElementById("show-past-courses");
const hidePastCourses = document.getElementById("hide-past-courses");
if (pastCoursesBtn) {
  pastCoursesBtn.addEventListener("click", updatePastCoursesButton);
}

showAccordionItem();
autoCloseMessages();

if (typeof module !== "undefined" && module.exports) {
  module.exports = { showAccordionItem, autoCloseMessages };
}
