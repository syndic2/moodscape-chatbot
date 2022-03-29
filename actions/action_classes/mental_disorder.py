from typing import Any, Text, Dict, List
from matplotlib.pyplot import text
from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

import requests

from utilities.constants import api_urls
from utilities.helpers import extract_entity

api_url= api_urls["production"]
not_yet_learn_template= 'utter_not_yet_learn_mental_disorder'

def get_mental_disorder(mental_disorder_name):
    response= requests.get(f'{api_url}/mental-disorders?name={mental_disorder_name}').json()

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

                if isinstance(item['description'], list):
                    if len(item['description']) != 0:
                        for description in item['description']:
                            diagnosis+= '  \u2022 '+description+'\n'
                else:
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
            how_to_prevent= 'Maaf data cara mencegah gangguan ini belum tersedia atau mungkin aku yang belum mengerti'
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

        mental_disorders= requests.get(f'{api_url}/mental-disorders/list').json()['mental_disorders']
        response_text= ''

        for i in range(len(mental_disorders)):
            response_text+= f"{i+1}. {mental_disorders[i]['name']}\n"

        dispatcher.utter_message(text= response_text)

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

#In story
class ActionExploreMentalDisorderDescription(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_description'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
           
        dispatcher.utter_message(text= f"Baik, aku akan menjelaskannya ya. Untuk yang pertama yaitu pengertian dari {mental_disorder_name}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'short_description'), buttons= buttons)

        return []

class ActionExploreMentalDisorderTypes(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_types'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikut yaitu merupakan jenis dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'types'), buttons= buttons)

        return []

class ActionExploreMentalDisorderSignsAndSympthomps(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_signs_and_sympthomps'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikutnya yaitu merupakan tanda dan gejala dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'signs_and_sympthomps'), buttons= buttons)

        return []

class ActionExploreMentalDisorderCauses(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_causes'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikut yaitu merupakan penyebab dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'causes'), buttons= buttons)

        return []

class ActionExploreMentalDisorderDiagnosis(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_diagnosis'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikut yaitu merupakan cara mendiagnosa dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'diagnosis'), buttons= buttons)            

        return []

class ActionExploreMentalDisorderComplications(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_complications'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikut yaitu merupakan komplikasi yang dapat terjadi dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'complications'), buttons= buttons)          

        return []

class ActionExploreMentalDisorderHowToTreat(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_how_to_treat'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
        buttons= [
            { 'title': 'Lanjut',  'payload': '/continue_explore_mental_disorders' },
            { 'title': 'Berhenti', 'payload': '/stop_explore_mental_disorders' } 
        ]
            
        dispatcher.utter_message(text= f"Berikut yaitu cara menangani dari gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_treat'), buttons= buttons)        

        return []

class ActionExploreMentalDisorderHowToPrevent(Action):

    def name(self) -> Text:
        return 'action_explore_mental_disorder_how_to_prevent'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mental_disorder_index= int(tracker.get_slot('explore_mental_disorder_name'))-1
        mental_disorder_name= tracker.get_slot('explore_mental_disorder_list')[mental_disorder_index]['name']

        response= requests.get(f'{api_url}/mental-disorders/by-name/{mental_disorder_name}').json()

        if response['status'] is False:
            dispatcher.utter_message(response= not_yet_learn_template)
            return []

        mental_disorder= response['mental_disorder']
            
        dispatcher.utter_message(text= f"Terakhir yaitu merupakan cara mencegah atau mengurangi timbulnya gangguan {mental_disorder['name']}")
        dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'how_to_prevent'))        

        return []


#In rules
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

class ActionSelfDiagnoseTerms(Action):

    def name(self) -> Text:
        return 'action_self_diagnose_terms'

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:  

        mental_disorder_name= tracker.get_slot('mental_disorder')
        mental_disorder= get_mental_disorder(mental_disorder_name.title()) 

        dispatcher.utter_message(text= f'Oh iya tadi kalau tidak salah dengar, kamu menyinggung tentang gangguan {mental_disorder_name} ya?')
        dispatcher.utter_message(text= f'Ini sebagai informasi tambahan untuk kamu ya mengenai ciri-ciri dari gangguan {mental_disorder_name}') 

        if mental_disorder is not None:
            dispatcher.utter_message(
                text= 'Maaf, sepertinya untuk data tersebut aku belum memiliki informasinya. Untuk membantu pengembangan, kamu bisa melaporkan pesan ini ya', 
                buttons= [{ 'title': 'Oh, okay kalo begitu. Terima kasih', 'payload': '/affirm_yes'}]
            )
        else:
            dispatcher.utter_message(text= get_mental_disorder_detail(mental_disorder, 'signs_and_sympthomps'), buttons= [{ 'title': 'Terima kasih atas tambahan informasinya', 'payload': '/affirm_yes'}])

        return []