# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return 'action_hello_world'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= 'Halo dunia dari python file')

        return []

class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return 'action_search_restaurant'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities= tracker.latest_message['entities']
        message= 'Jenis restoran yang anda cari tidak valid, silahkan masukan lagi:)'

        for entity in entities:
            if entity['entity'] == 'restaurant':
                name= entity['value']
            
            if name == 'india':
                message= 'India1, India2, India3, India4, India5'
            elif name == 'china':
                message= 'China1, China2, China3, China4, China5'

        dispatcher.utter_message(text= message)

        return []

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return 'action_corona_tracker'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_response= requests.get('https://api.kawalcorona.com/indonesia/provinsi').json()
        province= ''
        case= None
        message= 'Nama provinsi yang anda masukkan tidak valid, silahkan masukan lagi :)'

        #extract entities
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'province':
                province= entity['value']

        #extract api response
        for data in api_response:
            if data['attributes']['Provinsi'] == province.title():
                case= data['attributes']

        if case:
            message= f"Positif: {case['Kasus_Posi']}, Sembuh: {case['Kasus_Semb']}, Meninggal: {case['Kasus_Meni']}"
        
        dispatcher.utter_message(text= message)

        return []

class ActionCountryPresidentName(Action):

    def name(self) -> Text:
        return 'action_country_president_name'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name= tracker.get_slot('name')
        country= tracker.get_slot('country');
        
        dispatcher.utter_message(text= f"{name}, {country}")

        return []

class ValidateEmailSubscriptionForm(FormValidationAction):

    def name(self) -> Text:
        return 'validate_email_subscription_form'

    def validate_name_user(self, slot_value: Any, 
            dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> Dict[Text, Any]:

        if len(slot_value) <= 2:
            dispatcher.utter_message(text= 'Nama yang anda masukkan terlalu pendek. Saya mengasumsikan anda salah ketik.')
            return { 'name_user': None }

        return { 'name_user': slot_value }

