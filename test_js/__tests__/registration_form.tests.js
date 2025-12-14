let source;
let courseData = {
  course_type: "external_teacher",
  fees: [
    { fee_type: "entire_course", amount: 50, extra_fee_cash: 0, extra_fee_external: 0, fee_type_display: "Entire Course" },
    { fee_type: "single_session", amount: 30, extra_fee_cash: 0, extra_fee_external: 0, fee_type_display: "Single Session" },
  ],
};

describe("Registration form tests", () => {
  beforeAll(() => {
    document.body.innerHTML = `
      <input type="checkbox" id="entire-course">
      <input type="checkbox" id="entire-course-without-dan-preparation">
      <div id="id_selected_sessions">
        <input type="checkbox" id="checkbox1" data-dan-preparation="False" data-date="2024-01-01">
        <input type="checkbox" id="checkbox2" data-dan-preparation="False" data-date="2024-01-01">
      </div>
      <input type="checkbox" id="id_accept_terms">
      <button id="submit-button"></button>
      <div id="final-fee-display"></div>
      <span id="session-validation-msg"></span>
      <span id="terms-validation-msg"></span>
    `;
    // Only import the functions, after creating the dom elements.
    // This was a tough one to debug ...
    source = require("../../static/js/registration_form");
  });

  describe("Checkbox sync", () => {
    test("session checkboxes are checked when entire course checkbox is checked", () => {
      checkbox1.checked = checkbox2.checked = false;
      source.entireCourseCheckbox.checked = true;
      source.checkSessionCheckboxes();
      expect(checkbox1.checked).toBe(true);
      expect(checkbox2.checked).toBe(true);
    });

    test("session checkboxes are unckhecked when entire course checkbox is unchecked", () => {
      checkbox1.checked = checkbox2.checked = true;
      source.entireCourseCheckbox.checked = false;
      source.checkSessionCheckboxes();
      expect(checkbox1.checked).toBe(false);
      expect(checkbox2.checked).toBe(false);
    });

    test("Entire course checkbox is checked when all session checkboxes are checked", () => {
      checkbox1.checked = checkbox2.checked = true;
      source.checkEntireCourseCheckbox();
      expect(source.entireCourseCheckbox.checked).toBe(true);
    });

    test("Entire course checkbox is unchecked when a session checkboxes is unchecked", () => {
      source.entireCourseCheckbox.checked = true;
      checkbox1.checked = false;
      checkbox2.checked = true;
      source.checkEntireCourseCheckbox();
      expect(source.entireCourseCheckbox.checked).toBe(false);
    });
  });

  describe("Final fee calculation", () => {
    test("Final fee equals course fee if entire course is selected", () => {
      checkbox1.checked = checkbox2.checked = true;
      document.getElementById("entire-course-without-dan-preparation").checked = true;
      const result = source.calculateFinalFee(courseData);
      expect(result.finalFee).toEqual(50);
    });

    test("Final fee equals add fees of all selected sessions", () => {
      source.entireCourseCheckbox.checked = false;
      document.getElementById("entire-course-without-dan-preparation").checked = false;
      checkbox1.checked = true;
      checkbox2.checked = false;
      const result = source.calculateFinalFee(courseData);
      expect(result.finalFee).toEqual(30);
    });
  });

  describe("Disable Submit button", () => {
    test("Submit button is disabled if no sessions are selected", () => {
      checkbox1.checked = checkbox2.checked = source.entireCourseCheckbox = false;
      source.disableSubmitButton();
      expect(source.submitButton.classList.contains("disabled")).toBe(true);
    });

    test("Submit button is disabled if accept terms checkbox is not checked", () => {
      source.acceptTermsCheckbox.checked = false;
      source.disableSubmitButton();
      expect(source.submitButton.classList.contains("disabled")).toBe(true);
    });

    test("Submit button is enabled if accept terms checkbox is checked and at least one session is selected", () => {
      checkbox1.checked = true;
      source.acceptTermsCheckbox.checked = true;
      source.disableSubmitButton();
      expect(source.submitButton.classList.contains("disabled")).toBe(false);
    });

    test("session validation messages are displayed", () => {
      checkbox1.checked = checkbox2.checked = false;
      source.disableSubmitButton();
      expect(source.sessionMsg.style.display).toBe("inline");
      checkbox1.checked = true;
      source.disableSubmitButton();
      expect(source.sessionMsg.style.display).toBe("none");
    })

    test("terms validation messages are displayed", () => {
      source.acceptTermsCheckbox.checked = false;
      source.disableSubmitButton();
      expect(source.termsMsg.style.display).toBe("inline");
      source.acceptTermsCheckbox.checked = true;
      source.disableSubmitButton();
      expect(source.termsMsg.style.display).toBe("none");
    })
  });

  describe("DAN Preparation sessions", () => {
    test("updateEntireCourseWithoutDanPreparation checks all regular sessions are selected", () => {
      const entireCourseWithoutDanPreparation = document.getElementById("entire-course-without-dan-preparation");

      // Check all regular sessions (checkbox1 and checkbox2 have data-dan-preparation="False")
      checkbox1.checked = true;
      checkbox2.checked = true;

      source.updateEntireCourseWithoutDanPreparation();
      expect(entireCourseWithoutDanPreparation.checked).toBe(true);
    });

    test("updateEntireCourse checks if all sessions selected", () => {
      const entireCourse = document.getElementById("entire-course");

      // All sessions checked
      checkbox1.checked = true;
      checkbox2.checked = true;

      source.updateEntireCourse();
      expect(entireCourse.checked).toBe(true);

      // One unchecked
      checkbox1.checked = false;
      source.updateEntireCourse();
      expect(entireCourse.checked).toBe(false);
    });
  });

});

