// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const courseData = document.currentScript
  ? JSON.parse(document.currentScript.nextElementSibling.textContent)
  : {};

// Lazy getters for DOM elements
const getStickyFeeRow = () => document.getElementById("sticky-fee-row");
const getFinalFeeDisplay = () => document.getElementById("final-fee-display");
const getFinalFeeInfo = () => document.getElementById("final-fee-info");
const getEntireCourseWithoutDanPreparation = () => document.getElementById("entire-course-without-dan-preparation");
const getEntireCourse = () => document.getElementById("entire-course");
const getSessionCheckboxes = () => document.querySelectorAll('#id_selected_sessions input[type="checkbox"]');
const getRegularSessionCheckboxes = () => document.querySelectorAll('#id_selected_sessions input[type="checkbox"][data-dan-preparation="False"]');
const getSpecialSessionCheckboxes = () => document.querySelectorAll('#id_selected_sessions input[type="checkbox"][data-dan-preparation="True"]');
const getAcceptTermsCheckbox = () => document.getElementById("id_accept_terms");
const getSubmitButton = () => document.getElementById("submit-button");
const getSessionMsg = () => document.getElementById("session-validation-msg");
const getTermsMsg = () => document.getElementById("terms-validation-msg");
const getGradeSelect = () => document.getElementById("id_grade");
const getExamCheckbox = () => document.getElementById("id_exam");
const getDiscountCheckbox = () => document.getElementById("id_discount");
const getDanMemberCheckbox = () => document.getElementById("id_dan_member");
const getPaymentMethodSelect = () => document.getElementById("id_payment_method");
const getDojoSelect = () => document.getElementById("id_dojo");
const getOtherDojoDiv = () => document.getElementById("div_id_other_dojo");
const getOtherDojoInput = () => document.getElementById("id_other_dojo");
const getAccommodationSelect = () => document.getElementById("id_accommodation_option");

function updateEntireCourseWithoutDanPreparation() {
  const entireCourseWithoutDanPreparation = getEntireCourseWithoutDanPreparation();
  const regularSessionCheckboxes = getRegularSessionCheckboxes();
  const specialSessionCheckboxes = getSpecialSessionCheckboxes();

  // Check if all regular sessions are selected and no special sessions
  const allRegularChecked = Array.from(regularSessionCheckboxes).every(
    (cb) => cb.checked,
  );
  const anySpecialChecked = Array.from(specialSessionCheckboxes).some(
    (cb) => cb.checked,
  );
  if (entireCourseWithoutDanPreparation) {
    entireCourseWithoutDanPreparation.checked =
      allRegularChecked && !anySpecialChecked;
  }
}

function updateEntireCourse() {
  const entireCourse = getEntireCourse();
  const sessionCheckboxes = getSessionCheckboxes();

  if (entireCourse) {
    // Check if all sessions are selected
    const allChecked = Array.from(sessionCheckboxes).every(
      (cb) => cb.checked,
    );
    entireCourse.checked = allChecked;
  }
}

function handleSessionCheckboxChange() {
  updateEntireCourseWithoutDanPreparation();
  updateEntireCourse();
  displayFinalFee(courseData);
  disableSubmitButton();
}

function handleEntireCourseWithoutDanPreparationChange() {
  const entireCourseWithoutDanPreparation = getEntireCourseWithoutDanPreparation();
  const regularSessionCheckboxes = getRegularSessionCheckboxes();
  const specialSessionCheckboxes = getSpecialSessionCheckboxes();
  const entireCourse = getEntireCourse();

  const isChecked = entireCourseWithoutDanPreparation?.checked;

  // Select all regular sessions, uncheck special sessions
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
  const entireCourse = getEntireCourse();
  const sessionCheckboxes = getSessionCheckboxes();

  const isChecked = entireCourse?.checked;

  // Select all sessions for all course types
  sessionCheckboxes.forEach((cb) => (cb.checked = isChecked));

  updateEntireCourseWithoutDanPreparation();
  displayFinalFee(courseData);
  disableSubmitButton();
}

/**
 * Get fee type from course data according to selected sessions
 */
