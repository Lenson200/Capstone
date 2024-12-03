# Learning Management System

# Project Capstone Overview
This application is designed to help manage and track employee training within an organization 
 The application allows users to :
   - `access training modules`
   - `track completed trainings`
   - `create profiles`
   - `adding and deleting training modules`
   - `adding completed trainings`
   - `search ability for any modules or employees`

## Distinctiveness and Complexity
This project stands out for its combination of user management, training module handling, and dynamic interactions, all designed to meet the needs of a real-world organization. The application is tailored for multiple user roles—each with specific access permissions—ranging from basic users to administrators and trainers.
What makes this project particularly distinctive is the integration of various dynamic elements using JavaScript to improve user experience . The design of the  incorporates a layout with a navigation bar that adjusts based on user roles, further enhancing the overall usability and accessibility of the platform.
the application emphasizes robust data handling and security, ensuring that users’ personal and training data is stored and managed securely.The combination of database models for user profiles, training modules, and completed trainings ensures that all relevant information is accessible in an organized manner.
Since we used Django framework there is an assuarance for scalability and flexibility for future updates.

## File Structure and Content
My Key files and contents overview are as follows:

 **Main Structure** 
  - `LearningManagementSystem`
  - `Training`  
  - `media`
  - `env`  
  - `manage.py`  
  - `db.sqlite3`
  - `README.md`


**Sub Structure**

  A.**Django app framework project start-up files**
- Folder (`LearningManagementSystem`) 
     - Files:
        - `__init__.py`
        - `__pycache__`
        - `asgi.py`
        - `settings.py`
        - `urls.py`
        - `wsgi.py`
            
B. **Training app files** 
   - `Training` Folder:
        - Files:{
            - `__init__.py`
            - `admin.py`
            - `context_processors.py`{a script that allows me to embed and pass anything in my templates.I added this script for me to easily pass employeeprofile details as a way to access them instead of relying on passing it on each view }
            - `migrations`
            - `urls.py`
            - `__pycache__`
            - `apps.py`
            - `forms.py`
            - `models.py`(Contains the models used to represent users, employee profiles, training modules, completed trainings, and required trainings. This file is crucial for the database schema of the application)
            - `tests.py`
            - `views.py`(Handles the routing and logic for the different pages in the application)
            }
        - Folders:
            - `templates`:
               - Files:{
                    - `Completed_training_details.html`(A page that displays in tabular form the list of completed training sessions and year of expiry)
                    - `categories.html`(A page that displays a list of module categories available in the application)
                    - `login.html`(This page renders a form when users want to login to the application)
                    - `staff_completed_trainings.html`(displays a list of all employees who have completed training sessions and their counts )
                    - `training_module_form.html`(displays a form to add a trainng module to the system)
                    - `Layout.html`( The base template, which includes the navigation bar and common layout and styles.I preffered this in order for me to keep consistency in the entire application)
                    - `category_detail.html`(shows the content of available categories in the category list page)
                    - `profile.html`(Displays the user's profile information inlcuding training completion count and read modules count . with an update button to update profile)
                    - `training_module_confirm_delete.html`(confirms deletion of a chosen module)
                    - `training_module_list.html`(displays a list of available  modules)
                    - `add_completed_training.html`(Page used by a trainer profile that renders a form to add completed training sessions for a particular employee )
                    - `index.html`(The homepage with a just a search bar to search  available training modules or other trainees)
                    - `register.html`(Page that renders a form for registration)
                    - `training_module_detail.html`(Shows the content of a training module that a user has clicked on)
                    - `update_trainings_required.html`(used by a trainer profile to update required trainings for staffs)
                    }
            - `static`:
                - `Training`:
                     - Files:{
                    - `modulehandling.js`(this is used to handle the dynamic element of a button that marks read and unread to a module and changes the button depending on the style)
                    - `search.js`(enables users to search the for modules and routes the request dynamically from the front end and delivers it to the backend for logic handling)
                    - `style.css`(styles the entire application including pages background of the body ,elements ,tags and much more including the image display)
                    - `update.js`(This is use to update the user when logged in successfully and also when user is updating profile)}
                - `images`:  
                    - `default_application_images.cs50duck`(a default image for when a user has no profile pic)


C.**Media** 
   - Folders:
     - `profile_pics`-> (images for profiles)
     - `uploads` (all documents for the project)

D.**env**
     - (Environment configuration files->Incase one is in a cloud ,remote or codespace my settings would remain the same as i would be in the same environment and still retain consistency across all environments) 

E.**-File: `manage.py`**

F.**- File: `db.sqlite3`**
E.**-File: `README.md`**

## How to Run the Application
To run The Learning Management system application locally, follow these steps:
- Ensure you have a code editor or IDE installed, such as Visual Studio Code (VSCode), PyCharm, or any other editor that supports Python and Django development.
-It's recommended to use a virtual environment to manage dependencies. If you don’t have one set up, create it by running the following commands(python -m venv venv){depends on which OS you are using the given commands are for windows}
-Activate the virtual environment(.\venv\Scripts\activate){depends on which OS you are using the given commands are for windows}
- Install dependancies(pip install -r requirements.txt)
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver(By default, the server will run at http://127.0.0.1:8000/)

## Aditional information such as packages needed
Most of the dependacies are in the requirement.txt and the .env.This application has the potential for significant growth and the addition of more advanced features .However for this project I’ve simplified the project using a limited set of features and resources, adhering to the constraints specified in the project requirements.

