function checkDojo() {
  if (dojoSelect.value != "other") {
    otherDojoDiv.style.display = "none";
  } else {
    otherDojoDiv.style.display = "block";
  }
}

const dojoSelect = document.getElementById("id_dojo");
const otherDojoDiv = document.getElementById("div_id_other_dojo");
const otherDojoInput = document.getElementById("id_other_dojo");

dojoSelect.addEventListener("change", checkDojo);

checkDojo();
