// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const courseData = document.currentScript
  ? JSON.parse(document.currentScript.nextElementSibling.textContent)
  : {};

document.addEventListener("DOMContentLoaded", function () {
  const stickyFeeRow = document.getElementById("sticky-fee-row");
  const finalFeeDisplay = document.getElementById("final-fee-display");
  const finalFeeInfo = document.getElementById("final-fee-info");
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
  const danMemberCheckbox = document.getElementById("id_dan_member");
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
    displayFinalFee(courseData);
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
    displayFinalFee(courseData);
    disableSubmitButton();
  }

  function handleEntireCourseChange() {
    const isChecked = entireCourse?.checked;
    sessionCheckboxes.forEach((cb) => (cb.checked = isChecked));
    updateEntireCourseWithoutDanPreparation();
    displayFinalFee(courseData);
    disableSubmitButton();
  }

  /**
   * Get fee type from course data according to selected sessions
   */
  function getFeeType(courseData) {
    let feeType;

    // Check if all session checkboxes are on the same day
    let sessionDates = new Set(
      Array.from(sessionCheckboxes)
        .filter((checkbox) => checkbox.checked)
        .map((checkbox) => checkbox.dataset.date),
    );
    let singleDay = sessionDates.size === 1;

    switch (courseData.course_type) {
      case "sensei_emmerson":
        if (courseData.fee_category === "dan_seminar") {
          feeType = singleDay ? "single_day" : "entire_course";
        } else if (
          entireCourse?.checked &&
          courseData.course_has_dan_preparation
        ) {
          feeType = "entire_course_dan_preparation";
        } else if (entireCourseWithoutDanPreparation.checked) {
          feeType = "entire_course";
        } else {
          feeType = "single_session";
        }
        break;

      case "hombu_dojo":
        if (entireCourse?.checked) {
          feeType = "entire_course";
        } else {
          feeType = singleDay ? "single_day" : "entire_course";
        }
        break;

      case "external_teacher":
        if (courseData.fee_category === "dan_seminar") {
          feeType = "single_session";
        } else if (
          entireCourse?.checked &&
          courseData.course_has_dan_preparation
        ) {
          feeType = "entire_course_dan_preparation";
        } else if (entireCourseWithoutDanPreparation.checked) {
          feeType = "entire_course";
        } else {
          feeType = "single_session";
        }
        break;

      case "dan_bw_teacher":
        feeType = "single_session";
        break;

      case "children":
        feeType = "entire_course";
        break;

      default:
        feeType = null;
    }

    return feeType;
  }

  /**
   * Get fee from fee data according to fee type, payment method
   * and dan membership status
   */
  function getFee(feeType, paymentMethod, danMember, fees) {
    const feeObj = fees.find((fee) => fee.fee_type === feeType);

    if (feeObj) {
      let fee = feeObj.amount;

      if (paymentMethod === "cash") {
        fee += feeObj.extra_fee_cash;
      }
      if (!danMember) {
        fee += feeObj.extra_fee_external;
      }

      return fee;
    } else {
      console.error(`Fee not found for ${feeType}`);
      return null;
    }
  }

  function getFeeTypeDisplay(feeType, fees) {
    const feeObj = fees.find((fee) => fee.fee_type === feeType);

    if (feeObj) {
      return feeObj.fee_type_display;
    } else {
      console.error(`Fee not found for ${feeType}`);
      return null;
    }
  }

  /**
   * Calculate fees for individual sessions and return the total and count
   */
  function calculateIndividualSessions(
    sessionCheckboxes,
    courseData,
    paymentMethod,
    danMember,
  ) {
    let finalFee = 0;
    let sessionCount = 0;

    for (let checkbox of sessionCheckboxes) {
      if (!checkbox.checked) continue;

      const sessionType =
        checkbox.getAttribute("data-dan-preparation") == "True"
          ? "single_session_dan_preparation"
          : "single_session";

      let fee = getFee(sessionType, paymentMethod, danMember, courseData.fees);
      finalFee += fee ? fee : 0;
      sessionCount++;
    }

    return { finalFee, sessionCount };
  }

  /**
   * Calculate the final fee based on the selected sessions, payment method
   * and dan membership status
   */
  function calculateFinalFee(courseData) {
    const paymentMethod = paymentMethodSelect.value == 0 ? "bank" : "cash";
    const danMember = danMemberCheckbox ? danMemberCheckbox.checked : true;
    const feeType = getFeeType(courseData);
    let finalFee = 0;
    let sessionCount = 0;

    if (feeType.includes("single_session")) {
      const result = calculateIndividualSessions(
        sessionCheckboxes,
        courseData,
        paymentMethod,
        danMember,
      );
      finalFee = result.finalFee;
      sessionCount = result.sessionCount;
    } else {
      finalFee = getFee(feeType, paymentMethod, danMember, courseData.fees);
    }

    return { finalFee: finalFee ? finalFee : 0, feeType, sessionCount };
  }

  /**
   * Display the final fee
   */
  function displayFinalFee() {
    let { finalFee, feeType, sessionCount } = calculateFinalFee(courseData);
    let feeTypeDisplay = getFeeTypeDisplay(feeType, courseData.fees);
    let sessionSelected = Array.from(sessionCheckboxes).some(
      (cb) => cb.checked,
    );

    if (discountCheckbox.checked) {
      finalFee *= 1 - courseData.discount_percentage / 100;
    }

    if (finalFee > 0 && sessionSelected) {
      stickyFeeRow.classList.remove("d-none");
    } else {
      stickyFeeRow.classList.add("d-none");
    }

    finalFeeDisplay.innerText = Number.isInteger(finalFee)
      ? finalFee
      : finalFee.toFixed(2);
    if (sessionCount >= 1) {
      finalFeeInfo.innerText = ` (${sessionCount} x ${feeTypeDisplay}`;
    } else {
      finalFeeInfo.innerText = ` (${feeTypeDisplay}`;
    }
    finalFeeInfo.innerText += `, ${paymentMethodSelect.options[paymentMethodSelect.selectedIndex].text}`;
    if (danMemberCheckbox?.checked) {
      finalFeeInfo.innerText += `, ${courseData.dan_member_display}`;
    }
    if (discountCheckbox?.checked) {
      finalFeeInfo.innerText += `, ${courseData.discount_display}`;
    }
    finalFeeInfo.innerText += ")";
  }

  /**
   * Disable submit button if form is invalid
   */
  function disableSubmitButton() {
    let checkboxChecked = false;
    for (let checkbox of sessionCheckboxes) {
      if (checkbox.checked == true) {
        checkboxChecked = true;
        sessionMsg.style.visibility = "hidden";
        break;
      } else {
        sessionMsg.style.visibility = "visible";
      }
    }
    if (entireCourseWithoutDanPreparation.checked || entireCourse?.checked) {
      checkboxChecked = true;
    }
    if (acceptTermsCheckbox.checked) {
      termsMsg.style.visibility = "hidden";
    } else {
      termsMsg.style.visibility = "visible";
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
      displayFinalFee(courseData),
    );
  }

  if (danMemberCheckbox) {
    danMemberCheckbox.addEventListener("change", () =>
      displayFinalFee(courseData),
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
    displayFinalFee(courseData),
  );

  // Initial checks:
  checkDojo();
  updateEntireCourseWithoutDanPreparation();
  updateEntireCourse();
  displayFinalFee(courseData);
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
      displayFinalFee,
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
