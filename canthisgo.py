#!/usr/bin/env python3

import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.launch
def new_query():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent('OvenIntent')
def oven_start():
	oven_start_msg = render_template('oven_start')
	return statement(oven_start_msg)


@ask.intent('MicrowaveIntent')
def oven_start():
	oven_start_msg = render_template('microwave_start')
	return statement(microwave_start_msg)


@ask.intent('DishwasherIntent')
def oven_start():
	diswasher_start_msg = render_template('dishwasher_start')
	return statement(diswasher_start_msg)

# @ask.intent('OvenIntent')
# def oven():
#     oven_start_msg = render_template('oven_start')
#     return statement(speech_text).simple_card('HelloWorld', speech_text)


# @ask.intent('AMAZON.HelpIntent')
# def help():
#     speech_text = 'You can say hello to me!'
#     return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)