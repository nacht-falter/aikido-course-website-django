# User Story Tests
All user stories have been tested to make sure that the project requirements are met.

## THEME: User Accounts and Profiles

### EPIC: User Registration and Authentication

#### 👉 USER STORY: As a **visitor**, I can **create a user account** so that I can **log in and store my information** (https://github.com/nacht-falter/aikido-course-website-django/issues/2)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria:

- [x] There is a Sign Up button accessible from everywhere on the website
- [x] Upon clicking on the Sign Up button a user registration form is displayed
- [x] Upon successful registration a new user is created in the database.

##### Tasks:

- [x] Install and setup Django-allauth
- [x] Create UserProfile model with additional fields
- [x] Add Sign Up button to base template and link to allauth registration form
- [x] Create user profile view
- [x] Create user profile template
- [x] Create user profile form

</details>


#### 👉 USER STORY: As a **user**, I can **log in to my account** by **clicking on a login button from anywhere on the Website** (https://github.com/nacht-falter/aikido-course-website-django/issues/3)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a login button, which is accessible from everywhere on the website.
- [x] Upon clicking on the button the user is presented with a form for loggingn in with their user credentials.

##### Tasks
- [x] Add login button to base template
- [x] Create login form 

</details>



#### 👉 USER STORY: As a **user**, I can **log out from my account** by **clicking on a Logout button from anywhere on the website**. (https://github.com/nacht-falter/aikido-course-website-django/issues/4)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a logout button accessible from anywhere on the website
- [x] Upon clicking on the logout button the user is logged out from the system.

##### Tasks
- [x] Add logout button to base template
- [x] Show logout button only for authenticated users

</details>


#### 👉 USER STORY: As a **user**, I can **receive an email** as **confirmation when I create a user account**. (https://github.com/nacht-falter/aikido-course-website-django/issues/5)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 8](https://github.com/nacht-falter/aikido-course-website-django/milestone/25?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] After creating an account the user will receive an e-mail as confirmation.
- [x] The email contains relevant details about the account and a confirmation message.

##### Tasks
- [x] Set up email functionality in Django
- [x] Send confirmation e-mail after account creation
- [x] Create sendmail function in view to send the confirmation email upon successful account creation

</details>

<hr>

### EPIC: User Account Management

#### 👉 USER STORY: As a **logged-in user**, I can **view my user profile** (https://github.com/nacht-falter/aikido-course-website-django/issues/6)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a link in the navigation for logged in user which brings them to their user profile.
- [x] The user profile displays user data and includes a link to the user's course registration list. 

