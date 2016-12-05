from AlexaBaseHandler import AlexaBaseHandler
import requests
import inflect

class CurrencyConv(AlexaBaseHandler):
    """
    Sample concrete implementation of the AlexaBaseHandler to test the
    deployment scripts and process.
    All on_ handlers call the same test response changing the request type
    spoken.
    """

    def __init__(self):
        super(self.__class__, self).__init__()

    def _test_response(self, msg):
        session_attributes = {}
        card_title = "test card title"
        card_output = "test card output"
        speech_output = "type {0}".format(msg)
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = "test reprompt"
        should_end_session = False

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def _welcome_to_Curreny(self):
        session_attributes = {}
        card_title = "Welcome to Currency interact. You can ask me for a conversion for two Currencies. How can I help?"
        card_output = "Welcome to Currency interact. You can ask me for a conversion for two Currencies. How can I help?"
        speech_output = "Welcome to Curreny interact. You can ask me for a conversion for two Currencies. How can I help?"
        reprompt_text = "I am sorry, can you repeat your request?"
        should_end_session = False

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def _change_currency(self, intent, session):
        session_attributes = {}
        card_title = "get balance"
        card_output = "get balance"
        speech_output = "I can't find that account, You can ask me a balance to retrieve by saying for example, What is my savings account balance?"
        reprompt_text = "You can ask me to convert currency for example, convert AUS to EUR or convert 30 AUS to EUR "
        should_end_session = False
        amount = intent['slots']['AMOUNT']['value']
        money = intent['slots']['MONEY']['value']
        conv = intent['slots']['CONV']['value']

        # Lets call the API to get the currency conerted:
        requests.packages.urllib3.disable_warnings()
        r = requests.get("http://api.fixer.io/latest?symbols="+conv+"?base="+money, verify=False)
        return r.json()
        output = r[0]['rates'][conv][0]['value']

        p = inflect.engine()
        
        if len(amount) > 0:
           tot_amount = float(amount) * float(output)
           balance_arr = self._format_currency(tot_amount)
           speech_output = " %s and %s to be converted from %s into %s." % (p.number_to_words(balance_arr[0]), balance_arr[1], money, conv)
           reprompt_text = "You can ask me to convert currency for example, convert AUS to EUR or convert 30 AUS to EUR "
        else: 
           balance_arr = self._format_currency(output)
           speech_output = " %s converted into %s at current exchange rate is %s %s" % (p.number_to_words(money, conv, balance_arr[0]), balance_arr[1])
           speech_output = " %s to be converted into %s %s account. That is how you get your account balance like a boss" % (p.number_to_words(balance_arr[0]), balance_arr[1], account_type)
           reprompt_text = "You can ask me to convert currency for example, convert AUS to EUR or convert 30 AUS to EUR "

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def _format_currency(self, balance):
        balance_str = "%.2f" % balance
        balance_arr =  balance_str.split(".")

        if balance_arr[1] == "00":
            balance_arr[1] = "0"
        return balance_arr

    def _end_session(self, intent, session):
        session_attributes = {}
        card_title = "end session"
        card_output = "end session"
        reprompt_text = "I am sorry, can you repeat your request?"
        speech_output = "Thank you for using Currency conversion, we will miss you please come back soon"
        should_end_session = True
        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_processing_error(self, event, context, exc):
        return self._test_response("on processing error")

    def on_launch(self, launch_request, session):
        return self._welcome_to_Currency()

    def on_session_started(self, session_started_request, session):
        return self._test_response("on session started")

    def on_intent(self, intent_request, session):
        intent = intent_request['intent']
        intent_name = intent_request['intent']['name']
        print(intent_name)

        # Dispatch to your skill's intent handlers
        if intent_name == "Conversion":
            return self._change_currency(intent, session)
        else:
            raise ValueError("I do not understand what you have asked")

        return self._test_response("on intent")

    def on_session_ended(self, session_end_request, session):
        return self._test_response("on session end")


