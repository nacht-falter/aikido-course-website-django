# DANBW Aikido Course Website
## A course registration website built with Django
**Dynamic Aikido Nocquet BW** is an Aikido organization based in Baden-Württemberg, Germany. The organization offers Aikido courses several times a year. Members of the organization can sign up for those courses.

This website aims at offering an easy and straightforward way for DANBW members to sign up for courses and manage their course registrations and exams. Furthermore the website allows DANBW staff members to manage courses and course registrations as well as the website content.

![Aikido Course Website Mockups](media/screenshots/mockups.jpg)

## Table of contents

- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Design Process](#design-process)
  - [Strategy Plane](#strategy-plane)
  - [Scope Plane](#scope-plane)
  - [Structure Plane](#structure-plane)
  - [Skeleton Plane](#skeleton-plane)
  - [Surface Plane](#surface-plane)
- [Agile Methodology](#agile-methodology)
  - [GitHub Issues and Projects](#github-issues-and-projects-as-agile-tools)
  - [Sprint Planning](#sprint-planning)
  - [Progress Tracking](#progress-tracking)
- [Technologies Used](#technologies-used)
  - [Frameworks and Languages](#frameworks-and-languages)
  - [Additional Python Packages](#addditional-python-packages)
  - [Other Software](#other-software)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
  - [Code](#code)
  - [Images](#images)
  - [Text](#texts)
  - [Acknowledgements](#acknowledgements)

## Features

### Existing Features

#### User Accounts and Profiles
- Users can sign up to the website by providing an email address, a username, and a password.
- Users need to confirm their email address, before being able to log in to the website.
- After having confirmed their email address, users are asked to create a user profile with their full name and their current Aikido grade.
- Users can see their user profile on the **My Profile** page. From there, they can also update their information or delete their account, if they are regular users (Staff users cannot delete their accounts from the frontend, as a security measure).

![Screenshots Account](media/screenshots/screenshots_account.png)

#### Course Registration and Management
- Users can sign up for courses by choosing a course with open registration status from the **Courses** page and filling out the sign-up form. Users can decide if they want to participate in the whole course or select single sessions. The course fee will be calculated automatically, depending on the selection. Users can also apply for a grading exam. The exam grade will be stored with the registration according to the user's current grade.
- After signing up for a course, users can see their current registrations on the **My Registrations** page. They can update or cancel their registrations if they wish.

![Screenshots Course Registration](media/screenshots/screenshots_courseregistration.png)

- Upon logging in for the first time after a course with an exam application has passed, the user will be asked to confirm if they have passed their exam.

![Screenshots Course Registration](media/screenshots/screenshots_exam_passed.png)

#### Website UX
- The website has a responsive navigation menu accessible from all pages.
- The start page presents the user with an image slideshow and general information about the organization. Furthermore, the start page features a list of upcoming courses, so that users can immediately see, which courses are available to sign up for.
- There are several other pages available providing detailed information about Aikido, about the organization. Moreover, visitors, who are interested in learning Aikido, can get information on where to start.
- Finally, there is a contact page available from the websites' footer. Upon submitting the contact form, an email is sent to the organization with the user's message.

![Screenshots Course Registration](media/screenshots/screenshots_content.png)

#### Staff functions
##### Course and Registration Management
- Staff members can manage courses and course registrations from the Django admin site. They can create new courses, update existing courses, and see a list of registrations for each course.
- They can also update registrations, for example to update the payment status.
- There are actions available for duplicating courses (in order to minimize the effort for creating new courses, which are similar to existing courses) and for toggling a course's registration status.

![Screenshots Course Registration](media/screenshots/screenshots_admin_courses.png)

##### Content Management
- Staff users can also create new pages or edit existing pages to update the website's content.
- Pages are assigned a category and newly created pages will automatically appear in the main navigation in the appropriate menu item. The order in which pages and categories appear in the navigation can be controlled by assigning a menu position value.
- The page content can be edited with a WYSIWYG editor, which allows for styling and also image upload.

![Screenshots Course Registration](media/screenshots/screenshots_admin_pages.png)

### Future Features
- The following features have not been implemented in the current scope of the project, but could be worth considering for future iterations:
  - Add a breadcrumb navigation to the website to further improve user experience.
  - Update a course's registration status automatically based on a registration period. This would require some task scheduling solution on the server, like [Cron](https://wiki.ubuntuusers.de/Cron/).
  - Limit the final fee of a course registration so that the fee for multiple sessions never exceeds the fee for the entire course.
  - Add the option to upload a PDF file or an image as an attachment with a course.
  - Add a form for signing up for a membership with the organization.
  - Allow staff users to download course registration data as a CSV file.
- Furthermore, all [user stories, which were not part of the current scope of the project](#user-stories-not-included-in-current-scope), could be reevaluated and considered for future iterations. 

## Design Process

This project was designed with a user-centered approach, keeping the five planes of user experience in mind.

### Strategy Plane

The website's target audience are members of the Aikido organization DANBW. The aim is to provide an easy and intuitive way for members to sign up for courses and manage their course registrations. At the same time, the project wants to make managing courses and registrations as simple as possible for staff members.

The project aims to provide a central platform for DANBW members, which engages its users and offers a positive user experience. This should be part of a strong sense of community, which is an important aspect of DANBW.

### Scope Plane

#### User Stories Within Project Scope
ℹ️ The following user stories were included in the current scope of the project.

ℹ️ User stories marked with the https://github.com/nacht-falter/aikido-course-website-django/labels/MVP label make up the [Minimum Viable Product](https://en.wikipedia.org/wiki/Minimum_viable_product).

##### THEME: User Accounts and Profiles

###### EPIC: User Registration and Authentication

👉 USER STORY: As a **visitor**, I can **create a user account** so that I can **log in and store my information** (https://github.com/nacht-falter/aikido-course-website-django/issues/2)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria:

- There is a Sign Up button accessible from everywhere on the website
- Upon clicking on the Sign Up button a user registration form is displayed
- Upon successful registration a new user is created in the database.

###### Tasks:

- Install and setup Django-allauth
- Create UserProfile model with additional fields
- Add Sign Up button to base template and link to allauth registration form
- Create user profile view
- Create user profile template
- Create user profile form

<hr>

</details>

👉 USER STORY: As a **user**, I can **log in to my account** by **clicking on a login button from anywhere on the Website** (https://github.com/nacht-falter/aikido-course-website-django/issues/3)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- There is a login button, which is accessible from everywhere on the website.
- Upon clicking on the button the user is presented with a form for loggingn in with their user credentials.

###### Tasks
- Add login button to base template
- Create login form 

<hr>

</details>

👉 USER STORY: As a **user**, I can **log out from my account** by **clicking on a Logout button from anywhere on the website**. (https://github.com/nacht-falter/aikido-course-website-django/issues/4)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

###### Acceptance Criteria
https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

- There is a logout button accessible from anywhere on the website
- Upon clicking on the logout button the user is logged out from the system.

###### Tasks
- Add logout button to base template
- Show logout button only for authenticated users

<hr>

</details>

👉 USER STORY: As a **user**, I can **receive an email** as **confirmation when I create a user account**. (https://github.com/nacht-falter/aikido-course-website-django/issues/5)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Registration%20and%20Authentication
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- After creating an account the user will receive an e-mail as confirmation.
- The email contains relevant details about the account and a confirmation message.

###### Tasks
- Set up email functionality in Django
- Send confirmation e-mail after account creation
- Create sendmail function in view to send the confirmation email upon successful account creation

<hr>

</details>

<hr>

###### EPIC: User Account Management

👉 USER STORY: As a **logged-in user**, I can **view my user profile** (https://github.com/nacht-falter/aikido-course-website-django/issues/6)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a link in the navigation for logged in user which brings them to their user profile.
- The user profile displays user data and includes a link to the user's course registration list. 

###### Tasks
- Create UserProfile model to extend User model
- Create view for user profiles
- Update template for user profile
- Update base template
- Test model and view

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **update my user profile** (https://github.com/nacht-falter/aikido-course-website-django/issues/7)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- A user can click on a link to edit the user's profile on the profile page.
- Upon clicking that link, a form for editing the user's data will appear.
- After submitting the form the updated data is stored in the database.

###### Tasks
- Create form for editing user profile with the following fields: first name, last name, username, email, grade
- Create view for editing the profile
- Register urls
- Write tests

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **reset my password** (https://github.com/nacht-falter/aikido-course-website-django/issues/8)
 
https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- Users can reset their password by clicking on a link on their profile page

###### Tasks
- Include link to account_change_password url from allauth in user profile template
- Adjust allauth change password template

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **delete my account** (https://github.com/nacht-falter/aikido-course-website-django/issues/9)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- Users can delete or deactivate their account by clicking on a link
- After the user confirms they want to delete/deactivate the account, the user will be removed from the system

###### Tasks
- Create deactivate user view
- Create deactivate user template
- Write tests for view

<hr>

</details>

<hr>

###### EPIC: Course Registration

👉 USER STORY: As a **visitor**, I can **click on a link in the navigation menu** to **see a list of available courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/11)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a list of all courses available at a URL.
- Theres is a navigation menu containing a link to the URL to the course list.

###### Tasks
- Create course list view
- Create base template with navigation menu containing a link to the course list page
- Create course list template
- Register URL
- Test view

<hr>

</details>

👉 USER STORY: As a **visitor** or a **logged-in user**, I can **see the fees for the course, depending on how many sessions I have selected** (https://github.com/nacht-falter/aikido-course-website-django/issues/13)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

###### Acceptance Criteria
- Upon filling out a course registration form the user can see, what the course fees will be.
- The course fees change, depending on if the user selects single sessions or the entire course.
- The course fee will be stored with the registration upon submitting the form.

###### Tasks
- Add course sessions to course registration form
- Create logic for calculating the course fees to the post method of the course registration view.
- Add javascript to the template in order to display the fees dynamically.
- Write tests for view

<hr>

</details>

👉 USER STORY: As a **visitor** or a **logged-in user**, I can **receive an email as confirmation**, **after signing up for a course, containing course and payment details so that I have a backup of all relevant details** (https://github.com/nacht-falter/aikido-course-website-django/issues/14)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- After signing up for a course users will receive an email confirming the successful registration.
- The email contains details about the course and the registration.

###### Tasks
- Update RegisterCourse view to send email upon successful registration
- Include course and registration details in email

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **fill out a sign-up form** to **sign up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/43)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- A logged-in user can click on a link in the course with open registration status and will be directed to to a registration form.
- The registration-form provides fields for all necessary details.
- Upon filling out the form, a new registration will be stored in the database.

###### Tasks
- Create course registration form
- Create registration form template
- Create view
- Register url
- Write tests for form and view

<hr>

</details>

<hr>

###### EPIC: Course Registration Management

👉 USER STORY: As a **logged-in user**, I can **see a list of my current and past registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/15)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- The user can see a list of their current and past registrations in separete sections of the registrations list.

###### Tasks
- Update registration list template to separate between current and past registrations

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **edit my current registrations** so that **I can update information** (https://github.com/nacht-falter/aikido-course-website-django/issues/16)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L


###### Acceptance Criteria
- Users can see a list of their current registrations.
- Users can click on a current registration and be redirected to a form for editing their registration.
- After submitting the form the updated data will be stored in the database.

###### Tasks
- Create view to list registrations.
- Create template for registration list with edit registration button.
- Create view for editing registration
- Test views

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **cancel a course registration** (https://github.com/nacht-falter/aikido-course-website-django/issues/17)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- Users can see a list of their current registrations.
- Users can cancel registrations by clicking on a cancel registration button.
- Users will be asked for confirmation before the registration is cancelled.

###### Tasks
- Create view to list registrations
- Create view to delete registration
- Create templates for registration list with cancel button and confirmation
- Create navigation link to users registrations page
- Register urls
- Write tests for views

<hr>

</details>

👉 USER STORY: As a **visitor** or a **logged-in user**, I can **see if I applied for an exam after I signed up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/20)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- In the list of the users current registrations there is a message indicating if the user has applied for an exam.

###### Tasks
- Add exam field to registration list template

<hr>

</details>

<hr>

###### EPIC: Exams

👉 USER STORY: As a **logged-in user**, I can **receive a notification after logging in if I have previously applied for an exam** so that **I can update my user profile accordingly** (https://github.com/nacht-falter/aikido-course-website-django/issues/22)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

###### Acceptance Criteria
- After applying for an exam and after the course has passed, the user will be presented with a dialogue asking if they want to update their grade.
- If the user confirms that they passed their exam the registration will be updated to include the information in the exam_passed field.

###### Tasks
- Add logic for checking if the user has applied for an exam and if the course has passed to user profile view
- Create view for displaying the notification.
- Add exam_passed field to CourseRegistration model
- Display if exam has been passed in  the course registration view
- Write tests for views

<hr>

</details>

👉 USER STORY: As a **logged-in user** I can **see what exam I applied for in the list of my past and current registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/45)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- If the user applied for an exam with a course registration, the grade they applied for is displayed with the registration in the course registration list.

###### Tasks
- Display exam grade in course registration list template

<hr>

</details>

<hr>

##### THEME: Website UX

###### EPIC: UI Design

👉 USER STORY: As a **visitor** or a **logged-in user**, I want **the website to have a responsive, consistent and visually appealing UI design** in order to **elicit a positive response during my visit** (https://github.com/nacht-falter/aikido-course-website-django/issues/36)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

###### Acceptance Criteria
- The website has a consistent layout and styling over all pages.
- The website is responsive for different screen sizes.
-  The website uses colors and images which represent the organization.

###### Tasks
- Add bootstrap to base template
- Create basic bootstrap layout and styling
- Include images on the home page

<hr>

</details>

👉 USER STORY: As a **user**, I want **the website to comply with accessibility guidelines** so that **I can access it with screen readers or other assistive technologies** (https://github.com/nacht-falter/aikido-course-website-django/issues/55)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- The templates use accessibility labels and elements where appropriate.

###### Tasks
- Use aria-labels where necessary
- Fix suggestions from 
- User semantic html elements in base template

<hr>

</details>

👉 USER STORY: As a **visitor or logged-in user** I can **see messages with different colors** so that **I can get feedback for my actions.** (https://github.com/nacht-falter/aikido-course-website-django/issues/56)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- There are messages displayed, when the user submits forms.
- The messages have different colors depending on their type. 

###### Tasks
- Add bootstrap alert class to messages
- Set up messages typse in settings.py
- Add styling to alerts types

<hr>

</details>

👉 USER STORY: As a **logged-in user**  I can **see if I am logged in or not** (https://github.com/nacht-falter/aikido-course-website-django/issues/66)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- There is an indicator on the website showing logged-in users, that they are logged in.

###### Tasks
- Include indicator for authentication status in base.html template

<hr>

</details>

<hr>

###### EPIC: Navigation

👉 USER STORY: As a **visitor** or **logged-in user**, I can **easily navigate through different sections of the website using a clear and intuitive navigation menu displayed on all pages** (https://github.com/nacht-falter/aikido-course-website-django/issues/23)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a navigation menu displayed on all pages.
- The navigation menu is responsive so that it is easily accessible on all devices

###### Tasks
- Add bootstrap classes and js to navigation in order to style it and make it responsive

<hr>

</details>

👉 USER STORY: As a **Visitor or logged-in user** I can **see a custom error page with a link to the homepage**, when I try to access a URL that doesn't exist (https://github.com/nacht-falter/aikido-course-website-django/issues/50)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- There is a custom error page with a link to the homepage.
- The page is displayed when a 404 error comes up instead of the default 404 error page.

###### Tasks
- Create a custom 404 error template

<hr>

</details>

<hr>

###### EPIC: Website Content

👉 USER STORY: As a **user**, I want **the start page to display information about the website's purpose** (https://github.com/nacht-falter/aikido-course-website-django/issues/25)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- The homepage includes information about the website's purpose and a short description.

###### Tasks
- Add description of the organization and the purpose of the website to the home page template

<hr>

</details>

👉 USER STORY: As a **user**, I want **the start page to display the latest courses and currently open course registrations** so that **I can quickly access them** (https://github.com/nacht-falter/aikido-course-website-django/issues/26)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a list of upcoming courses on the home page.
- Users can see which courses are open for registration.

###### Tasks
- Add list of upcoming courses to index.html
- Mark courses with open registrations with a badge

<hr>

</details>

👉 USER STORY: As a **user**, I want **the start page to display the latest courses and currently open course registrations** so that **I can quickly access them** (https://github.com/nacht-falter/aikido-course-website-django/issues/27)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- There are pages for accessing information about the organization accessible from the navigation menu.
- There is a page with links to the websites of all Aikido Dojos which are part of the organization.
- There is information available for beginners so that they can find out where they can start learning Aikido.

###### Tasks
- Create pages for information about Aikido, about Danbw, about the Dojos, and for beginners
- Include pages in navigation menu

<hr>

</details>

👉 USER STORY: As a **visitor or logged-in user**, I can **fill out a contact form** so that **I can get in touch with the team** (https://github.com/nacht-falter/aikido-course-website-django/issues/27)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- There is a contact page, which is accessible from the footer.
- There is a contact form on the contact page, which allows users to contact the organization.

###### Tasks
- Set up email backend
- Create contact view
- Create contact form
- Create template

<hr>

</details>

<hr>

###### EPIC: Course Management

👉 USER STORY: As a **staff member**, I can **create new courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/30)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- A staff member can login to the Django backend and create new course items by clicking on 'Add Course' and fill out the course details
- All form fields are validated according to their field type.
- Slug field is auto completed

###### Tasks
- Create Course model according to ERD (MVP version)
- Register Course model in admin view
- Add custom validation to date fields
- Add auto fill method for slug field
- Write tests for the model

<hr>

</details>

👉 USER STORY: As a **staff member**, I can **duplicate existing courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/31)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- Staff members can see existing courses in the Django backend and duplicate a course by clicking on a course in the list and select a duplicate course method.

###### Tasks
- Create method for course duplication and register it in the admin view
- Write tests for duplication method

<hr>

</details>

👉 USER STORY: As a **staff member**, I can **update or delete existing courses** (https://github.com/nacht-falter/aikido-course-website-django/issues/32)

https://github.com/nacht-falter/aikido-course-website-django/labels/MVP

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- Staff members can update courses from the Django admin backend
- Staff members can delete courses from the Django admin backend
- Staff members can see the properties of existing courses in the django admin backend course list.

###### Tasks
- Adjust admin view for courses to include course details.

<hr>

</details>

👉 USER STORY: As a **staff member**, I can **click on a course to see all registrations for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/33)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- When clicking on a Course in the Django backend, staff users can see a list of all registrations for the course.

###### Tasks
- Create CourseRegistration model
- Create CourseSessions model
- Register CourseRegistrations as a field of Courses in the admin view as an inline
- Write tests for CourseRegistration and CourseSessions model

<hr>

</details>

👉 USER STORY: As a **staff member**, I can **click on a course to see all sessions associated with the course** (https://github.com/nacht-falter/aikido-course-website-django/issues/41)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- When clicking on a Course in the Django backend, staff users can see a list of all sessions for the course.

###### Tasks
- Register CourseSessions as a field of Courses in the admin view as an inline

<hr>

</details>

👉 USER STORY: As a **staff member** I can **see the number of registrations for each course in the course list in the Django admin backend** so that **I can access that information without having to click on a course first.** (https://github.com/nacht-falter/aikido-course-website-django/issues/42)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- The number of registrations for each course are displayed in the course list in the Django admin view.

###### Tasks
- Create method for getting registration count
- Add method to courses_list display
- Write tests for method

<hr>

</details>

👉 USER STORY: As a **staff member** I can **use a WYSIWYG editor in the Django backend** so that **I have more control over layout and styling.** (https://github.com/nacht-falter/aikido-course-website-django/issues/44)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- There is a WYSIWYG editor installed that staff members can use for editing text fields.

###### Tasks
- Install and setup summernote.
- Adjust admin view to use summernote fields for text fields.

<hr>

</details>

👉 USER STORY: As a **staff member** I can **toggle a courses registration status from the course list in the Django amdin backend** without **having to click on the course first.** (https://github.com/nacht-falter/aikido-course-website-django/issues/47)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS

###### Acceptance Criteria
- There is an action for toggling the registration status in the action dropdown list in the course view of the Django backend.

###### Tasks
- Add action to CourseAdmin view which toggles the courses registration_status

<hr>

</details>

<hr>

###### EPIC: Content Management

👉 USER STORY: As a **staff member**, I can **create new pages and edit existing pages** so that **I can add new content to the website**. (https://github.com/nacht-falter/aikido-course-website-django/issues/35)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Content%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

###### Acceptance Criteria
- Staff members can add pages from the admin view
- Staff members can define for pages
- Published pages are displayed in the main navigation automatically
- Staff members can use a WYSIWYG editor to edit the page contents

###### Tasks
- Create page model
- Create category model
- Register models to the admin site
- Create views for page display
- Update base.html template to include links to pages sorted by category in the navigation
- Write tests for models and views

<hr>

</details>

<hr>


#### User Stories Not Included in Current Scope
ℹ️ The following user stories were not included in the current scope of the project.

👉 USER STORY: As a **logged-in user**, I can receive an email as confirmation when I delete my account (https://github.com/nacht-falter/aikido-course-website-django/issues/10)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20User%20Accounts%20and%20Profiles
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20User%20Account%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- Users receive an email as confirmation, when they have deactivated their account.

###### Tasks
- Add sendemail function to DeactivateAccount view

<hr>

</details>

👉 USER STORY: As a **visitor**, I can **fill out a registration form** to **sign up for a course** (https://github.com/nacht-falter/aikido-course-website-django/issues/12)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L


###### Acceptance Criteria
- A visitor can sign up for courses without having to create a user account.
- The registration will be saved in the database upon submitting a registration form.

###### Tasks
- Create model for visitor registrations
- Create registration form and view
- Add template

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **receive an email as confirmation when I updated a registration** (https://github.com/nacht-falter/aikido-course-website-django/issues/18)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
- After updating a course registration the user wil receive an email with the updated information.

###### Tasks
- Add sendemail function to update course registration view

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **receive an email as confirmation when I canceled a registration.** (https://github.com/nacht-falter/aikido-course-website-django/issues/19)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Registration%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S

###### Acceptance Criteria
-  After cancelling a course registration a user receives an email as confirmation.

###### Tasks
- Add sendemail function to cancel registration view

<hr>

</details>

👉 USER STORY: As a **logged-in user**, I can **cancel exam applications for current registrations** (https://github.com/nacht-falter/aikido-course-website-django/issues/21)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Course%20Registration%20and%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Exams
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- In the users registrations list, there is a button for cancelling an exam application.
- Upon clicking the button, the user is asked to confirm the cancellation.
- After confirming the registration is updated with the new setting.

###### Tasks
- Update course registration template to display a button for cancelling an exam application
- Create confirmation template
- Create view
- Write tests for view

<hr>

</details>

👉 USER STORY: As a **visitor** or **logged-in user** I want **to be able to see a list of pages with thumbnail images to visit** in the sidebar on the home page (https://github.com/nacht-falter/aikido-course-website-django/issues/65)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20UI%20Design
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a list of available pages on the home page for quick access.
- Pages include thumbnail images.

###### Tasks
- Update index.html template to include list of pages.
- Display pages with thumbnail (featured image)

<hr>

</details>

👉 USER STORY: As a **user**, I can **see a breadcrumb navigation on all pages** so that **I can see my current position on the website and easily navigate back to previous pages** (https://github.com/nacht-falter/aikido-course-website-django/issues/24)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Navigation
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- The user can see where they are on the website from a breadcrumb navigation, which is visible on all pages.

###### Tasks
- Add a navigation to base.html with a link to the current page, as well as links to parent pages such as categories and a link to the start page

<hr>

</details>

👉 USER STORY: As a **visitor** or a **logged-in user,** I can **see a photo gallery with photos from past courses** so that **I can get some impressions of the courses.** (https://github.com/nacht-falter/aikido-course-website-django/issues/40)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

###### Acceptance Criteria
- There is a photo gallery of past courses available on the website.
- Users and visitors can look at photos from different courses.

###### Tasks
- Create a Picture model with a foreign key to courses
- Create a view and a template for displaying pictures filtered by course as a picture gallery

<hr>

</details>

👉 USER STORY: As a **visitor** or **logged-in user**, I want **to be able to see a list of pages with thumbnail images to visit** in the sidebar on the home page (https://github.com/nacht-falter/aikido-course-website-django/issues/65)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Website%20UX
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Website%20Content
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M

###### Acceptance Criteria
- There is a list of available pages on the home page for quick access.
- Pages include thumbnail images.

###### Tasks
- Update index.html template to include list of pages.
- Display pages with thumbnail (featured image)

<hr>

</details>

👉 USER STORY: As a **staff member,** I can **download a CSV file containing all registrations for a course** so that **I can have a local copy of that information.** (https://github.com/nacht-falter/aikido-course-website-django/issues/39)

<details>

<summary>Show details</summary>

https://github.com/nacht-falter/aikido-course-website-django/labels/THEME%3A%20Staff%20functions
https://github.com/nacht-falter/aikido-course-website-django/labels/EPIC%3A%20Course%20Management
https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have
https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L

###### Acceptance Criteria
- There is a download button in the admin view which allows staff users to download the registration data for a course as a csv file.

###### Tasks
- Create admin action which gets all registrations of a course and saves their data as a csv file

<hr>

</details>

<hr>

### Structure Plane

The project is built around two main models: Courses and Users. What the website is supposed to do, essentially, is to connect those to models. The connection between the two models is provided by the Course Registrations model as an intermediary model.

The relationships between the models used in the project are represented in the following entity relationship diagrams:

Database schema for the minimum viable product:

![ERD for MVP](media/erd/erd_mvp.png)

Database schema for the final version in the current scope:

![ERD for MVP](media/erd/erd_final.png)

### Skeleton Plane

The overall layout of the website stays close to the [existing website](https://www.danbw.de) to make the transition from the old to the new version as user-friendly as possible.

The website consists of three main sections: A header with the logo, the main title, and the navigation menu, a main section for the content, and a footer.

The website is designed to be responsive for all screen sizes.

The wireframes for the project can be found here:

[Wireframes Mobile](media/wireframes/wireframes-mobile.png)

[Wireframes Desktop](media/wireframes/wireframes-desktop.png)

### Surface Plane

Similar to the general layout, the goal of the visual design of the website was to stay close to the design of the original website, while updating and modernizing design elements where appropriate.

#### Colors

The project adopts the color scheme of the original website, which is part of the corporate design of the organization.

The color scheme consists of two main colors and one tertiary color:

<!-- Display colors in markdown: https://stackoverflow.com/a/41247934 -->
![#1e3c95](https://placehold.co/100x100/1e3c95/1e3c95.png) Primary color: #1e3c95

![#b5172c](https://placehold.co/100x100/b5172c/b5172c.png)  Secondary color: #b5172c

![#f1f1f1](https://placehold.co/100x100/f1f1f1/f1f1f1.png) Tertiary color: #f1f1f1

#### Fonts

The font for the website, [Source Sans 3](https://fonts.google.com/specimen/Source+Sans+3), is the same as the one used on the existing website in order to provide visual coherence.

#### Logo

The organization's logo has been slightly updated for this project to make it fit better with the more modern look of the website:

![DANBW Logo](static/images/danbw-logo.png)

## Agile Methodology

### GitHub Issues and Projects as Agile Tools

[GitHub Issues](https://docs.github.com/en/issues) and [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) were used as tools for Agile methodology.

- I used [Issues](https://github.com/nacht-falter/aikido-course-website-django/issues) for user stories and for bugs.

- Issue tasks were used to define acceptance criteria and tasks for each user story.

- I assigned labels to user stories to categorize them into [Themes](https://github.com/nacht-falter/aikido-course-website-django/labels?q=THEME) and [Epics](https://github.com/nacht-falter/aikido-course-website-django/labels?q=EPIC)

- Furthermore, all user stories were prioritized using the MoSCoW prioritization technique with the following project-wide priorities:

  https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Must-Have https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Should-Have https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Could-Have https://github.com/nacht-falter/aikido-course-website-django/labels/PRIORITY%3A%20Won%27t-Have

- All user stories were assigned a SIZE label, categorizing them into five different sizes:

  https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XS https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20S https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20M https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20L https://github.com/nacht-falter/aikido-course-website-django/labels/SIZE%3A%20XL

  The Fibonacci series was used to assign story points to these sizes: XS = 1 story point, S = 2 story points, M = 3 story points, L = 5 story points, XL = 8 story points.

- I used Milestones for the [Product Backlog](https://github.com/nacht-falter/aikido-course-website-django/milestone/1) and for adding user stories to [Sprints](https://github.com/nacht-falter/aikido-course-website-django/milestones?state=closed).

- [Projects](https://github.com/nacht-falter/aikido-course-website-django/projects?query=is%3Aclosed) were used for tracking tasks within each iteration.

- [Project workflows](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically) were used to automatically add user stories in a sprint to the Todo column of the corresponding  project board.

- Finally, I created a [custom priority field](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields) to further prioritize items within a project on a sprint level.

### Sprint Planning

I planned the project with timeboxed sprints of three days each. I assigned user stories to each sprint, while prioritizing MVP user stories, but making sure that the amount of user stories with a Must-Have priority never exceeded 60% in each sprint. The situation was reevaluated after each sprint.

#### Sprint 1 (3.7.-5.7.2023)

<details>

<summary>Show sprint details</summary>

- Initial Setup and Deployment
- Create models for MVP
- Setup Admin view for course management
- Create course list view

All items completed on 5.7.2023

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/2?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/5)

</details>

<hr>

#### Sprint 2 (6.7-8.7.2023)

<details>

<summary>Show sprint details</summary>

- Create forms for course registration for logged-in users (*C*RUD)
- Create a list view to display a user's current and past registrations (C*R*UD)
- Add options for updating and cancelling registrations (CR*UD*)

All items completed on 7.7.2023

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/19?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/6)

</details>

<hr>

#### Sprint 3 (10.7.-12.7.2023)

<details>

<summary>Show sprint details</summary>

- User account registration
- Login/Logout
- Deactivate account
- User profile
- Refine admin view
- Bugfixes

All items completed on 11.7.2023

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/20?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/8)

</details>

<hr>

#### Sprint 4 (13.7.-15.7.2023)

<details>

<summary>Show sprint details</summary>

- Course fee calculation
- Update grade after exam
- Password reset
- Admin site actions

Finished on 15.7.2023, one unfinished item moved back to product backlog

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/21?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/9)

</details>

<hr>

#### Sprint 5 (18.7.-20.7.2023)

<details>

<summary>Show sprint details</summary>

- Startpage content
- Implement Django messages
- Main navigation
- Basic styling for user interface
- Bugfixes

Finished on 20.7.2023, two unfinished items moved back to product backlog

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/22?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/10)

</details>

<hr>

#### Sprint 6 (21.7.-25.7.2023)

<details>

<summary>Show sprint details</summary>

- Pages and Categories
- Accessibility
- WYSIWYG editor
- Bugfixes

Finished on 25.7.2023, two unfinished items moved back to product backlog

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/23?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/12)

</details>

<hr>

#### Sprint 7 (26.7.-28.7.2023)

<details>

<summary>Show sprint details</summary>

- Contact Form
- Custom error pages
- Bugfixes

Completed on 28.7.2023

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/24?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/13)

</details>

<hr>

#### Sprint 8 (31.7.-2.8.2023)

<details>

<summary>Show sprint details</summary>

- Page content
- Confirmation emails 
- Login status indicator
- Bugfixes

Finished on on 2.8.2023, one unfinished item moved back to the product backlog

[Sprint Details](https://github.com/nacht-falter/aikido-course-website-django/milestone/25?closed=1)

[Sprint Project Board](https://github.com/users/nacht-falter/projects/14)

</details>

<hr>

#### Sprint 9 (3.8.-5.8.2023)

<details>

<summary>Show sprint details</summary>

- Testing
- Bugfixes

Completed on 5.8.2023

</details>

<hr>

#### Sprint 10 (7.8-9.8.2023)

<details>

<summary>Show sprint details</summary>

- Documentation
- Implement test user feedback
- Bugfixes

Completed on 9.8.2023

</details>

<hr>

### Progress Tracking

The progress of the project was tracked with a burndown chart ([Burndown Chart Template](https://www.smartsheet.com/content/burndown-chart-templates)), by calculating the total amount of story points from the user stories. The ideal velocity was calculated by dividing the total number of story points with the number of sprints. The progress was tracked after each sprint:

![Burndown Chart](media/agile/burndown_chart.png)

## Technologies Used

### Frameworks and Languages

- The website has been built with [Django](https://www.djangoproject.com/), a Python web framework.
- HTML, CSS, and JavaScript have been used for implementing the website's front end.
- [Bootstrap](https://getbootstrap.com/) was used for the visual design and the layout for the front end.

### Addditional Python Packages

- [gunicorn](https://pypi.org/project/gunicorn/): WSGI server used for deployment 
- [psycopg2](https://pypi.org/project/psycopg2/): PostgreSQL database integration
- [dj-database-url](https://pypi.org/project/dj-database-url/): Django database management 
- [cloudinary](https://pypi.org/project/cloudinary/): Cloudinary integration
- [dj3-cloudinary-storage](https://pypi.org/project/dj3-cloudinary-storage/): Using Cloudinary as Django file storage
- [django-allauth](https://pypi.org/project/django-allauth/): Advanced authentication and user management for Django 
- [django-summernote](https://pypi.org/project/django-summernote/): WYSIWYG editor for text fields
- [django-crispy-forms](https://pypi.org/project/django-crispy-forms/): Provides styling for Django forms 
- [crispy-bootstrap5](https://pypi.org/project/crispy-bootstrap5/): Bootstrap5 package for crispy forms 
- [coverage](https://pypi.org/project/coverage/): Analyzing test coverage

### Other Software

- [GitHub](https://github.com/) is used to store all project files in the [repository](https://github.com/nacht-falter/aikido-course-website)
- [GitHub Issues](https://docs.github.com/en/issues) have been used for Agile methodology by assigning user stories to issues and using labels to organize user stories.
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) have been used for Agile sprint planning and task tracking.
  [The project boards for all sprints can be found here](https://github.com/nacht-falter/aikido-course-website-django/projects?query=is%3Aclosed).
- [Git](https://git-scm.com/) was used for version control by committing changes to Git and pushing them to GitHub from the command line.
- [Heroku](https://heroku.com/) is used to deploy the website. The deployed version is available at: 
- [ElephantSQL](https://www.elephantsql.com/) is used for the project's PostgreSQL database.
- [Cloudinary](https://cloudinary.com/) is used to store media files.
- [Balsamiq](https://balsamiq.com/) was used to create the [wireframes](#skeleton-plane) during the design process.
- [Lucidchart](https://www.lucidchart.com/) was used to create the [entity relationship diagrams (ERD)](#structure-plane) used for modeling the project database.
- [Font Awesome](https://fontawesome.com/) was used to add icons for aesthetic and UX purposes. The necessary files have been included in the static/fontawesome folder to avoid loading them from an external resource on each page load.
- [Google Fonts](https://fonts.google.com/) was used to import the font 'Source Sans 3'. The [font files](https://fonts.google.com/specimen/Source+Sans+3) have been included in the assets/fonts folder, to ensure that they don't have to be loaded from an external resource.
- [LightHouse](https://developer.chrome.com/docs/lighthouse/) has been used to assess the website's performance.
- [WAVE](https://wave.webaim.org/) has been used to further evaluate the website's accessibility.
- [Neovim](https://neovim.io/) was used for writing code.
- [Pixelmator Pro](https://www.pixelmator.com/pro/) was used to resize and edit images and to create the [mockup image](#danbw-aikido-course-website) at the top of this README

## Testing

[Testing documentation can be found here](TESTING.md)

## Deployment

In order to deploy the project follow the [instructions in the official Django Docs](https://docs.djangoproject.com/en/5.1/howto/deployment/).

## Credits

The following resources were used for the project:

### Code
I made extensive use of the Django documentation available at: https://docs.djangoproject.com/en/stable/. I won't list all the used pages here, but the use of the Django docs is extensively documented in comments in the code.

The initial setup and the basic structure of the project followed the instructions from the Code Institute Django Blog walkthrough project.

All other used sources are listed here (all code from these sources has been thoroughly reviewed, understood and adapted to the specific circumstances of this project):
- Customize property name: https://stackoverflow.com/a/64352815
- Add inlines to UserAdmin model: https://stackoverflow.com/a/35573797
- Add summernote field to inline model: https://github.com/summernote/django-summernote/issues/14
- Instructions for importing signals: https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
- Context processor for passing categories to templates: https://stackoverflow.com/a/34903331
- Pass course instance to form: https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c)
- Add new fields to form: https://stackoverflow.com/a/58944671
- Create slug from another field: https://stackoverflow.com/a/837835
- Adjust the plural of a model: https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-model-in-django-admin/
- Assign increasing integer values to a list of variables: https://stackoverflow.com/a/64485228
- Using django signals: https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
- Testing Django admin instructions from: https://www.argpar.se/posts/programming/testing-django-admin
- Test validation error: https://stackoverflow.com/questions/73188838/django-testcase-check-validationerror-with-assertraises-in-is-throwing-validatio
- Test messages: https://stackoverflow.com/a/46865530
- Test Redirect: https://stackoverflow.com/a/49353888
- Test bad header: https://stackoverflow.com/a/27268861
- Override default allauth password redirect url: https://stackoverflow.com/a/56599071
- Contact form: https://learndjango.com/tutorials/django-email-contact-form-tutorial
- Get Course id from url: https://stackoverflow.com/a/1036564
- Receiving data from the template with JavaScript: Instructions from: https://adamj.eu/tech/2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
- Get data to dynamically set active nav-link: https://stackoverflow.com/a/55151707
- Instructions for safely passing data to JavaScript: https://adamj.eu/tech/2022/10/06/how-to-safely-pass-data-to-javascript-in-a-django-template/
- Mocking timers with Jest: https://jestjs.io/docs/timer-mocks

### Images

All images used on the website were images used on the original website (https://www.danbw.de). I would like to thank DANBW for letting me use these images.

### Texts

The texts used for the project were taken from the original website, updated and translated to English.

### Acknowledgements

- I would like to thank my Code Institute mentor Can for his continued support and constructive advice.
- I would like to thank the Code Institute tutors for their support.
- I would like to thank all friends and family members who have tested the website for their helpful feedback and suggestions.
