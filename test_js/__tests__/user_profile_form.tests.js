let source;

describe("User Profile Form - Dojo Selection", () => {
  beforeAll(() => {
    // Create DOM structure once before all tests
    document.body.innerHTML = `
      <select id="id_dojo">
        <option value="">Select your Dojo</option>
        <option value="AAR">Aikido am Rhein</option>
        <option value="AVE">Aikido Verein Emmendingen</option>
        <option value="other">Other Dojo</option>
      </select>
      <div id="div_id_other_dojo" style="display: none;">
        <input type="text" id="id_other_dojo" name="other_dojo">
      </div>
    `;

    // Import module after DOM is ready
    // Only import once - this was a tough one to debug ...
    source = require("../../static/js/user_profile_form");
  });

  test("other_dojo field is hidden when regular dojo is selected", () => {
    const dojoSelect = document.getElementById("id_dojo");
    const otherDojoDiv = document.getElementById("div_id_other_dojo");
    const otherDojoInput = document.getElementById("id_other_dojo");

    // Select a regular dojo
    dojoSelect.value = "AAR";
    source.checkDojo();

    expect(otherDojoDiv.style.display).toBe("none");
    expect(otherDojoInput.hasAttribute("required")).toBe(false);
  });

  test("other_dojo field is shown when 'other' is selected", () => {
    const dojoSelect = document.getElementById("id_dojo");
    const otherDojoDiv = document.getElementById("div_id_other_dojo");
    const otherDojoInput = document.getElementById("id_other_dojo");

    // Select "other"
    dojoSelect.value = "other";
    source.checkDojo();

    expect(otherDojoDiv.style.display).toBe("block");
    expect(otherDojoInput.hasAttribute("required")).toBe(true);
    expect(otherDojoInput.getAttribute("required")).toBe("required");
  });

  test("switching from 'other' to regular dojo hides field and removes required", () => {
    const dojoSelect = document.getElementById("id_dojo");
    const otherDojoDiv = document.getElementById("div_id_other_dojo");
    const otherDojoInput = document.getElementById("id_other_dojo");

    // Start with "other" selected
    dojoSelect.value = "other";
    source.checkDojo();
    expect(otherDojoDiv.style.display).toBe("block");
    expect(otherDojoInput.hasAttribute("required")).toBe(true);

    // Switch to regular dojo
    dojoSelect.value = "AVE";
    source.checkDojo();

    expect(otherDojoDiv.style.display).toBe("none");
    expect(otherDojoInput.hasAttribute("required")).toBe(false);
  });

  test("initial state with empty selection hides other_dojo field", () => {
    const dojoSelect = document.getElementById("id_dojo");
    const otherDojoDiv = document.getElementById("div_id_other_dojo");
    const otherDojoInput = document.getElementById("id_other_dojo");

    // Empty/default selection
    dojoSelect.value = "";
    source.checkDojo();

    expect(otherDojoDiv.style.display).toBe("none");
    expect(otherDojoInput.hasAttribute("required")).toBe(false);
  });

  test("change event listener triggers checkDojo when dojo selection changes", () => {
    const dojoSelect = document.getElementById("id_dojo");
    const otherDojoDiv = document.getElementById("div_id_other_dojo");

    // Start with regular dojo
    dojoSelect.value = "AAR";
    dojoSelect.dispatchEvent(new Event("change"));
    expect(otherDojoDiv.style.display).toBe("none");

    // Change to "other"
    dojoSelect.value = "other";
    dojoSelect.dispatchEvent(new Event("change"));
    expect(otherDojoDiv.style.display).toBe("block");
  });
});
