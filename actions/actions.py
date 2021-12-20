# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

#class ActionHelloWorld(Action):
#
#    def name(self) -> Text:
#        return "action_hello_world"
#
#    def run(self, dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#        dispatcher.utter_message(text= "Hello World!")
#
#        return []

class ActionUserLoggedIn(Action):

    def name(self) -> Text:
        return 'action_user_logged_in'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events= []
    
        if tracker.get_slot('user_provided_name') is None:
            dispatcher.utter_message(response= 'utter_submit_name_user_form')
            events.append(SlotSet('user_provided_name', True))
        
        return events

class ActionGetCurrentDialogTopic(Action):

    def name(self) -> Text:
        return 'action_get_current_dialog_topic'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_intent= tracker.latest_message['intent']['name']
        current_dialog_topic= tracker.get_slot('current_dialog_topic')

        if current_dialog_topic is None:
            dispatcher.utter_message(response= 'utter_not_know_about_current_dialog_yet')

        dispatcher.utter_message(text= current_dialog_topic)

        return []        
