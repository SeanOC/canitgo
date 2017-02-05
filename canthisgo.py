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
    session.attributes['DEVICE'] = 'oven'
    session.attributes['YES_NEXT'] = 'done_positive'
    session.attributes['YES_IS_DONE'] = True
    session.attributes['NO_NEXT'] = 'composition_question'
    session.attributes['NO_IS_DONE'] = False
    session.attributes['YES_NO_STEP'] = 0
    return question(oven_start_msg)


@ask.intent('MicrowaveIntent')
def microwave_start():
    microwave_start_msg = render_template('microwave_start')
    session.attributes['DEVICE'] = 'microwave'
    session.attributes['YES_NEXT'] = 'done_positive'
    session.attributes['YES_IS_DONE'] = True
    session.attributes['NO_NEXT'] = 'metal_question'
    session.attributes['NO_IS_DONE'] = False
    session.attributes['YES_NO_STEP'] = 0
    return question(microwave_start_msg)


@ask.intent('DishwasherIntent')
def dishwasher_start():
    diswasher_start_msg = render_template('dishwasher_start')
    session.attributes['DEVICE'] = 'dishwasher'
    session.attributes['YES_NEXT'] = 'done_positive'
    session.attributes['YES_IS_DONE'] = True
    session.attributes['NO_NEXT'] = 'composition_question'
    session.attributes['NO_IS_DONE'] = False
    session.attributes['YES_NO_STEP'] = 0
    return question(diswasher_start_msg)


@ask.intent('AffirmativeIntent')
def affirmative():
    device = session.attributes['DEVICE']
    yes_next = session.attributes['YES_NEXT']
    yes_is_done = session.attributes['YES_IS_DONE']
    yes_no_step = session.attributes['YES_NO_STEP']

    if yes_no_step == 1:
        if device == 'microwave':
            yes_next = 'metal_done'
            yes_is_done = True

    template = '_'.join((device, yes_next))
    response_msg = render_template(template)


    session.attributes['YES_NO_STEP'] = yes_no_step + 1
    if yes_is_done:
        return statement(response_msg)
    else:
        return question(response_msg)


@ask.intent('NegativeIntent')
def negative():
    device = session.attributes['DEVICE']
    no_next = session.attributes['NO_NEXT']
    no_is_done = session.attributes['NO_IS_DONE']
    yes_no_step = session.attributes['YES_NO_STEP']


    if yes_no_step == 1:
        if device == 'microwave':
            no_next = 'plastic_start'
            no_is_done = False

    logging.info('device:  {}     no_next:  {}      yes_no_step:  {}'.format(device, no_next, yes_no_step))
    template = '_'.join((device, no_next))
    response_msg = render_template(template)
    
    session.attributes['YES_NO_STEP'] = yes_no_step + 1
    if no_is_done:
        return statement(response_msg)
    else:
        return question(response_msg)

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