##### Tasks
- [x] Create UserProfile model to extend User model
- [x] Create view for user profiles
- [x] Update template for user profile
- [x] Update base template
- [x] Test model and view

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **update my user profile** (https://github.com/nacht-falter/aikido-course-website-django/issues/7)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] A user can click on a link to edit the user's profile on the profile page.
- [x] Upon clicking that link, a form for editing the user's data will appear.
- [x] After submitting the form the updated data is stored in the database.

##### Tasks
- [x] Create form for editing user profile with the following fields: first name, last name, username, email, grade
- [x] Create view for editing the profile
- [x] Register urls
- [x] Write tests

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **reset my password** (https://github.com/nacht-falter/aikido-course-website-django/issues/8)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 4](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Users can reset their password by clicking on a link on their profile page

##### Tasks
- [x] Include link to account_change_password url from allauth in user profile template
- [x] Adjust allauth change password template

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **delete my account** (https://github.com/nacht-falter/aikido-course-website-django/issues/9)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Users can delete or deactivate their account by clicking on a link
- [x] After the user confirms they want to delete/deactivate the account, the user will be removed from the system

##### Tasks
- [x] Create deactivate user view
- [x] Create deactivate user template
- [x] Write tests for view

</details>


#### 👉 USER STORY: As a **logged-in user**, I can receive an email as confirmation when I delete my account (https://github.com/nacht-falter/aikido-course-website-django/issues/10)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] Users receive an email as confirmation, when they have deactivated their account.

##### Tasks
- [ ] Add sendemail function to DeactivateAccount view

</details>

<hr>

## THEME: Course Registration and Management

### EPIC: Course Registration

#### 👉 USER STORY: As a **visitor**, I can **click on a link in the navigation menu** to **see a list of available courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/11)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 1](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a list of all courses available at a URL.
- [x] Theres is a navigation menu containing a link to the URL to the course list.

##### Tasks
- [x] Create course list view
- [x] Create base template with navigation menu containing a link to the course list page
- [x] Create course list template
- [x] Register URL
- [x] Test view

</details>


#### 👉 USER STORY: As a **visitor**, I can **fill out a registration form** to **sign up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/12)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>


##### Acceptance Criteria
- [ ] A visitor can sign up for courses without having to create a user account.
- [ ] The registration will be saved in the database upon submitting a registration form.

##### Tasks
- [ ] Create model for visitor registrations
- [ ] Create registration form and view
- [ ] Add template

</details>


#### 👉 USER STORY: As a **visitor** or a **logged-in user**, I can **see the fees for the course, depending on how many sessions I have selected** (https://github.com/nacht-falter/aikido-course-website-django/issues/13)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

Completed in [Sprint 4](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Upon filling out a course registration form the user can see, what the course fees will be.
- [x] The course fees change, depending on if the user selects single sessions or the entire course.
- [x] The course fee will be stored with the registration upon submitting the form.

##### Tasks
- [x] Add course sessions to course registration form
- [x] Create logic for calculating the course fees to the post method of the course registration view.
- [x] Add javascript to the template in order to display the fees dynamically.
- [x] Write tests for view

</details>


#### 👉 USER STORY: As a **visitor** or a **logged-in user**, I can **receive an email as confirmation**, **after signing up for a course, containing course and payment details so that I have a backup of all relevant details** (https://github.com/nacht-falter/aikido-course-website-django/issues/14)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 8](https://github.com/nacht-falter/aikido-course-website-django/milestone/25?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] After signing up for a course users will receive an email confirming the successful registration.
- [x] The email contains details about the course and the registration.

##### Tasks
- [x] Update RegisterCourse view to send email upon successful registration
- [x] Include course and registration details in email

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **fill out a sign-up form** to **sign up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/43)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 2](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] A logged-in user can click on a link in the course with open registration status and will be directed to to a registration form.
- [x] The registration-form provides fields for all necessary details.
- [x] Upon filling out the form, a new registration will be stored in the database.

##### Tasks
- [x] Create course registration form
- [x] Create registration form template
- [x] Create view
- [x] Register url
- [x] Write tests for form and view

</details>

<hr>

### EPIC: Course Registration Management

#### 👉 USER STORY: As a **logged-in user**, I can **see a list of my current and past registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/15)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 2](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] The user can see a list of their current and past registrations in separete sections of the registrations list.

##### Tasks
- [x] Update registration list template to separate between current and past registrations

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **edit my current registrations** so that **I can update information** (https://github.com/nacht-falter/aikido-course-website-django/issues/16)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 2](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1) ✓

<details>

<summary>Show details</summary>


##### Acceptance Criteria
- [x] Users can see a list of their current registrations.
- [x] Users can click on a current registration and be redirected to a form for editing their registration.
- [x] After submitting the form the updated data will be stored in the database.

##### Tasks
- [x] Create view to list registrations.
- [x] Create template for registration list with edit registration button.
- [x] Create view for editing registration
- [x] Test views

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **cancel a course registration** (https://github.com/nacht-falter/aikido-course-website-django/issues/17)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 2](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Users can see a list of their current registrations.
- [x] Users can cancel registrations by clicking on a cancel registration button.
- [x] Users will be asked for confirmation before the registration is cancelled.

##### Tasks
- [x] Create view to list registrations
- [x] Create view to delete registration
- [x] Create templates for registration list with cancel button and confirmation
- [x] Create navigation link to users registrations page
- [x] Register urls
- [x] Write tests for views

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **receive an email as confirmation when I updated a registration** (https://github.com/nacht-falter/aikido-course-website-django/issues/18)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] After updating a course registration the user wil receive an email with the updated information.

##### Tasks
- [ ] Add sendemail function to update course registration view

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **receive an email as confirmation when I canceled a registration.** (https://github.com/nacht-falter/aikido-course-website-django/issues/19)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] After cancelling a course registration a user receives an email as confirmation.

##### Tasks
- [ ] Add sendemail function to cancel registration view

</details>

<hr>

### EPIC: Exams

#### 👉 USER STORY: As a **visitor** or a **logged-in user**, I can **see if I applied for an exam after I signed up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/20)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 2](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] In the list of the users current registrations there is a message indicating if the user has applied for an exam.

##### Tasks
- [x] Add exam field to registration list template

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **cancel exam applications for current registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/21)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] In the users registrations list, there is a button for cancelling an exam application.
- [ ] Upon clicking the button, the user is asked to confirm the cancellation.
- [ ] After confirming the registration is updated with the new setting.

##### Tasks
- [ ] Update course registration template to display a button for cancelling an exam application
- [ ] Create confirmation template
- [ ] Create view
- [ ] Write tests for view

</details>


#### 👉 USER STORY: As a **logged-in user**, I can **receive a notification after logging in if I have previously applied for an exam** so that **I can update my user profile accordingly** (https://github.com/nacht-falter/aikido-course-website-django/issues/22)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

Completed in [Sprint 4](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] After applying for an exam and after the course has passed, the user will be presented with a dialogue asking if they want to update their grade.
- [x] If the user confirms that they passed their exam the registration will be updated to include the information in the exam_passed field.

##### Tasks
- [x] Add logic for checking if the user has applied for an exam and if the course has passed to user profile view
- [x] Create view for displaying the notification.
- [x] Add exam_passed field to CourseRegistration model
- [x] Display if exam has been passed in the course registration view
- [x] Write tests for views

</details>


#### 👉 USER STORY: As a **logged-in user**,I can **see what exam I applied for in the list of my past and current registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/45)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 4](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] If the user applied for an exam with a course registration, the grade they applied for is displayed with the registration in the course registration list.

##### Tasks
- [x] Display exam grade in course registration list template

</details>

<hr>

## THEME: Website UX

### EPIC: UI Design

#### 👉 USER STORY: As a **visitor** or a **logged-in user**, I want **the website to have a responsive, consistent and visually appealing UI design** in order to **elicit a positive response during my visit** (https://github.com/nacht-falter/aikido-course-website-django/issues/36)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

Completed in [Sprint 5](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] The website has a consistent layout and styling over all pages.
- [x] The website is responsive for different screen sizes.
- [x]The website uses colors and images which represent the organisation.

##### Tasks
- [x] Add bootstrap to base template
- [x] Create basic bootstrap layout and styling
- [x] Include images on the home page

</details>


#### 👉 USER STORY: As a **user**, I want **the website to comply with accessibility guidelines** so that **I can access it with screen readers or other assistive technologies** (https://github.com/nacht-falter/aikido-course-website-django/issues/55)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 6](https://github.com/nacht-falter/aikido-course-website-django/milestone/23?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] The templates use accessibility labels and elements where appropriate.

##### Tasks
- [x] Use aria-labels where necessary
- [x] Fix suggestions from 
- [x] User semantic html elements in base template

</details>


#### 👉 USER STORY: As a **visitor or logged-in user**,I can **see messages with different colors** so that **I can get feedback for my actions.** (https://github.com/nacht-falter/aikido-course-website-django/issues/56)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 5](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There are messages displayed, when the user submits forms.
- [x] The messages have different colors depending on their type. 

##### Tasks
- [x] Add bootstrap alert class to messages
- [x] Set up messages typse in settings.py
- [x] Add styling to alerts types

</details>


#### 👉 USER STORY: As a **visitor** or **logged-in user**,I want **to be able to see a list of pages with thumbnail images to visit** in the sidebar on the home page (https://github.com/nacht-falter/aikido-course-website-django/issues/65)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] There is a list of available pages on the home page for quick access.
- [ ] Pages include thumbnail images.

##### Tasks
- [ ] Update index.html template to include list of pages.
- [ ] Display pages with thumbnail (featured image)

</details>


#### 👉 USER STORY: As a **logged-in user**I can **see if I am logged in or not** (https://github.com/nacht-falter/aikido-course-website-django/issues/66)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 8](https://github.com/nacht-falter/aikido-course-website-django/milestone/25?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is an indicator on the website showing logged-in users, that they are logged in.

##### Tasks
- [x] Include indicator for authentication status in base.html template

</details>

<hr>

### EPIC: Navigation

#### 👉 USER STORY: As a **visitor** or **logged-in user**, I can **easily navigate through different sections of the website using a clear and intuitive navigation menu displayed on all pages** (https://github.com/nacht-falter/aikido-course-website-django/issues/23)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 5](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a navigation menu displayed on all pages.
- [x] The navigation menu is responsive so that it is easily accessible on all devices

##### Tasks
- [x] Add bootstrap classes and js to navigation in order to style it and make it responsive

</details>


#### 👉 USER STORY: As a **user**, I can **see a breadcrumb navigation on all pages** so that **I can see my current position on the website and easily navigate back to previous pages** (https://github.com/nacht-falter/aikido-course-website-django/issues/24)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] The user can see where they are on the website from a breadcrumb navigation, which is visible on all pages.

##### Tasks
- [ ] Add a navigation to base.html with a link to the current page, as well as links to parent pages such as categories and a link to the start page

</details>


#### 👉 USER STORY: As a **Visitor or logged-in user**,I can **see a custom error page with a link to the homepage**, when I try to access a URL that doesn't exist (https://github.com/nacht-falter/aikido-course-website-django/issues/50)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 7](https://github.com/nacht-falter/aikido-course-website-django/milestone/24?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a custom error page with a link to the homepage.
- [x] The page is displayed when a 404 error comes up instead of the default 404 error page.

##### Tasks
- [x] Create a custom 404 error template

</details>

<hr>

### EPIC: Website Content

#### 👉 USER STORY: As a **user**, I want **the start page to display information about the website's purpose** (https://github.com/nacht-falter/aikido-course-website-django/issues/25)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 5](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] The homepage includes information about the website's purpose and a short description.

##### Tasks
- [x] Add description of the organisation and the purpose of the website to the home page template

</details>


#### 👉 USER STORY: As a **user**, I want **the start page to display the latest courses and currently open course registrations** so that **I can quickly access them** (https://github.com/nacht-falter/aikido-course-website-django/issues/26)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Completed in [Sprint 5](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a list of upcoming courses on the home page.
- [x] Users can see which courses are open for registration.

##### Tasks
- [x] Add list of upcoming courses to index.html
- [x] Mark courses with open registrations with a badge

</details>


#### 👉 USER STORY: As a **user**, I want **the start page to display the latest courses and currently open course registrations** so that **I can quickly access them** (https://github.com/nacht-falter/aikido-course-website-django/issues/27)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 8](https://github.com/nacht-falter/aikido-course-website-django/milestone/25?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There are pages for accessing information about the organization accessible from the navigation menu.
- [x] There is a page with links to the websites of all Aikido Dojos which are part of the organization.
- [x] There is information available for beginners so that they can find out where they can start learning Aikido.

##### Tasks
- [x] Create pages for information about Aikido, about Danbw, about the Dojos, and for beginners
- [x] Include pages in navigation menu

</details>


#### 👉 USER STORY: As a **visitor or logged-in user**, I can **fill out a contact form** so that **I can get in touch with the team** (https://github.com/nacht-falter/aikido-course-website-django/issues/27)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 7](https://github.com/nacht-falter/aikido-course-website-django/milestone/24?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a contact page, which is accessible from the footer.
- [x] There is a contact form on the contact page, which allows users to contact the organization.

##### Tasks
- [x] Set up email backend
- [x] Create contact view
- [x] Create contact form
- [x] Create template

</details>


#### 👉 USER STORY: As a **visitor** or a **logged-in user,** I can **see a photo gallery with photos from past courses** so that **I can get some impressions of the courses.** (https://github.com/nacht-falter/aikido-course-website-django/issues/40)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] There is a photo gallery of past courses available on the website.
- [ ] Users and visitors can look at photos from different courses.

##### Tasks
- [ ] Create a Picture model with a foreign key to courses
- [ ] Create a view and a template for displaying pictures filtered by course as a picture gallery

</details>


#### 👉 USER STORY: As a **visitor** or **logged-in user**,I want **to be able to see a list of pages with thumbnail images to visit** in the sidebar on the home page (https://github.com/nacht-falter/aikido-course-website-django/issues/65)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] There is a list of available pages on the home page for quick access.
- [ ] Pages include thumbnail images.

##### Tasks
- [ ] Update index.html template to include list of pages.
- [ ] Display pages with thumbnail (featured image)

</details>

<hr>

## THEME: Staff functions

### EPIC: Course Management

#### 👉 USER STORY: As a **staff member**, I can **create new courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/30)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 1](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] A staff member can login to the Django backend and create new course items by clicking on 'Add Course' and fill out the course details
- [x] All form fields are validated according to their field type.
- [x] Slug field is auto completed

##### Tasks
- [x] Create Course model according to ERD (MVP version)
- [x] Register Course model in admin view
- [x] Add custom validation to date fields
- [x] Add auto fill method for slug field
- [x] Write tests for the model

</details>


#### 👉 USER STORY: As a **staff member**, I can **duplicate existing courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/31)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 1](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Staff members can see existing courses in the Django backend and duplicate a course by clicking on a course in the list and select a duplicate course method.

##### Tasks
- [x] Create method for course duplication and register it in the admin view
- [x] Write tests for duplication method

</details>


#### 👉 USER STORY: As a **staff member**, I can **update or delete existing courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/32)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 1](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] Staff members can update courses from the Django admin backend
- [x] Staff members can delete courses from the Django admin backend
- [x] Staff members can see the properties of existing courses in the django admin backend course list.

##### Tasks
- [x] Adjust admin view for courses to include course details.

</details>


#### 👉 USER STORY: As a **staff member**, I can **click on a course to see all registrations for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/33)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Completed in [Sprint 1](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] When clicking on a Course in the Django backend, staff users can see a list of all registrations for the course.

##### Tasks
- [x] Create CourseRegistration model
- [x] Create CourseSessions model
- [x] Register CourseRegistrations as a field of Courses in the admin view as an inline
- [x] Write tests for CourseRegistration and CourseSessions model

</details>


#### 👉 USER STORY: As a **staff member,* I can **download a CSV file containing all registrations for a course** so that **I can have a local copy of that information.** (https://github.com/nacht-falter/aikido-course-website-django/issues/39)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

Not completed (prioritized as Won't-Have)

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [ ] There is a download button in the admin view which allows staff users to download the registration data for a course as a csv file.

##### Tasks
- [ ] Create admin action which gets all registrations of a course and saves their data as a csv file

</details>


#### 👉 USER STORY: As a **staff member**, I can **click on a course to see all sessions associated with the course** (https://github.com/nacht-falter/aikido-course-website-django/issues/41)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] When clicking on a Course in the Django backend, staff users can see a list of all sessions for the course.

##### Tasks
- [x] Register CourseSessions as a field of Courses in the admin view as an inline

</details>


#### 👉 USER STORY: As a **staff member** I can **see the number of registrations for each course in the course list in the Django admin backend** so that **I can access that information without having to click on a course first.** (https://github.com/nacht-falter/aikido-course-website-django/issues/42)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 3](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] The number of registrations for each course are displayed in the course list in the Django admin view.

##### Tasks
- [x] Create method for getting registration count
- [x] Add method to courses_list display
- [x] Write tests for method

</details>


#### 👉 USER STORY: As a **staff member* I can **use a WYSIWIG editor in the Django backend** so that **I have more control over layout and styling.** (https://github.com/nacht-falter/aikido-course-website-django/issues/44)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

Completed in [Sprint 6](https://github.com/nacht-falter/aikido-course-website-django/milestone/23?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is a WYSIWIG editor installed that staff members can use for editing text fields.

##### Tasks
- [x] Install and setup summernote.
- [x] Adjust admin view to use summernote fields for text fields.

</details>


#### 👉 USER STORY: As a **staff member** I can **toggle a courses registration status from the course list in the Django amdin backend** without **having to click on the course first.** (https://github.com/nacht-falter/aikido-course-website-django/issues/47)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

Completed in [Sprint 4](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1) ✓

<details>

<summary>Show details</summary>

##### Acceptance Criteria
- [x] There is an action for toggling the registration status in the action dropdown list in the course view of the Django backend.

##### Tasks
- [x] Add action to CourseAdmin view which toggles the courses registration_status

</details>

<hr>

### EPIC: Content Management

#### 👉 USER STORY: As a **staff member**, I can **create new pages and edit existing pages** so that **I can add new content to the website**. (https://github.com/nacht-falter/aikido-course-website-django/issues/35)
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Content%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

Completed in [Sprint 6](https://github.com/nacht-falter/aikido-course-website-django/milestone/23?closed=1) ✓

<details>

<summary>Show details</summary>

### Acceptance Criteria
- [x] Staff members can add pages from the admin view
- [x] Staff members can define for pages
- [x] Published pages are displayed in the main navigation automatically
- [x] Staff members can use a WYSIWIG editor to edit the page contents

### Tasks
- [x] Create page model
- [x] Create category model
- [x] Register models to the admin site
- [x] Create views for page display
- [x] Update base.html template to include links to pages sorted by category in the navigation
- [x] Write tests for models and views

</details>

<hr>
