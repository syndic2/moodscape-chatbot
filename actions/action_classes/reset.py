from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

class ActionResetBriefCOPEEvaluation(Action):

    def name(self) -> Text:
        return 'action_reset_brief_cope_evaluation'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        events= []

        for i in range(28):
            events.append(SlotSet(f'brief_cope_answer.score_{i+1}', None))

        return events

class ActionResetExploreMentalDisorder(Action):

    def name(self) -> Text:
        return 'action_reset_explore_mental_disorder'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet('explore_mental_disorder_name', None)]