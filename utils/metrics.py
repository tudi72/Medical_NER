from collections import defaultdict 
import itertools
import pandas as pd
import json 
import ast

def compute_ner_metrics(ground_truth, eval_corpus, print_falses=False):
    """
    Compute the precision, recall, and F1 score based on ground truth and evaluation sets.

    Parameters:
        ground_truth (pd.Series): Ground truth annotations (list of entity labels).
        eval_corpus (pd.Series): Evaluation annotations (list of entity labels).

    Returns:
        dict: Dictionary containing precision, recall, and F1 score.
    """
    # Convert ground truth and eval annotations to sets of unique labels
    if isinstance(ground_truth, (pd.DataFrame, pd.Series)):
        ground_set = set(ground_truth.explode().dropna().tolist())
    else:
        flat_list = [item for sublist in ground_truth for item in sublist]
        ground_set = set(flat_list)
    eval_set = set(eval_corpus.explode().dropna().tolist())
    
    # Calculate true positives, false positives, and false negatives
    true_positives = ground_set.intersection(eval_set)
    false_positives = eval_set.difference(ground_set)
    false_negatives = ground_set.difference(eval_set)

    # Calculate precision, recall, and F1 score
    precision = len(true_positives) / (len(true_positives) + len(false_positives)) if len(true_positives) + len(false_positives) > 0 else 0
    recall = len(true_positives) / (len(true_positives) + len(false_negatives)) if len(true_positives) + len(false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    # Print the metrics
    print(f"Precision\t\t: {precision:.2f}")
    print(f"Recall\t\t\t: {recall:.2f}")
    print(f"F1 Score\t\t: {f1:.2f}")

    # Optionally, print the false positives and false negatives
    if print_falses:
        print("\nFalse Negatives:")
        print(false_negatives)
        
        print("\nFalse Positives:")
        print(false_positives)
    else:
        print(f"\nFalse Negatives: {len(false_negatives)}")
        print(f"\nFalse Positives: {len(false_positives)}")

    # Return the metrics in a dictionary
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }


def count_ner_labels(corpus, ner_column='entities'):
    """
    Count the frequency of NER labels in the given corpus.
    
    Parameters:
        corpus (pandas.DataFrame): DataFrame containing NER annotations.
        ner_column (str): The name of the column containing the NER annotations (list of tuples).

    Returns:
        sorted_counts (list): Sorted list of tuples (label, count) from highest to lowest frequency.
    """
    # Flatten the list of NER annotations (word, label) from the 'entities' column
    custom_ner_results = corpus[ner_column].apply(lambda x: list(x))
    custom_ner_results = list(itertools.chain.from_iterable(custom_ner_results))

    # Dictionary to count occurrences of each NER label
    counts_dict = defaultdict(int)

    # Iterate through the list of NER tuples (word, NER label)
    for _, label in custom_ner_results:
        counts_dict[label] += 1

    # Sort labels by frequency from most to least frequent
    sorted_counts = sorted(counts_dict.items(), key=lambda item: item[1], reverse=True)

    # Find the maximum length of the label to align the output properly
    max_length = max(len(key) for key in counts_dict.keys())

    # Print the counts sorted by frequency
    for key, value in sorted_counts:
        print(f"[{key.ljust(max_length)}] : {value}")

    return sorted_counts  # Return the sorted list if you need to use it elsewhere

def read_ner_with_index_annotations(JSON_FILE):
    # Initialize lists to store texts and their corresponding annotations
    annotations_dict = []

    # Open and load the JSON file
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)

    # Iterate over each item in the JSON data
    for item in data:
        
        # Extract the 'annotations' (label and text) and ensure correct order
     

        annotations = list(
            {
                (
                    annotation['value']['start'],  # Start position
                    annotation['value']['end'],    # End position
                    annotation['value']['labels'][0]  # Label
                )
                for annotation in item['annotations'][0]['result']
            }
        )

        unique_annotations = list(set(tuple(annotation) for annotation in annotations))

        data_dict = [
                        item['data']['text'],
                        {
                            "entities": unique_annotations
                        }
                ]      


        # Append the annotations for each text
        annotations_dict.append(data_dict)


    return annotations_dict

def read_ner_annotations(JSON_FILE):
    # Initialize lists to store texts and their corresponding annotations
    texts = []
    annotations_list = []

    # Open and load the JSON file
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)

    # Iterate over each item in the JSON data
    for item in data:
        # Extract the 'text' from the 'data' field
        text_content = item['data']['text']
        texts.append(text_content)
        
        # Extract the 'annotations' (label and text) and ensure correct order
        annotations = [
            (annotation['value']['text'], annotation['value']['labels'][0])
            for annotation in item['annotations'][0]['result']
        ]
        
        # Append the annotations for each text
        annotations_list.append(annotations)

    # Create a DataFrame from the texts and their annotations
    df = pd.DataFrame({
        'text': texts,
        'annotations': annotations_list
    })

    return df


def read_ner_annotations_for_bert(JSON_FILE):
    # Initialize lists to store texts and their corresponding annotations
    texts = []
    annotations_list = []

    # Open and load the JSON file
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)

    # Iterate over each item in the JSON data
    for item in data:
        # Extract the 'text_content' from the 'data' field
        text_content = item['data']['text']
        texts.append(text_content)

        annotations = []
        for annotation in item['annotations'][0]['result']:
            text = annotation['value']['text']

            start_offset = annotation['value']['start']
            end_offset = annotation['value']['end']
            label = annotation['value']['labels'][0]

            start_word_id = len(text_content[:start_offset].split())
            end_word_id = len(text_content[:end_offset].split()) - 1

            annotation_extracted = (
                (text, label, (start_word_id, end_word_id))
            )
            annotations.append(annotation_extracted)

        # Append the annotations for each text
        annotations_list.append(annotations)

    # Create a DataFrame from the texts and their annotations
    df = pd.DataFrame({
        'text': texts,
        'annotations': annotations_list
    })

    return df


# function to convert the dataframe entities from string --> lsit
def convert_string_to_list(s):
    try:
        # Handle empty or null values
        if pd.isna(s) or s == '[]':
            return []
        # Remove any extra whitespace and evaluate the string
        cleaned_s = s.strip()
        return ast.literal_eval(cleaned_s)
    except Exception as e:
        print(f"Error parsing: {s}")
        print(f"Error message: {str(e)}")
        return []