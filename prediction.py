import os
import sys
import spacy
import logging
import pandas as pd
from src.constant import *
from pandas import DataFrame
from src.exception import NerException
from src.entity.config_entity import ModelPredictorConfig
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification


# initializing logger
logger = logging.getLogger(__name__)


class ModelPredictor:
    def __init__(self) -> None:
        self.model_predictor_config = ModelPredictorConfig()

    def bert_person_extraction(self, model: object, tokenizer: object, text: str) -> str:
        try:
            logger.info("Entered the bert_person_extraction method of Model predictor class")

            nlp = pipeline("ner", model=model, tokenizer=tokenizer)

            ner_results = nlp(text)

            # Extract 'word' for entities of type 'PER'
            per_entities = [entity['word'] for entity in ner_results if entity['entity'] == 'B-PER' or entity['entity'] == 'I-PER']

            # save the extracted 'word' for PER entities
            person_name = " ".join(per_entities)

            logger.info("Exited the bert_person_extraction method of Model predictor class")
            return person_name

        except Exception as e:
            raise NerException(e, sys) from e
        

    def spacy_info_extraction(self, prediction_data_df: DataFrame, spacy_model: object, bert_model: object,
                              bert_tokenizer: object) -> dict:
        try:
            logger.info("Entered the spacy_info_extraction method of Model predictor class")

            extracted_info = []
            for desc in prediction_data_df['Certificate Description']:
                doc = spacy_model(desc)

                sports_name = None
                winning_position = None
                org_year = None

                for ent in doc.ents:
                    if ent.label_ == 'SPORTS_NAME':
                        sports_name = ent.text
                    elif ent.label_ == 'WINNING_POSITION':
                        winning_position = ent.text
                    elif ent.label_ == 'ORG_YEAR':
                        org_year = ent.text

                # Extracting person name using the BERT model
                participant_name = self.bert_person_extraction(model=bert_model, tokenizer=bert_tokenizer, text=desc)

                extracted_info.append({
                    'participent_name': participant_name,
                    'sports_name': sports_name,
                    'winning_position': winning_position,
                    'org_year': org_year
                })

            logger.info("Entered the spacy_info_extraction method of Model predictor class")
            return extracted_info
        
        except Exception as e:
            raise NerException(e, sys) from e
        

    def initiate_model_predictor(self, excel_file_path: str) -> None:
        try:
            logger.info("Entered the initiate_model_predictor method of Model predictor class")

            bert_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
            logger.info("Loaded the tokenizer")

            bert_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
            logger.info("Loaded the bert model")

            # Loading spaCy NER model
            spacy_model = spacy.load(self.model_predictor_config.trained_model_path)
            logger.info("Loaded the spacy model")

            # Load the new data from the Excel file
            prediction_data_df = pd.read_excel(excel_file_path, 'Data-Pending', header=None, names=['Certificate Description'])

            # Extract information from the certificate descriptions
            extracted_info = self.spacy_info_extraction(prediction_data_df=prediction_data_df, spacy_model=spacy_model,
                                                        bert_model=bert_model, bert_tokenizer=bert_tokenizer)
            logger.info("Extracted the necessary information from the prediction data.")

            # Create a new DataFrame with the extracted information
            result_df = pd.DataFrame(extracted_info)
            result_df.insert(0, column="Certificate Description",  value=prediction_data_df['Certificate Description'])
            logger.info("Created a dataframe from the extracted information")

            result_df.to_excel(self.model_predictor_config.final_excel_file_path)
            logger.info("Exited the initiate_model_predictor method of Model predictor class")

        except Exception as e:
            raise NerException(e, sys) from e
        

if __name__ == "__main__":
    model_predictor = ModelPredictor()

    prediction_file_path = os.path.join(DATA_DIRECTORY, DATA_FILE_NAME)
    model_predictor.initiate_model_predictor(excel_file_path=prediction_file_path)
    