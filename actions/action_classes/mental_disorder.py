from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import requests

from utilities.constants import api_urls
from utilities.helpers import extract_entity

not_yet_learn_template= 'utter_not_yet_learn_mental_disorder'

def get_mental_disorder(mental_disorder_name):
    response= requests.get(f'{api_urls["development"]}/mental-disorders?name={mental_disorder_name}').json()

    if len(response['mental_disorders']) == 0:
        return None
    
    return response['mental_disorders'][0]

class ActionDescription(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_description'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())
        
        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            dispatcher.utter_message(text= mental_disorder_dict['short_description'])

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)] 

class ActionTypes(Action):
     
    def name(self) -> Text:
         return 'action_mental_disorder_types'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            types= ''

            if len(mental_disorder_dict['types']) == 0:
                types= 'Gangguan ini tidak memiliki jenis'
            else:
                for type in mental_disorder_dict['types']:
                    types+= '- '+type['name']+'\n'
                    types+= '  \u2022 '+type['short_description']+'\n'

            dispatcher.utter_message(text= types)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionSignsAndSympthomps(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_signs_and_sympthomps'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())          

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            signs_and_sympthomps= ''

            for item in mental_disorder_dict['signs_and_sympthomps']:
                signs_and_sympthomps+= '- '+item['point']+'\n'

                if len(item['description_points']) != 0: 
                    for description_point in item['description_points']:
                        signs_and_sympthomps+= '  \u2022 '+description_point+'\n'

            dispatcher.utter_message(text= signs_and_sympthomps)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionCauses(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_causes'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())  

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            causes= ''

            for cause in mental_disorder_dict['causes']:
                causes+= '- '+cause+'\n'

            dispatcher.utter_message(text= causes)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionDiagnosis(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_diagnosis'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())  

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            diagnosis= ''

            for item in mental_disorder_dict['diagnosis']:
                diagnosis+= '- '+item['point']+'\n'

                if item['description'] != '':
                    diagnosis+= '  \u2022 '+item['description']+'\n'

            dispatcher.utter_message(text= diagnosis)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionComplications(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_complications'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())  

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            complications= ''

            for complication in mental_disorder_dict['complications']:
                complications+= '- '+complication+'\n'

            dispatcher.utter_message(text= complications)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionHowToTreat(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_how_to_treat'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())  

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else:
            how_to_treat= ''

            for item in mental_disorder_dict['how_to_treat']:
                how_to_treat+= '\u2022 '+item['point']+'\n'
                
                if item['description'] != '':
                    how_to_treat+= '  - '+item['description']+'\n'

                for description_point in item['description_points']:
                    how_to_treat+= '   \u2022 '+description_point+'\n'

            dispatcher.utter_message(text= how_to_treat)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]

class ActionHowToPrevent(Action):

    def name(self) -> Text:
        return 'action_mental_disorder_how_to_prevent'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder_dict= get_mental_disorder(mental_disorder_name.title())  

        if mental_disorder_dict is None:
            dispatcher.utter_message(response= not_yet_learn_template)
        else: 
            how_to_prevent= ''

            for item in mental_disorder_dict['how_to_prevent']:
                how_to_prevent+= item+'\n'

            dispatcher.utter_message(text= how_to_prevent)

        return [SlotSet('mental_disorder_dict', mental_disorder_dict)]