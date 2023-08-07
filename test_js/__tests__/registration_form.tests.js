let source;
let courseData = {
  course_fee: 50,
  session_0_fee: 30,
  session_1_fee: 30,
};

describe("Registration form tests", () => {
  beforeAll(() => {
    document.body.innerHTML = `
      <input type"checkbox" id="entire-course">
      <div id="id_selected_sessions">
        <input type="checkbox" id="checkbox1">
        <input type="checkbox" id="checkbox2">
      </div>
      <input type="checkbox" id="id_accept_terms">
      <button id="submit-button"></button>
      <div id="final-fee-display"></div>
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
      source.entireCourseCheckbox.checked = true;
      source.calculateFinalFee(courseData);
      expect(source.finalFeeDisplay.innerText).toEqual(courseData.course_fee);
    });

    test("Final fee equals add fees of all selected sessions", () => {
      source.entireCourseCheckbox.checked = false;
      checkbox1.checked = true;
      checkbox2.checked = false;
      source.calculateFinalFee(courseData);
      expect(source.finalFeeDisplay.innerText).toEqual(courseData.session_0_fee);
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
  });
});
