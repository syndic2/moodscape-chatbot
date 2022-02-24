from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

import requests

from utilities.constants import api_urls
from utilities.helpers import extract_entity

not_yet_learn_template= 'utter_not_yet_learn_mental_disorder'

def get_mental_disorder(mental_disorder_name):
    response= requests.get(f'{api_urls["development"]}/mental-disorders?name={mental_disorder_name}').json()

    if len(response['mental_disorders']) == 0:
        return None
    
    return response['mental_disorders'][0]

def get_mental_disorder_detail(mental_disorder, field):
    if field == 'short_description': 
        return mental_disorder['short_description']

    elif field == 'types':
        types= ''

        if len(mental_disorder['types']) == 0:
            types= 'Maaf, data jenis dari gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for type in mental_disorder['types']:
                types+= '- '+type['name']+'\n'
                types+= '  \u2022 '+type['short_description']+'\n'

        return types

    elif field == 'signs_and_sympthomps':
        signs_and_sympthomps= ''

        if len(mental_disorder['signs_and_sympthomps']) == 0:
            signs_and_sympthomps= 'Maaf, data untuk tanda dan gejala dari gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for item in mental_disorder['signs_and_sympthomps']:
                signs_and_sympthomps+= '- '+item['point']+'\n'

                if len(item['description_points']) != 0: 
                    for description_point in item['description_points']:
                        signs_and_sympthomps+= '  \u2022 '+description_point+'\n'

        return signs_and_sympthomps

    elif field == 'causes':
        causes= ''

        if len(mental_disorder['causes']) == 0:
            causes= 'Maaf, data untuk penyebab dari gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for cause in mental_disorder['causes']:
                causes+= '- '+cause+'\n'
        
        return causes

    elif field == 'diagnosis':
        diagnosis= ''
        
        if len(mental_disorder['diagnosis']) == 0:
            diagnosis= 'Maaf, data cara mendiagnosa gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for item in mental_disorder['diagnosis']:
                diagnosis+= '- '+item['point']+'\n'

                if item['description'] != '':
                    diagnosis+= '  \u2022 '+item['description']+'\n'

        return diagnosis
    
    elif field == 'complications':
        complications= ''

        if len(mental_disorder['complications']) == 0:
            complications= 'Maaf, data untuk efek komplikasi dari gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for complication in mental_disorder['complications']:
                complications+= '- '+complication+'\n'

        return complications
    
    elif field == 'how_to_treat': 
        how_to_treat= ''

        if len(mental_disorder['how_to_treat']) == 0:
            how_to_treat= 'Maaf, data untuk cara menangani gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
        else:
            for item in mental_disorder['how_to_treat']:
                how_to_treat+= '\u2022 '+item['point']+'\n'
                
                if item['description'] != '':
                    how_to_treat+= '  - '+item['description']+'\n'

                for description_point in item['description_points']:
                    how_to_treat+= '   \u2022 '+description_point+'\n'
        
        return how_to_treat
    
    elif field == 'how_to_prevent':
        how_to_prevent= ''

        if len(mental_disorder['how_to_prevent']) == 0:
            how_to_prevent= 'Maaf data cara mencegah gangguan ini belum tersedia atau mungki aku yang belum mengerti'
        else:
            for item in mental_disorder['how_to_prevent']:
                how_to_prevent+= item+'\n'
        
        return how_to_prevent

class ActionGetMentalDisorderList(Action):

   def name(self) -> Text:
       return 'action_get_mental_disorder_list'

   def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        

        mental_disorders= requests.get(f'{api_urls["development"]}/mental-disorders/list').json()['mental_disorders']
        response_text= ''

        for i in range(len(mental_disorders)):
            response_text+= f"{i+1}. {mental_disorders[i]['name']}\n"

        dispatcher.utter_message(text= response_text)
        dispatcher.utter_message(text= 'Untuk sekarang masih harus memilih dengan menulis manual gangguann mana yang kamu ingin kamu tau ya')

        return [SlotSet('explore_mental_disorder_list', mental_disorders)]

class ValidateGetExploreMentalDisorderNameForm(FormValidationAction):
    def name(self) -> Text: 
        return 'validate_get_explore_mental_disorder_name_form'

    def validate_explore_mental_disorder_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        mental_disorder_list= tracker.get_slot('explore_mental_disorder_list')

        try:
            mental_disorder_index= int(slot_value)
        except:
            dispatcher.utter_message(text= 'Inputan harus berupa angka')
            return { 'explore_mental_disorder_name': None }

        if mental_disorder_index > len(mental_disorder_list) or mental_disorder_index < 1:
            dispatcher.utter_message(text= 'Nomor yang dimasukkan tidak sesuai')
            return { 'explore_mental_disorder_name': None }

        return { 'explore_mental_disorder_name': slot_value }

class ActionGetMentalDisorderDetail(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_detail'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_urls["development"]}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(template= not_yet_learn_template)

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
        next_field= tracker.get_slot('next_explore_mental_disorder_field')
        
        if next_field is None:
            buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "types" }'
            
            dispatcher.utter_message(text= 'Baik, aku akan menjelaskannya ya')
            dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'short_description'), buttons= buttons)
        else:
            if next_field == 'types':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "signs_and_sympthomps" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan jenis dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'types'), buttons= buttons)
            elif next_field == 'signs_and_sympthomps':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "causes" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan tanda dan gejala dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'signs_and_sympthomps'), buttons= buttons)
            elif next_field == 'causes':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "diagnosis" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan penyebab dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'causes'), buttons= buttons)
            elif next_field == 'diagnosis':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "complications" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan cara mendiagnosa dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'diagnosis'), buttons= buttons)            
            elif next_field == 'complications':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "how_to_treat" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan komplikasi yang dapat terjadi dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'complications'), buttons= buttons)
            elif next_field == 'how_to_treat':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": "how_to_prevent" }'

                dispatcher.utter_message(text= f"Berikut dibawah merupakan cara menangani dari gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_treat'), buttons= buttons)
            elif next_field == 'how_to_prevent':
                buttons[0]['payload']= '/continue_explore_mental_disorders{ "next_explore_mental_disorder_field": None }'

                dispatcher.utter_message(text= f"Terakhir yaitu merupakan cara mencegah atau mengurangi timbulnya gangguan {mental_disorder['name']}")
                dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_prevent'))

        return []

class ActionGetMentalDisorderDescription(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_description'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'short_description')) 

        return [] 

class ActionGetMentalDisorderTypes(Action):
     
    def name(self) -> Text:
         return 'action_get_mental_disorder_types'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'types'))

        return []

class ActionGetMentalDisorderSignsAndSympthomps(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_signs_and_sympthomps'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())          

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'signs_and_sympthomps'))

        return []

class ActionGetMentalDisorderCauses(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_causes'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())  

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'causes'))

        return []

class ActionMentalDisorderDiagnosis(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_diagnosis'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())  

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'diagnosis'))

        return []

class ActionGetMentalDisorderComplications(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_complications'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())  

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'complications'))

        return []

class ActionGetMentalDisorderHowToTreat(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_how_to_treat'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())  

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_treat'))

        return []

class ActionGetMentalDisorderHowToPrevent(Action):

    def name(self) -> Text:
        return 'action_get_mental_disorder_how_to_prevent'
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_name= extract_entity('mental_disorder', tracker.latest_message['entities'])        
        mental_disorder= get_mental_disorder(mental_disorder_name.title())  

        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_prevent'))

        return []