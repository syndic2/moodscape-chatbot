def extract_entity(entity_name, entities= []):
    for e in entities:
        print('entity', e['entity'])
        print('value', e['value'])

        if e['entity'] == entity_name:
            return e['value']
    
    return None