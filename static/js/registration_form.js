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
  let paymentMethod = paymentMethodSelect.value;
  if (entireCourseCheckbox.checked) {
    finalFee =
      paymentMethod == 0 ? courseData.course_fee : courseData.course_fee_cash;
  } else {
    let i = 0;
    for (let checkbox of sessionsCheckboxes) {
      if (checkbox.checked) {
        let sessionFee =
          paymentMethod == 0
            ? courseData[`session_${i}_fee`]
            : courseData[`session_${i}_fee_cash`];
        finalFee += sessionFee;
      }
      i++;
    }
  }

  if (discountCheckbox.checked) {
    finalFee *= courseData.discount_percentage / 100;
  }
  if (finalFee > 0) {
    finalFeeContainer.classList.remove("d-none");
  } else {
    finalFeeContainer.classList.add("d-none");
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
      sessionMsg.style.display = "none";
      break;
    } else {
      sessionMsg.style.display = "inline";
    }
  }
  if (entireCourseCheckbox.checked) {
    checkboxChecked = true;
  }
  if (acceptTermsCheckbox.checked) {
    termsMsg.style.display = "none";
  } else {
    termsMsg.style.display = "inline";
  }
  if (checkboxChecked == true && acceptTermsCheckbox.checked) {
    submitButton.classList.remove("disabled");
  } else {
    submitButton.classList.add("disabled");
  }
}

/**
 * Hide exam section if grade is above 1st Kyu
 */
function checkGrade() {
  if (gradeSelect.value > 5) {
    examSection.style.display = "none";
  } else {
    examSection.style.display = "flex";
  }
}

function checkDojo() {
  if (dojoSelect.value != "other") {
    otherDojoDiv.style.display = "none";
    otherDojoInput.value = "";
  } else {
    otherDojoDiv.style.display = "block";
    otherDojoInput.value = "";
  }
}

// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const courseData = document.currentScript
  ? JSON.parse(document.currentScript.nextElementSibling.textContent)
  : {};

const finalFeeContainer = document.getElementById("final-fee-container");
const finalFeeDisplay = document.getElementById("final-fee-display");
const entireCourseCheckbox = document.getElementById("entire-course");
const sessionsList = document.getElementById("div_id_selected_sessions");
const sessionsCheckboxes = sessionsList.querySelectorAll("input");
const acceptTermsCheckbox = document.getElementById("id_accept_terms");
const submitButton = document.getElementById("submit-button");
const sessionMsg = document.getElementById("session-validation-msg");
const termsMsg = document.getElementById("terms-validation-msg");
const gradeSelect = document.getElementById("id_grade");
const examSection = document.getElementById("exam-section");
const discountCheckbox = document.getElementById("id_discount");
const paymentMethodSelect = document.getElementById("id_payment_method");
const dojoSelect = document.getElementById("id_dojo");
const otherDojoDiv = document.getElementById("div_id_other_dojo");
const otherDojoInput = document.getElementById("id_other_dojo");

otherDojoDiv.style.display = "none";

// Add event listeners:
entireCourseCheckbox.addEventListener("click", checkSessionCheckboxes);
for (let checkbox of sessionsCheckboxes) {
  checkbox.addEventListener("click", checkEntireCourseCheckbox);
}

discountCheckbox.addEventListener("click", checkEntireCourseCheckbox);

paymentMethodSelect.addEventListener("change", checkEntireCourseCheckbox);

acceptTermsCheckbox.addEventListener("click", disableSubmitButton);

if (gradeSelect) {
  gradeSelect.addEventListener("change", checkGrade);
}

dojoSelect.addEventListener("change", checkDojo);

// Initial checks:
checkEntireCourseCheckbox();

if (typeof module !== "undefined" && module.exports) {
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
    sessionMsg,
    termsMsg,
  };
}
