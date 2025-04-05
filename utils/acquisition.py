import spacy 
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from sklearn.base import BaseEstimator, TransformerMixin

@Language.factory('language_detector')
def create_language_detector(nlp, name):
    return LanguageDetector()

class Language_Detector(BaseEstimator,TransformerMixin):
    """
    LanguageDetect is a transformer class that uses the spaCy library
    to detect the language of textual data. This class is designed to 
    be compatible with scikit-learn's pipeline structure, allowing 
    seamless integration into data processing workflows.

    Attributes:
    ----------
    nlp : spacy.language.Language
        The spaCy language model loaded for processing text.
    Methods:
    -------
    fit(X, y=None):
        Fits the transformer. This method does not perform any fitting 
        since language detection is not a learning process.
        
    transform(X):
        Detects the language of the text in the input DataFrame or Series 
        and appends a new column, 'detected_language', to the original data.
        
    _detect_language(text):
        Processes a single text input through the spaCy pipeline to 
        retrieve the detected language.
    """
    def __init__(self):
        super().__init__()
        self.nlp = spacy.load('en_core_web_sm')
    
        self.nlp.add_pipe('language_detector',last=True)

    def fit(self,X,y=None):
        return self 
    
    def transform(self,X):

        texts = X['text']

        detected_languages = texts.apply(self._detect_language)

        X['detected_language'] = detected_languages

        return X

    def _detect_language(self,text):
        doc = self.nlp(text)

        return doc._.language['language']

