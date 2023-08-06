module.exports = {
  roots: ["static/js", "test_js"],
  collectCoverage: true,
  collectCoverageFrom: ["static/js/**/*.js", "!static/js/**/*.spec.js", "test_js/**/*.js"],
  testEnvironment: "jsdom",
};
