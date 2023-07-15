/**
 * Check/uncheck all sessions if entire course box is checked/unchecked
 */
function checkSessionCheckboxes() {
  for (let checkbox of sessionsCheckboxes) {
    checkbox.checked = entireCourseCheckbox.checked;
  }
  calculateFinalFee();
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
  calculateFinalFee();
}

/**
 * Calculate the final fee and display it
 */
function calculateFinalFee() {
  let finalFee = 0;
  if (entireCourseCheckbox.checked) {
    finalFee = course_data.course_fee;
  } else {
    let i = 0;
    for (let checkbox of sessionsCheckboxes) {
      if (checkbox.checked) {
        let sessionFee = course_data[`session_${i}_fee`];
        finalFee += sessionFee;
      }
      i++;
    }
  }
  finalFeeDisplay.innerText = finalFee;
}

// Receiving data from the template. Instructions from: https://adamj.eu/tech/
// 2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
const course_data = JSON.parse(document.currentScript.nextElementSibling.textContent);

const finalFeeDisplay = document.getElementById("final-fee-display");
const entireCourseCheckbox = document.getElementById("entire-course");
const sessionsList = document.getElementById("id_selected_sessions");
const sessionsCheckboxes = sessionsList.querySelectorAll("input");

// Add event listeners to checkboxes:
entireCourseCheckbox.addEventListener("click", checkSessionCheckboxes);
for (let checkbox of sessionsCheckboxes) {
  checkbox.addEventListener("click", checkEntireCourseCheckbox);
}
