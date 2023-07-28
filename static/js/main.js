/**
 * Show accordion item if it is targeted from id in url
 */
function showAccordionItem() {
  if (document.getElementById("accordion")) {
    // Get Course id from url:
    // https://stackoverflow.com/a/1036564
    const id = location.hash.replace("#", "");
    let item = document.getElementById(`button-${id}`);
    if (item) {
      item.click();
    }
  }
}

/**
 * Auto close messages (Adapted from CI DjangoBlog tutorial)
 */
function autoCloseMessages() {
  let messages = document.getElementsByClassName("msg");
  let timeoutDelay = 3000;
  for (let message of messages) {
    setTimeout(function() {
      message.remove();
    }, timeoutDelay);
    timeoutDelay += 3000;
  }
}

showAccordionItem();
autoCloseMessages();

module.exports = { showAccordionItem, autoCloseMessages };
