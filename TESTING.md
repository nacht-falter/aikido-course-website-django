# Testing
## Automated Testing
The Python and JavaScript code written for the project has been tested by writing automated unit tests and measuring code coverage. Since even 100% code coverage is no guarantee for bug-free code, thorough [manual tests](#manual-testing) have been conducted as well.

### Python Testing
All Python code written for the project has been tested by writing automated unit tests using [unittest](https://docs.python.org/3/library/unittest.html#module-unittest).
Code coverage has been measured using [Coverage.py](https://coverage.readthedocs.io/en/latest/#). Code coverage of 100% has been achieved.

IMAGE: COVERAGE REPORT

### JavaScript Testing
All JavaScript code written for the project has been tested by writing automated tests using [Jest](https://jestjs.io/). 98% of the JavaScript code where covered by the tests.

IMAGE: COVERAGE REPORT

## Manual Testing
- The website was manually tested on a variety of devices (desktop, laptop, tablet, and smartphone) and browsers. The following browsers and operating systems have been tested:
  - Linux: Firefox, Google Chrome
  - macOS: Safari
  - Microsoft Windows: Microsoft Edge
  - iOS: Safari, Firefox
  
- The website is working as expected in all tested browsers.
- All links, buttons and forms were thoroughly tested to make sure they work as expected.
- Friends and family members were asked to review the application and documentation to point out any bugs or user experience issues.

## Validators and Linters
### W3C Validators
Both HTML and CSS pass the [W3C Markup Validator](https://validator.w3.org) and [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) with no errors:
- [W3C Markup Validator results](https://validator.w3.org/nu/?doc=https%3A%2F%2Faikido-course-website-django-ddffe52bc952.herokuapp.com%2F) 
- [W3C CSS Validator results](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdlbwcrs5v%2Fraw%2Fupload%2Fv1%2Fstatic%2Fcss%2Fstyle.6bea1ea32948.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en) (The W3C validator does not work with Bootstrap, only the custom CSS code in style.css has been validated)

### PEP 8 Linter
All python code written for the project passes through the PEP 8 [python linter](https://pep8ci.herokuapp.com/) by Code Institute with no issues.

#### Jshint
All JavaScript code was validated with the [Jshint linter](https://jshint.com/). All code passed with no errors.
   
### Chrome Lighthouse
A report on the application website generated with [Chrome Lighthouse](https://developer.chrome.com/docs/lighthouse/) showed no major issues with the performance or accessibility of the application.

![Lighthouse results summary](media/testing/)
[Detailed Chrome Lighthouse results](media/testing/)

### WAVE
[WAVE (Web Accessibility Evaluation Tool)](https://wave.webaim.org/) was used to asses the website's accessibility. The test resulst showed no errors.

IMAGE: RESULTS

## User Story Tests
All user stories have been tested to make sure that the project requirements are met: [User story test results](testing/text-inspector-user-story-test.md)

## Known limitations

...
