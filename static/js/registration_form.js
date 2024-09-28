// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const courseData = document.currentScript
  ? JSON.parse(document.currentScript.nextElementSibling.textContent)
  : {};

document.addEventListener("DOMContentLoaded", function () {
  const finalFeeContainer = document.getElementById("final-fee-container");
  const finalFeeDisplay = document.getElementById("final-fee-display");
  const entireCourseWithoutDanPreparation = document.getElementById(
    "entire-course-without-dan-preparation",
  );
  const entireCourse = document.getElementById("entire-course");
  const sessionCheckboxes = document.querySelectorAll(
    '#id_selected_sessions input[type="checkbox"]',
  );
  const regularSessionCheckboxes = document.querySelectorAll(
    '#id_selected_sessions input[type="checkbox"][data-dan-preparation="False"]',
  );
  const specialSessionCheckboxes = document.querySelectorAll(
    '#id_selected_sessions input[type="checkbox"][data-dan-preparation="True"]',
  );
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

  function updateEntireCourseWithoutDanPreparation() {
    const allRegularChecked = Array.from(regularSessionCheckboxes).every(
      (cb) => cb.checked,
    );
    const anySpecialChecked = Array.from(specialSessionCheckboxes).some(
      (cb) => cb.checked,
    );
    entireCourseWithoutDanPreparation.checked =
      allRegularChecked && !anySpecialChecked;
  }

  function updateEntireCourse() {
    if (entireCourse) {
      entireCourse.checked = Array.from(sessionCheckboxes).every(
        (cb) => cb.checked,
      );
    }
  }

  function handleSessionCheckboxChange() {
    updateEntireCourseWithoutDanPreparation();
    updateEntireCourse();
    calculateFinalFee(courseData);
    disableSubmitButton();
  }

  function handleEntireCourseWithoutDanPreparationChange() {
    const isChecked = entireCourseWithoutDanPreparation.checked;
    regularSessionCheckboxes.forEach((cb) => (cb.checked = isChecked));
    specialSessionCheckboxes.forEach((cb) => (cb.checked = false));
    if (entireCourse) {
      entireCourse.checked = false;
    }
    updateEntireCourse();
    calculateFinalFee(courseData);
    disableSubmitButton();
  }

  function handleEntireCourseChange() {
    const isChecked = entireCourse.checked;
    sessionCheckboxes.forEach((cb) => (cb.checked = isChecked));
    updateEntireCourseWithoutDanPreparation();
    calculateFinalFee(courseData);
    disableSubmitButton();
  }

  /**
   * Calculate the final fee and display it
   */
  function calculateFinalFee(courseData) {
    let finalFee = 0;
    let paymentMethod = paymentMethodSelect.value;
    if (entireCourseWithoutDanPreparation.checked) {
      finalFee =
        paymentMethod == 0 ? courseData.course_fee : courseData.course_fee_cash;
    } else if (entireCourse && entireCourse.checked) {
      finalFee =
        paymentMethod == 0
          ? courseData.course_fee_with_dan_preparation
          : courseData.course_fee_with_dan_preparation_cash;
    } else {
      let i = 0;
      for (let checkbox of sessionCheckboxes) {
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
    finalFeeDisplay.innerText = Number.isInteger(finalFee)
      ? finalFee
      : finalFee.toFixed(2);
  }

  /**
   * Disable submit button if form is invalid
   */
  function disableSubmitButton() {
    let checkboxChecked = false;
    for (let checkbox of sessionCheckboxes) {
      if (checkbox.checked == true) {
        checkboxChecked = true;
        sessionMsg.style.display = "none";
        break;
      } else {
        sessionMsg.style.display = "inline";
      }
    }
    if (
      entireCourseWithoutDanPreparation.checked ||
      (entireCourse && entireCourse.checked)
    ) {
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
    if (checkDojo && otherDojoDiv) {
      if (dojoSelect.value != "other") {
        otherDojoDiv.style.display = "none";
        otherDojoInput.value = "Other Dojo";
      } else {
        otherDojoDiv.style.display = "block";
        otherDojoInput.value = "";
      }
    }
  }

  sessionCheckboxes.forEach((cb) =>
    cb.addEventListener("change", handleSessionCheckboxChange),
  );
  entireCourseWithoutDanPreparation.addEventListener(
    "change",
    handleEntireCourseWithoutDanPreparationChange,
  );
  if (entireCourse) {
    entireCourse.addEventListener("change", handleEntireCourseChange);
  }

  if (discountCheckbox) {
    discountCheckbox.addEventListener("change", () =>
      calculateFinalFee(courseData),
    );
  }

  if (acceptTermsCheckbox) {
    acceptTermsCheckbox.addEventListener("click", disableSubmitButton);
  }

  if (gradeSelect) {
    gradeSelect.addEventListener("change", checkGrade);
  }

  if (dojoSelect) {
    dojoSelect.addEventListener("change", checkDojo);
  }

  paymentMethodSelect.addEventListener("change", () =>
    calculateFinalFee(courseData),
  );

  // Initial checks:
  checkDojo();
  updateEntireCourseWithoutDanPreparation();
  updateEntireCourse();
  calculateFinalFee(courseData);
  disableSubmitButton();

  // Expose functions for testing
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      handleSessionCheckboxChange,
      handleEntireCourseWithoutDanPreparationChange,
      handleEntireCourseChange,
      updateEntireCourseWithoutDanPreparation,
      updateEntireCourse,
      calculateFinalFee,
      disableSubmitButton,
      finalFeeDisplay,
      entireCourse,
      specialSessionCheckboxes,
      sessionCheckboxes,
      acceptTermsCheckbox,
      submitButton,
      sessionMsg,
      termsMsg,
    };
  }
});
