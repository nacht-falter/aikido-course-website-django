function checkDojo() {
  if (dojoSelect.value != "other") {
    otherDojoDiv.style.display = "none";
    otherDojoInput.value = "Other Dojo";
    otherDojoInput.removeAttribute("required");
  } else {
    otherDojoDiv.style.display = "block";
    otherDojoInput.value = "";
    otherDojoInput.setAttribute("required", "required");
  }
}

const dojoSelect = document.getElementById("id_dojo");
const otherDojoDiv = document.getElementById("div_id_other_dojo");
const otherDojoInput = document.getElementById("id_other_dojo");

dojoSelect.addEventListener("change", checkDojo);

checkDojo();