function getFeeType(courseData) {
  const sessionCheckboxes = getSessionCheckboxes();
  const entireCourse = getEntireCourse();
  const entireCourseWithoutDanPreparation = getEntireCourseWithoutDanPreparation();

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
      } else if (entireCourseWithoutDanPreparation?.checked) {
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
      } else if (entireCourseWithoutDanPreparation?.checked) {
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

    case "family_reunion":
      // Check if entire course checkboxes are checked first
      if (
        entireCourse?.checked &&
        courseData.course_has_dan_preparation
      ) {
        feeType = "entire_course_with_dan_seminar";
      } else if (entireCourseWithoutDanPreparation?.checked) {
        feeType = "entire_course";
      } else {
        // Otherwise, check session selection
        // Get all unique days in the course
        const allCourseDays = new Set(
          Array.from(sessionCheckboxes).map((cb) => cb.dataset.date),
        );

        // Get unique days with at least one selected session
        const selectedDays = new Set(
          Array.from(sessionCheckboxes)
            .filter((cb) => cb.checked)
            .map((cb) => cb.dataset.date),
        );

        // Entire course = at least one session selected on each unique day
        const entireCourseSelected =
          allCourseDays.size === selectedDays.size &&
          [...allCourseDays].every((day) => selectedDays.has(day));

        const hasDanSessions = Array.from(sessionCheckboxes).some(
          (cb) => cb.checked && cb.dataset.danPreparation === "True",
        );

        if (entireCourseSelected) {
          feeType = hasDanSessions
            ? "entire_course_with_dan_seminar"
            : "entire_course";
        } else {
          feeType = hasDanSessions
            ? "single_day_with_dan_seminar"
            : "single_day";
        }
      }
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
 * Calculate fees per day for family reunion courses
 */
function calculateFamilyReunionDays(courseData, paymentMethod, danMember) {
  const sessionCheckboxes = getSessionCheckboxes();

  // Group sessions by date
  const sessionsByDate = {};
  Array.from(sessionCheckboxes).forEach((cb) => {
    if (cb.checked) {
      const date = cb.dataset.date;
      if (!sessionsByDate[date]) {
        sessionsByDate[date] = [];
      }
      sessionsByDate[date].push(cb);
    }
  });

  let finalFee = 0;
  let dayCount = 0;

  // Calculate fee for each day
  for (const [date, daySessions] of Object.entries(sessionsByDate)) {
    const hasDanSession = daySessions.some(
      (cb) => cb.dataset.danPreparation === "True",
    );
    const dayFeeType = hasDanSession
      ? "single_day_with_dan_seminar"
      : "single_day";
    const fee = getFee(dayFeeType, paymentMethod, danMember, courseData.fees);
    finalFee += fee ? fee : 0;
    dayCount++;
  }

  return { finalFee, dayCount };
}

/**
 * Calculate the final fee
 */
function calculateFinalFee(courseData) {
  const sessionCheckboxes = getSessionCheckboxes();
  const discountCheckbox = getDiscountCheckbox();
  const danMemberCheckbox = getDanMemberCheckbox();
  const paymentMethodSelect = getPaymentMethodSelect();
  const accommodationSelect = getAccommodationSelect();

  let paymentMethod =
    paymentMethodSelect?.value === "1" ? "cash" : "bank_transfer";
  let danMember = danMemberCheckbox?.checked || false;
  let feeType = getFeeType(courseData);
  let finalFee = 0;

  if (feeType && feeType.includes("single_session")) {
    ({ finalFee } = calculateIndividualSessions(
      sessionCheckboxes,
      courseData,
      paymentMethod,
      danMember,
    ));
  } else if (
    courseData.course_type === "family_reunion" &&
    feeType &&
    feeType.includes("single_day")
  ) {
    ({ finalFee } = calculateFamilyReunionDays(
      courseData,
      paymentMethod,
      danMember,
    ));
  } else {
    finalFee = getFee(feeType, paymentMethod, danMember, courseData.fees);
  }

  if (discountCheckbox?.checked) {
    finalFee = finalFee * (1 - courseData.discount_percentage / 100);
  }

  // Add accommodation fee if selected
  if (accommodationSelect && accommodationSelect.value) {
    const accommodationOption = courseData.accommodation_options?.find(
      (opt) => opt.id === parseInt(accommodationSelect.value),
    );
    if (accommodationOption) {
      finalFee += accommodationOption.fee;
    }
  }

  return { finalFee, feeType };
}

/**
 * Display the final fee in the sticky fee row
 */
function displayFinalFee(courseData) {
  const stickyFeeRow = getStickyFeeRow();
  const finalFeeDisplay = getFinalFeeDisplay();
  const finalFeeInfo = getFinalFeeInfo();
  const sessionCheckboxes = getSessionCheckboxes();

  const { finalFee, feeType } = calculateFinalFee(courseData);

  if (finalFeeDisplay && feeType) {
    const feeTypeDisplay = getFeeTypeDisplay(feeType, courseData.fees);
    finalFeeDisplay.textContent = `${finalFee.toFixed(2)} €`;

    let count = 0;

    if (feeType && feeType.includes("single_session")) {
      ({ sessionCount: count } = calculateIndividualSessions(
        sessionCheckboxes,
        courseData,
        "",
        false,
      ));
    } else if (
      courseData.course_type === "family_reunion" &&
      feeType &&
      feeType.includes("single_day")
    ) {
      ({ dayCount: count } = calculateFamilyReunionDays(courseData, "", false));
    }

    finalFeeInfo.textContent =
      count > 0 ? `${count}× ${feeTypeDisplay}` : feeTypeDisplay;
  }

  if (stickyFeeRow) {
    stickyFeeRow.classList.toggle("d-none", finalFee <= 0);
  }
}

/**
 * Disable submit button if validation fails
 */
function disableSubmitButton() {
  const sessionCheckboxes = getSessionCheckboxes();
  const acceptTermsCheckbox = getAcceptTermsCheckbox();
  const submitButton = getSubmitButton();
  const sessionMsg = getSessionMsg();
  const termsMsg = getTermsMsg();

  let sessionSelected = false;
  for (let checkbox of sessionCheckboxes) {
    if (checkbox.checked) {
      sessionSelected = true;
      break;
    }
  }

  let termsAccepted = acceptTermsCheckbox?.checked;

  if (sessionMsg) {
    sessionMsg.style.display = sessionSelected ? "none" : "inline";
  }
  if (termsMsg) {
    termsMsg.style.display = termsAccepted ? "none" : "inline";
  }
  if (submitButton) {
    if (sessionSelected && termsAccepted) {
      submitButton.classList.remove("disabled");
      submitButton.disabled = false;
    } else {
      submitButton.classList.add("disabled");
      submitButton.disabled = true;
    }
  }
}

function checkGrade() {
  const gradeSelect = getGradeSelect();
  const examCheckbox = getExamCheckbox();

  if (gradeSelect && examCheckbox) {
    if (parseInt(gradeSelect.value) >= 6) {
      examCheckbox.checked = false;
      examCheckbox.disabled = true;
    } else {
      examCheckbox.disabled = false;
    }
  }
}

function checkDojo() {
  const dojoSelect = getDojoSelect();
  const otherDojoDiv = getOtherDojoDiv();
  const otherDojoInput = getOtherDojoInput();

  if (dojoSelect && otherDojoDiv) {
    if (dojoSelect.value != "other") {
      otherDojoDiv.style.display = "none";
      if (otherDojoInput) {
        otherDojoInput.value = "Other Dojo";
      }
    } else {
      otherDojoDiv.style.display = "block";
      if (otherDojoInput) {
        otherDojoInput.value = "";
      }
    }
  }
}

// Event listener setup
document.addEventListener("DOMContentLoaded", function () {
  const sessionCheckboxes = getSessionCheckboxes();
  const entireCourseWithoutDanPreparation = getEntireCourseWithoutDanPreparation();
  const entireCourse = getEntireCourse();
  const discountCheckbox = getDiscountCheckbox();
  const danMemberCheckbox = getDanMemberCheckbox();
  const acceptTermsCheckbox = getAcceptTermsCheckbox();
  const gradeSelect = getGradeSelect();
  const dojoSelect = getDojoSelect();
  const paymentMethodSelect = getPaymentMethodSelect();
  const accommodationSelect = getAccommodationSelect();

  sessionCheckboxes.forEach((cb) =>
    cb.addEventListener("change", handleSessionCheckboxChange),
  );

  if (entireCourseWithoutDanPreparation) {
    entireCourseWithoutDanPreparation.addEventListener(
      "change",
      handleEntireCourseWithoutDanPreparationChange,
    );
  }

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

  if (paymentMethodSelect) {
    paymentMethodSelect.addEventListener("change", () =>
      displayFinalFee(courseData),
    );
  }

  if (accommodationSelect) {
    accommodationSelect.addEventListener("change", () =>
      displayFinalFee(courseData),
    );
  }

  // Initial checks:
  checkDojo();
  updateEntireCourseWithoutDanPreparation();
  updateEntireCourse();
  displayFinalFee(courseData);
  disableSubmitButton();
});

// Wrapper functions for backward compatibility with tests
function checkSessionCheckboxes() {
  const entireCourse = getEntireCourse();
  const sessionCheckboxes = getSessionCheckboxes();
  const isChecked = entireCourse?.checked;
  sessionCheckboxes.forEach((cb) => (cb.checked = isChecked));
}

function checkEntireCourseCheckbox() {
  return updateEntireCourse();
}

// Expose functions and elements for testing
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
    checkSessionCheckboxes,
    checkEntireCourseCheckbox,
    // Element getters for tests
    get entireCourseCheckbox() { return getEntireCourse(); },
    get finalFeeDisplay() { return getFinalFeeDisplay(); },
    get specialSessionCheckboxes() { return getSpecialSessionCheckboxes(); },
    get sessionCheckboxes() { return getSessionCheckboxes(); },
    get acceptTermsCheckbox() { return getAcceptTermsCheckbox(); },
    get submitButton() { return getSubmitButton(); },
    get sessionMsg() { return getSessionMsg(); },
    get termsMsg() { return getTermsMsg(); },
  };
}
