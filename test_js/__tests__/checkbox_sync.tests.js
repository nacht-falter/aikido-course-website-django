/**
 * Comprehensive tests for checkbox synchronization logic in registration form
 *
 * This is critical logic that affects fee calculation and user experience.
 * The form has three types of checkboxes:
 * 1. Individual session checkboxes (regular and DAN preparation)
 * 2. "Entire course without DAN preparation" checkbox
 * 3. "Entire course" checkbox (includes DAN preparation sessions)
 */

let source;

describe("Registration Form - Checkbox Synchronization", () => {
  beforeAll(() => {
    // Set up a realistic DOM with regular and DAN preparation sessions
    document.body.innerHTML = `
      <input type="checkbox" id="entire-course">
      <input type="checkbox" id="entire-course-without-dan-preparation">
      <div id="id_selected_sessions">
        <input type="checkbox" id="session1" data-dan-preparation="False" data-date="2024-01-01">
        <input type="checkbox" id="session2" data-dan-preparation="False" data-date="2024-01-02">
        <input type="checkbox" id="dan-session1" data-dan-preparation="True" data-date="2024-01-03">
        <input type="checkbox" id="dan-session2" data-dan-preparation="True" data-date="2024-01-04">
      </div>
      <input type="checkbox" id="id_accept_terms">
      <button id="submit-button"></button>
      <div id="final-fee-display"></div>
      <div id="final-fee-info"></div>
      <div id="sticky-fee-row"></div>
      <span id="session-validation-msg"></span>
      <span id="terms-validation-msg"></span>
    `;

    // Provide minimal courseData via script tag (same way the real page does it)
    // The pattern from Adam Johnson's blog: script tag followed by JSON script tag
    const script = document.createElement("script");
    script.src = "/static/js/registration_form.js";

    const dataScript = document.createElement("script");
    dataScript.type = "application/json";
    dataScript.textContent = JSON.stringify({
      course_type: "external_teacher",
      course_has_dan_preparation: true,
      fees: [
        { fee_type: "entire_course", amount: 100, extra_fee_cash: 0, extra_fee_external: 0, fee_type_display: "Entire Course" },
        { fee_type: "entire_course_dan_preparation", amount: 120, extra_fee_cash: 0, extra_fee_external: 0, fee_type_display: "Entire Course with DAN Prep" },
        { fee_type: "single_session", amount: 30, extra_fee_cash: 0, extra_fee_external: 0, fee_type_display: "Single Session" },
      ],
    });

    document.head.appendChild(script);
    document.head.appendChild(dataScript);

    // Mock document.currentScript to return the script tag (with dataScript as nextElementSibling)
    Object.defineProperty(document, "currentScript", {
      value: script,
      writable: true,
      configurable: true,
    });

    source = require("../../static/js/registration_form");
  });

  describe("Entire Course checkbox behavior", () => {
    test("checking 'Entire Course' selects ALL sessions (regular + DAN)", () => {
      const entireCourse = document.getElementById("entire-course");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Start with all unchecked
      session1.checked = false;
      session2.checked = false;
      danSession1.checked = false;
      danSession2.checked = false;
      entireCourse.checked = true;

      // Call the REAL handler function
      source.handleEntireCourseChange();

      // All sessions should be checked
      expect(session1.checked).toBe(true);
      expect(session2.checked).toBe(true);
      expect(danSession1.checked).toBe(true);
      expect(danSession2.checked).toBe(true);
    });

    test("unchecking 'Entire Course' unselects ALL sessions", () => {
      const entireCourse = document.getElementById("entire-course");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Start with all checked
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = true;
      danSession2.checked = true;
      entireCourse.checked = false;

      // Call the REAL handler function
      source.handleEntireCourseChange();

      // All sessions should be unchecked
      expect(session1.checked).toBe(false);
      expect(session2.checked).toBe(false);
      expect(danSession1.checked).toBe(false);
      expect(danSession2.checked).toBe(false);
    });

    test("manually selecting all sessions auto-checks 'Entire Course'", () => {
      const entireCourse = document.getElementById("entire-course");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Manually check all sessions
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = true;
      danSession2.checked = true;

      source.updateEntireCourse();

      // Entire course should auto-check
      expect(entireCourse.checked).toBe(true);
    });

    test("unchecking one session auto-unchecks 'Entire Course'", () => {
      const entireCourse = document.getElementById("entire-course");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Start with all checked
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = true;
      danSession2.checked = true;
      entireCourse.checked = true;

      // Uncheck one session
      session2.checked = false;

      source.updateEntireCourse();

      // Entire course should auto-uncheck
      expect(entireCourse.checked).toBe(false);
    });
  });

  describe("Entire Course Without DAN Preparation checkbox behavior", () => {
    test("checking 'Without DAN' selects only regular sessions, not DAN sessions", () => {
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const entireCourse = document.getElementById("entire-course");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Start with all unchecked
      session1.checked = false;
      session2.checked = false;
      danSession1.checked = false;
      danSession2.checked = false;
      entireCourseWithoutDan.checked = true;

      // Call the REAL handler function
      source.handleEntireCourseWithoutDanPreparationChange();

      // Only regular sessions should be checked
      expect(session1.checked).toBe(true);
      expect(session2.checked).toBe(true);
      expect(danSession1.checked).toBe(false);
      expect(danSession2.checked).toBe(false);
      // Entire course should be unchecked (mutually exclusive)
      expect(entireCourse.checked).toBe(false);
    });

    test("unchecking 'Without DAN' unselects regular sessions", () => {
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");

      // Start with regular sessions checked
      session1.checked = true;
      session2.checked = true;
      entireCourseWithoutDan.checked = false;

      // Call the REAL handler function
      source.handleEntireCourseWithoutDanPreparationChange();

      // Regular sessions should be unchecked
      expect(session1.checked).toBe(false);
      expect(session2.checked).toBe(false);
    });

    test("manually selecting all regular sessions (no DAN) auto-checks 'Without DAN'", () => {
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Manually check all regular sessions, not DAN
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = false;
      danSession2.checked = false;

      source.updateEntireCourseWithoutDanPreparation();

      // 'Without DAN' should auto-check
      expect(entireCourseWithoutDan.checked).toBe(true);
    });

    test("selecting a DAN session auto-unchecks 'Without DAN'", () => {
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");

      // Start with all regular sessions checked
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = false;
      entireCourseWithoutDan.checked = true;

      // Now check a DAN session
      danSession1.checked = true;

      source.updateEntireCourseWithoutDanPreparation();

      // 'Without DAN' should auto-uncheck
      expect(entireCourseWithoutDan.checked).toBe(false);
    });

    test("unchecking one regular session auto-unchecks 'Without DAN'", () => {
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");

      // Start with all regular sessions checked
      session1.checked = true;
      session2.checked = true;
      entireCourseWithoutDan.checked = true;

      // Uncheck one regular session
      session2.checked = false;

      source.updateEntireCourseWithoutDanPreparation();

      // 'Without DAN' should auto-uncheck
      expect(entireCourseWithoutDan.checked).toBe(false);
    });
  });

  describe("Interaction between 'Entire Course' and 'Without DAN' checkboxes", () => {
    test("checking 'Entire Course' also updates 'Without DAN' appropriately", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Check entire course (which checks all sessions including DAN)
      entireCourse.checked = true;

      // Call the REAL handler function
      source.handleEntireCourseChange();

      // All sessions are now checked (regular + DAN)
      expect(session1.checked).toBe(true);
      expect(session2.checked).toBe(true);
      expect(danSession1.checked).toBe(true);
      expect(danSession2.checked).toBe(true);

      // 'Without DAN' should be FALSE because DAN sessions are selected
      // (handleEntireCourseChange calls updateEntireCourseWithoutDanPreparation internally)
      expect(entireCourseWithoutDan.checked).toBe(false);
    });

    test("checking 'Without DAN' ensures 'Entire Course' is unchecked", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");

      // Start with entire course checked
      entireCourse.checked = true;

      // Check 'Without DAN'
      entireCourseWithoutDan.checked = true;

      // Call the REAL handler function
      source.handleEntireCourseWithoutDanPreparationChange();

      // 'Entire Course' should be unchecked (explicitly set in the handler)
      expect(entireCourse.checked).toBe(false);
    });

    test("manually selecting all sessions checks 'Entire Course' but not 'Without DAN'", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Manually select all sessions
      session1.checked = true;
      session2.checked = true;
      danSession1.checked = true;
      danSession2.checked = true;

      source.updateEntireCourse();
      source.updateEntireCourseWithoutDanPreparation();

      // 'Entire Course' should be checked
      expect(entireCourse.checked).toBe(true);
      // 'Without DAN' should NOT be checked (because DAN sessions are selected)
      expect(entireCourseWithoutDan.checked).toBe(false);
    });
  });

  describe("Edge cases and partial selections", () => {
    test("selecting only DAN sessions doesn't check either master checkbox", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Select only DAN sessions
      session1.checked = false;
      session2.checked = false;
      danSession1.checked = true;
      danSession2.checked = true;

      source.updateEntireCourse();
      source.updateEntireCourseWithoutDanPreparation();

      // Neither master checkbox should be checked
      expect(entireCourse.checked).toBe(false);
      expect(entireCourseWithoutDan.checked).toBe(false);
    });

    test("selecting mix of regular and DAN sessions doesn't check either master checkbox", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const danSession1 = document.getElementById("dan-session1");

      // Select one regular and one DAN
      session1.checked = true;
      danSession1.checked = true;

      source.updateEntireCourse();
      source.updateEntireCourseWithoutDanPreparation();

      // Neither master checkbox should be checked
      expect(entireCourse.checked).toBe(false);
      expect(entireCourseWithoutDan.checked).toBe(false);
    });

    test("no sessions selected means no master checkboxes checked", () => {
      const entireCourse = document.getElementById("entire-course");
      const entireCourseWithoutDan = document.getElementById("entire-course-without-dan-preparation");
      const session1 = document.getElementById("session1");
      const session2 = document.getElementById("session2");
      const danSession1 = document.getElementById("dan-session1");
      const danSession2 = document.getElementById("dan-session2");

      // Uncheck all
      session1.checked = false;
      session2.checked = false;
      danSession1.checked = false;
      danSession2.checked = false;

      source.updateEntireCourse();
      source.updateEntireCourseWithoutDanPreparation();

      // Neither master checkbox should be checked
      expect(entireCourse.checked).toBe(false);
      expect(entireCourseWithoutDan.checked).toBe(false);
    });
  });
});
