// Open accordion item if course is targeted from url
if (document.getElementById("accordion")) {
  // Get Course id from url:
  // https://stackoverflow.com/a/1036564
  const id = location.hash.replace("#", "");
  console.log(id);
  let item = document.getElementById(`button-${id}`);
  if (item) {
  item.click();
  }
}

// Auto close messages (Instructions from CI DjangoBlog tutorial)
setTimeout(function () {
  let messages = document.getElementById("msg");
  let alert = new bootstrap.Alert(messages);
  alert.close();
}, 3500);
