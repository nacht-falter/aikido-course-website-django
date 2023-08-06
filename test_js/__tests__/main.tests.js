const { autoCloseMessages } = require("../../static/js/main");

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
    expect(setTimeout).toHaveBeenLastCalledWith(expect.any(Function), 6000);
    const messages = document.getElementsByClassName("msg");
    expect(messages.length).toBe(0);
  });
});
