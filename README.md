# Foodyssey: Group Lunch Ordering Skype Bot 🍽️

Foodyssey is a Skype bot that streamlines group lunch orders, allowing users to initiate, place, and view a summary of orders within a specified time window. Ideal for office groups and friends, Foodyssey makes organizing group meals a breeze.

![Foodyssey Demo](demo.gif)

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Deployment](#deployment)
- [License](#license)

## Features

- 🍲 Simple commands for initiating lunch orders and placing individual orders.
- ⏲️ Automatic deadline for order submissions.
- 📋 Summary of all orders sent to the initiator after the deadline.

## Setup

1. Clone this repository
2. Install dependencies:

   pip install -r requirements.txt

3. Create a `.env` file in the project root folder with your skype credentials:

   skype_username=`<your-skype-username>`
   skype_password=`<your-skype-password>`

## Usage

1. Initiate lunch orders in a Skype group chat:

   /lunch <restaurant_name>

2. Place individual orders within the 30-minutewindow:

   /order <order_details>

3. Wait for the deadline to pass, and the initiator will receive a summary of all orders.

## Deployment

Follow the instructions in this [guide](deployment-guide.md) to deploy the bot on your preferred platform (e.g., Heroku).

## License

This project is licensed under the [MIT License](LICENSE).
