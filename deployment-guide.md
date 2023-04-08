# Foodyssey Bot Deployment Guide

This guide will walk you through the process of deploying your Foodyssey bot on Heroku.

## Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- A Heroku account
- A GitHub account with the Foodyssey bot repository

## Deployment Steps

1. Log in to Heroku using the Heroku CLI:

   heroku login

   Follow the prompts to login.

2. Navigate to your local Foodyssey bot repository in the terminal or command prompt.
3. Create a new Heroku app:

   heroku create your-app-name

   Replace `your-app-name`with a unique name for your bot.

4. Set the environment variables `APP_ID` and `APP_PASSWORD` on Heroku:

   heroku config:set APP_ID=`<your-app-id>`
   heroku config:set APP_PASSWORD=`<your-app-password>`

   Replace `<your-app-id>` and `<your-app-password>`with your actual credentials.

5. Push your code to Heroku:

   git push heroku main

6. Scale your bot to run one instance:

   heroku ps:scale web=1

   Your bot should now be deployed on Heroku! You can access your bot using the URL `https://your-app-name.herokuapp.com`. Replace `your-app-name` with the name you chose instep3.

7. Update your bot's messaging endpoint: In the bot registration portal, update the messaging endpoint to point to the deployed Heroku URL: `https://your-app-name.herokuapp.com/api/messages`. Don't forget to replace `your-app-name` with your chosen name.

   Your bot is now deployed on Heroku and ready to receive messages.
