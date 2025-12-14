function checkDojo() {
  if (dojoSelect.value !== "other") {
    otherDojoDiv.style.display = "none";
    otherDojoInput.removeAttribute("required");
  } else {
    otherDojoDiv.style.display = "block";
    otherDojoInput.setAttribute("required", "required");
  }
}

const dojoSelect = document.getElementById("id_dojo");
const otherDojoDiv = document.getElementById("div_id_other_dojo");
const otherDojoInput = document.getElementById("id_other_dojo");

if (dojoSelect) {
  dojoSelect.addEventListener("change", checkDojo);
  checkDojo();
}

// Export for testing
if (typeof module !== "undefined" && module.exports) {
  module.exports = { checkDojo };
}
