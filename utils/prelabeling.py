from itertools import groupby


def doc_to_spans(doc):
    # This function converts spaCy docs to the list of named entity spans in Label Studio compatible JSON format
    tokens = [(tok.text, tok.idx, tok.ent_type_) for tok in doc]
    results = []
    entities = set()
    for entity, group in groupby(tokens, key=lambda t: t[-1]):
        if not entity:
            continue
        group = list(group)
        _, start, _ = group[0]
        word, last, _ = group[-1]
        text = ' '.join(item[0] for item in group)
        end = last + len(word)
        results.append({
            'from_name': 'label',
            'to_name': 'text',
            'type': 'labels',
            'value': {
                'start': start,
                'end': end,
                'text': text,
                'labels': [entity]
            }
        })
        entities.add(entity)

    return results, entities
