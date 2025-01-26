# Task Manager
    #### Video Demo:  <https://youtu.be/whjKKie2GSI>
    #### Description: My CS50 Computer Science project is little game of flashcard, with learning twist, which helps people who learn Georgian language learn and revise words they have learnt or are learning.

    #### The users have 4 option to choose from and only one is correct answer. The sequence of the option words are always random, so that correct answer will be in the different positions every time.

    #### If the users want to check what the word is, they can click on the flashcard and it will flip, revealing meaning of the word in the English.

    #### The Georgian words are written in Georgian and IPA format too.

    #### The program let's users to continue from where they stopped and not from the beginning.

    #### There is also points and levels, each word is each level and points are added as users choose correct words for each flashcard, however, points are also subtracted from total amount of point for each mistake one point, so users may be on a higher level, but have 1 or 2 points only because of the mistakes they have done before.

    #### The users can also Reset progress and start from the zero with zero points, as well as, they can finish every word and start from the beginning, in this case points are saved, but level will start counting from the 1.

    #### There is also page dedicated to the Georgian recipes, where users can see Georgian cuisine recipes and isntructions how to make it.

    #### The inspiration came from my love for languages and of my own culture. I was also thinking about the gamification of it and how to make it fun for the users as well as how come up with something I would enjoy and be able to do. In the end, it was really fun to make this project, it made me work on something that I like as well as made me practice a lot of different parts of programing, a lot of Python, Flask, sqlite3, HTML and CSS, and just a pinch of the Javascript. Obviously, it was easier done with bootstrap too.

## Main
    #### Pages of the website and their functions explained:
    #### 1. Home page
    #### 2. Flashcards
    #### 3. Recipes
    #### 4. Profile
    #### 5. Registration/Log in/Log out

    #### Separate functions and files:
    #### 6. __init.py__
    #### 7. config.py
    #### 8. models.py
    #### 9. routes.py
    #### 10. run.py
    #### 11. utils.py
    #### 12. Database.db
    #### 13. words.csv and recipes.csv
    #### 14. styles.css

## Home page
    #### This page consists least of the functions.

    #### Every user can enter this page and it shows history and information about Georgia. There are images of Georgia as a slide show.

## Flashcards
    #### To access Flashcards page user should be logged in as it counts levels and points of the user, otherwise user will be redirected to log in page.

    #### After accessing the flashcard page user sees card with a Georgian word, 4 options, where one is correct answer and 3 wrong. the user should answer correctly to move on to the next level. the user also can click on the card to flip it and see the correct answer and give the answer after that, to give answer user should click on the submit button.

    #### When user picks the word and clicks on the submit button, the answer is send to routes.py where it is compared to the correct word, which is extracted from the sqlite3 with ID of the word. If the answer is correct point and level is updated and same if the answer was incorrect. In case that total point of the user is 0, then it can't be subtracted in case of wrong answer and stays zero.

    #### There is also Reset button, clicking on the zero button it updates Level and points of the user, so that they can start with 0 points and from first level.

    #### The words come from words.csv file which is in main directory and is extracted into database.db every time flashcards page is loaded.
    #### With words.csv file it is possible to update words and add or remove words from the lists easily.

## Recipes

    #### When user is on the recipes page, they see recipe, with ingredients, instructions and time for preparation and cooking.

    #### If user wants to move to the next recipe they can click on the next button, but only if it is available and if there is next recipe, in case there is no more recipes button is inactive, which is true for previous button as well and is controlled from routes.py page and in HTML with help of Jinja.

    #### The recipes logic is mostly dependant on the ID of the recipe, which determines amount of recipes, their sequence and how the buttons work.

    #### The recipes are exported from recipes.csv file with load of the recipes page. CSV file help us to easily add or remove recipes fro the webpage, with jsut edit of the CSV file.

## profile

    #### The users can access the profile page only when they are logged in.

    #### With help of the python and sqlite3 there is information such as users username, mail, levels and points.

    #### The users can update their username, mail and password. In case of chaging of the password function checks old password and matches it to the actual password at the moment. Also, it compares new passwords which are typed twice separately.

## Registration/Log in/Log out

    #### Registration just creates new data in database.db after user will input personal input into the fields, like username, mail and password.
    #### In the database.db, other information is included automatically, or just left empty.

    #### When user want to Log in, they just input username and password, which is compared to the information in the database.db and if they match, user is logged in, otherwise they see message and are not logged in.

    #### Log out is impossible if the user is not logged in, otherwise button is not jsut visible. When they see the button and click function jsut clears the session and user is logged out and returned to the log in page.

## Addition file:

    #### 6. __init.py__ contains function about the session, which helps to save information about user and session into the cookies.
    #### 7. config.py contains function which extract information from words.csv and recipes.csv files and imports it into database.db.
    #### 8. models.py contains function which connect to the database.db, which is after used in the routes.py.
    #### 9. routes.py contains every page main functions, which are described above in the pages section.
    #### 10. run.py contains functions which declares the app.
    #### 11. utils.py contains apologe for when user makes a mistake and is redirected to this page and login_required functions which checks if user is logged in.
    #### 12. Database.db is sqlite3 file containing necessary data about users, words and recipes.
    #### 13. words.csv and recipes.csv are files with words and recipes which are imported into database.db tables with help of config.py.
    #### 14. styles.css contains CSS styling for the HTML pages.
