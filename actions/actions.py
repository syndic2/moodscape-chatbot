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

import random

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

        if name_user == '/initiate_bot_greet':
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
        dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/4wKh265mCiA' })

        return []

class ActionGetMeditation(Action):

    def name(self) -> Text:
        return 'action_get_meditation'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        meditation_type= tracker.get_slot('meditation_type')

        dispatcher.utter_message(text= f'Oke, kamu memilih meditaso {meditation_type} ya')
        dispatcher.utter_message(text= f'Aku akan memberikanmu sebuah video mengenai meditasi tersebut ya')

        if meditation_type == 'Mindfullness':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/4wKh265mCiA' })
        elif meditation_type == 'Focus':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/fIx0btrWaC8' })
        elif meditation_type == 'Visual':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/sStpgmiXPaM' })
        elif meditation_type == 'Spritual':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/G0QdWOcB6Ho' })
        elif meditation_type == 'Love':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/1eLKEuJkggw' })
        elif meditation_type == 'Trancendental':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/ZH-rEqP0Cdc' })
        elif meditation_type == 'Movement':
            dispatcher.utter_message(json_message= { 'is_show_video': True, 'video_url': 'https://www.youtube.com/embed/4MLCf9b_OdQ' })

        dispatcher.utter_message(
            text= f'Semoga video ini dapat membantu dalam memberikan gambaran lebih ke kamu mengenai teknik dari meditasi {meditation_type} ya', 
            buttons= [{ 'title': 'Iya, terima kasih. Aku akan mencobanya', 'payload': '/affirm_yes' }]
        )

        return []

class ActionShowMeditationImage(Action):

    def name(self) -> Text:
        return 'action_show_meditation_image'

    def run(self,  dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(json_message= { 'is_show_image': True, 'image_url': 'https://i.pinimg.com/originals/c1/42/22/c142226087319868314c6c1d5c94f3a7.gif' })

        return []

class ActionRandomJoke(Action):

    def name(self) -> Text:
        return 'action_random_joke'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        randomed_joke= random.choice([joke for joke in range(8)])
        dispatcher.utter_message(response= f'utter_joke_story_{randomed_joke+1}')

        return []