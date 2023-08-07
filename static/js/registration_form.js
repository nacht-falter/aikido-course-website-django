/**
 * Check/uncheck all sessions if entire course box is checked/unchecked
 */
function checkSessionCheckboxes() {
  for (let checkbox of sessionsCheckboxes) {
    checkbox.checked = entireCourseCheckbox.checked;
  }
  calculateFinalFee(courseData);
  disableSubmitButton();
}

/**
 * Check/uncheck entire course box, depending on if sessions boxes are
 * checked/unchecked
 */
function checkEntireCourseCheckbox() {
  if (this.checked === false && entireCourseCheckbox.checked === true) {
    entireCourseCheckbox.checked = false;
  }
  let allSessionsSelected = true;
  for (let checkbox of sessionsCheckboxes) {
    if (checkbox.checked === false) {
      allSessionsSelected = false;
      break;
    }
  }
  entireCourseCheckbox.checked = allSessionsSelected;
  calculateFinalFee(courseData);
  disableSubmitButton();
}

/**
 * Calculate the final fee and display it
 */
function calculateFinalFee(courseData) {
  let finalFee = 0;
  if (entireCourseCheckbox.checked) {
    finalFee = courseData.course_fee;
  } else {
    let i = 0;
    for (let checkbox of sessionsCheckboxes) {
      if (checkbox.checked) {
        let sessionFee = courseData[`session_${i}_fee`];
        finalFee += sessionFee;
      }
      i++;
    }
  }
  finalFeeDisplay.innerText = finalFee;
}

/**
 * Disable submit button if form is invalid
 */
function disableSubmitButton() {
  let checkboxChecked = false;
  for (let checkbox of sessionsCheckboxes) {
    if (checkbox.checked == true) {
      checkboxChecked = true;
      break;
    }
  }
  if (entireCourseCheckbox.checked) {
    checkboxChecked = true;
  }
  if (checkboxChecked == true && acceptTermsCheckbox.checked) {
    submitButton.classList.remove("disabled");
  } else {
    submitButton.classList.add("disabled");
  }
}

// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const courseData = document.currentScript ? JSON.parse(document.currentScript.nextElementSibling.textContent) : {};

const finalFeeDisplay = document.getElementById("final-fee-display");
const entireCourseCheckbox = document.getElementById("entire-course");
const sessionsList = document.getElementById("id_selected_sessions");
const sessionsCheckboxes = sessionsList.querySelectorAll("input");
const acceptTermsCheckbox = document.getElementById("id_accept_terms");
const submitButton = document.getElementById("submit-button");

// Add event listeners to checkboxes:
entireCourseCheckbox.addEventListener("click", checkSessionCheckboxes);
for (let checkbox of sessionsCheckboxes) {
  checkbox.addEventListener("click", checkEntireCourseCheckbox);
}
acceptTermsCheckbox.addEventListener("click", disableSubmitButton);

checkEntireCourseCheckbox();

module.exports = {
  checkSessionCheckboxes,
  checkEntireCourseCheckbox,
  calculateFinalFee,
  disableSubmitButton,
  finalFeeDisplay,
  entireCourseCheckbox,
  sessionsCheckboxes,
  acceptTermsCheckbox,
  submitButton,
};
