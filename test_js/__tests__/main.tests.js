const { showAccordionItem, autoCloseMessages } = require("../../static/js/main");

describe("Accordion item clicked", () => {
  test("test accordionItem is clicked", () => {
    const accordionContainer = document.createElement("div");
    accordionContainer.id = "accordion";
    document.body.appendChild(accordionContainer);

    let accordionItem = document.createElement("button");
    accordionItem.id = "button-1";
    accordionItem.addEventListener("click", function () {
      this.clicked = true;
    });

    accordionContainer.appendChild(accordionItem);
    location.hash = "#1";
    showAccordionItem();
    expect(accordionItem.clicked).toBeTruthy;

    location.hash = "#2";
    showAccordionItem();
    expect(accordionItem.clicked).toBeFalsy;
  });
});

describe("Auto close messages", () => {
  test("autoCloseMessages closes messages", () => {
    // Documentation: https://jestjs.io/docs/timer-mocks
    document.body.innerHTML = `
    <div class="msg">Message 1</div>
    <div class="msg">Message 2</div>
  `;
    jest.useFakeTimers();
    jest.spyOn(global, "setTimeout");
    autoCloseMessages();
    jest.runAllTimers();
    expect(setTimeout).toHaveBeenCalledTimes(2);
    expect(setTimeout).toHaveBeenLastCalledWith(expect.any(Function), 5000);
    const messages = document.getElementsByClassName("msg");
    expect(messages.length).toBe(0);
  });
});
