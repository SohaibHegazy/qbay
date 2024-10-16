# Qbay - The Quiz Application

Welcome to Qbay! This platform allows you to create and take quizzes.

Qbay is designed to help you create a quiz of your own with any number of questions,
each question should have four possible answers with one of them correct.

You can also take a quiz and see your score.

Go to the profile page to access and control the quizzes you created.

In the profile page, you can also see the quizzes you have taken and their scores.

## Features

1- Customized Quiz Topic: Any user can create quiz in any topic.

2- Any Number of Questions: Users can determine how many question in their quiz.

3- Instant Result Update: Users receive their score instantly.

4- User Authentication: Secure user authentication for a personalized experience.

5- Quiz Control: Users can delete the quizzes they created.

## Usage

1- Create an account using the sign up link in the navigation menu or login if you have an account
2- Go to home page and click the "Create Quiz" button to create quiz or the "Take Quiz" button to take one.
3- If you created a quiz Enter the title and the number of questions and click create quiz.
4- You will then redirected to enter the question and the four choices, an select the correct one by checking the check box under the correct answer.
5- Click "save question" to be redirected to the next question.
6- When you reached the number of questions determined earlier, you will be prompted to click "Submit Quiz".
7- The quiz will show to all users in the page "Take Quiz"
8- If you take a quiz you should select the answers and then click submit quiz to see the score.


## Installation

To run this project locally for development purposes, follow the following in order:


1- Clone the repository to your local machine:

   ```shell
   git clone https://github.com/SohaibHegazy/quiz-app-django.git
   ```

2- Navigate to the project directory:

   ```shell
   cd qbay
   ```

3- Install dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4- Run migrations:

   ```shell
   python manage.py migrate
   ```


5- Start the development server:

   ```shell
   python manage.py runserver
   ```

6- Open your web browser and explore the project locally at [http://localhost:8000/](http://localhost:8000/).


