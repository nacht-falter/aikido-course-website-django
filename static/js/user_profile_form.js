function checkDojo() {
  if (dojoSelect.value != "other") {
    otherDojoDiv.style.display = "none";
    otherDojoInput.value = "Other Dojo";
  } else {
    otherDojoDiv.style.display = "block";
    otherDojoInput.value = "";
  }
}

const dojoSelect = document.getElementById("id_dojo");
const otherDojoDiv = document.getElementById("div_id_other_dojo");
const otherDojoInput = document.getElementById("id_other_dojo");

// Add eventListener
dojoSelect.addEventListener("change", checkDojo);

checkDojo();
