# Medical_NER
Using Spacy and Custom labels for Named-entity recognition. Trying to optimize the NER training and testing with BERT, GPT.

![alt text](image.png)

1. Spacy Classification 

`SpaCy Classification` → `Grammar Checker` → `Evaluation` → `GPT Evaluation`
   
    1. Grammar Checker using LanguageTools
   
    2. SPACY Labels 
![alt text](image-1.png)
    
    3. SPACY Evaluation for Manual Labels
   
    4. SPACY Evaluation with GPT 
![alt text](image-2.png)







2. Custom Labels 
`Custom Labels (TAG)` → `Empty Spacy NER Classifier` → `GPT Evaluation`

    1. SPACY Classifier
   
    3. SPACY Fine-Tuning
   
    5. Evaluation with GPT

3. BERT Classification 

![alt text](image-3.png)
<div style="display: flex; align-items: center; justify-content: center; font-family: Arial, sans-serif;">
    <div style="border: 2px solid black; padding: 10px; margin: 5px; text-align: center;">
        BERT Classifier
    </div>
    <div style="margin: 0 10px; font-size: 24px; font-weight: bold;">→</div>
    <div style="border: 2px solid black; padding: 10px; margin: 5px; text-align: center;">
        GPT Evaluation
    </div>
</div>
