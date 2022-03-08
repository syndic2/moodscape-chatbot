# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from typing import Any, Text, Dict, List

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

class ValidateGetNameUserForm(FormValidationAction):
    def name(self) -> Text: 
        return 'validate_get_name_user_form'

    def validate_name_user(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        name_user= slot_value

        if name_user == 'initiate_bot_greet':
            return { 'name_user': None }

        return { 'name_user': slot_value }

class ActionInformShowDatePicker(Action):

    def name(self) -> Text:
        return 'action_inform_show_datepicker'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(json_message= dict({ 'is_show_datepicker': True }))

        return []

class ActionGiveMindfullnessVideo(Action):

    def name(self) -> Text:
        return 'action_give_mindfullness_video'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= 'Untuk membantu kamu dalam latihan Mindfullness ini, aku ada video yang mungkin dapat membantu kamu. Coba untuk melihat video yang aku kirimkan ini ya')
        dispatcher.utter_message(json_message= dict({ 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/4wKh265mCiA' }))

        return []