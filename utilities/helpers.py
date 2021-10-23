def extract_entity(entity_name, entities= []):
    print('entities', entities)

    for e in entities:
        print('entity', e['entity'])

        if e['entity'] ==  entity_name:
            return e['value']
    
    return ''