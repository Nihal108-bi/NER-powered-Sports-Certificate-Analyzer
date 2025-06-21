import os
import sys
import json
import logging
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from src.constant import *
from src.exception import NerException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifacts_entity import DataTransformationArtifacts
from src.utils.main_utils import MainUtils


# initiatlizing logger
logger = logging.getLogger(__name__)


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig) -> None:
        self.data_transformation_config = data_transformation_config
        self.utils = MainUtils()


    def create_spacy_format_data(self, data: json, docbin_obj: object, output_file_path: str, nlp_model: object):
        try:
            logger.info(
                "Entered the create_spacy_format_data method of Model transformation class"
            )
            for text, annot in tqdm(data["annotations"]):
                doc = nlp_model.make_doc(text)
                ents = []
                for start, end, label in annot["entities"]:
                    span = doc.char_span(
                        start, end, label=label, alignment_mode="contract"
                    )
                    if span is None:
                        print("Skipping entity")
                    else:
                        ents.append(span)
                doc.ents = ents
                docbin_obj.add(doc)

            docbin_obj.to_disk(output_file_path)  # save the docbin object
            logger.info(
                "Exited the create_spacy_format_data method of Model transformation class"
            )

        except Exception as e:
            raise NerException(e, sys) from e


    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        try:
            logger.info(
                "Entered the initiate_model_transformation method of Model transformation class"
            )

            os.makedirs(
                self.data_transformation_config.data_transformation_artifacts_dir, exist_ok=True
            )
            logger.info(
                f"Created {os.path.basename(self.data_transformation_config.data_transformation_artifacts_dir)} directory."
            )            

            # load a new spacy model
            nlp = spacy.blank("en")
            logger.info("Loaded new blank spacy model.")

            # create a DocBin object
            db = DocBin()
            logger.info("Created a new docbin object.")

            # load train json data file
            train_data = self.utils.read_json_file(json_data_path=self.data_transformation_config.train_annotation_path)
            logger.info("Loaded train json data")

            # load test json data file
            test_data = self.utils.read_json_file(json_data_path=self.data_transformation_config.test_annotation_path)
            logger.info("Loaded test json data")

            # definfng spacy format train data path
            spacy_format_train_data_path = os.path.join(
                ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR, SPACY_TRAIN_DATA_FORMAT_NAME
            )

            # definfng spacy format test data path
            spacy_format_test_data_path = os.path.join(
                ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR, SPACY_TEST_DATA_FORMAT_NAME
            )

            self.create_spacy_format_data(data=train_data, docbin_obj=db, output_file_path=spacy_format_train_data_path, nlp_model=nlp)
            logger.info("Converted train data into spacy format.")

            self.create_spacy_format_data(data=test_data, docbin_obj=db, output_file_path=spacy_format_test_data_path, nlp_model=nlp)
            logger.info("Converted test data into spacy format.")

            data_transformation_artifacts = DataTransformationArtifacts(train_spacy_format_data_path=spacy_format_train_data_path,
                                                                        test_spacy_format_data_path=spacy_format_test_data_path)
            
            logger.info("Exited the initiate_model_transformation method of Model transformation class")
            return data_transformation_artifacts
        
        except Exception as e:
            raise NerException(e, sys) from e