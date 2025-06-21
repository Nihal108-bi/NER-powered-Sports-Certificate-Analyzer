import os
from dataclasses import dataclass
from src.constant import *


@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.data_transformation_artifacts_dir: str = os.path.join(ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)

        self.data_file_path: str = os.path.join(DATA_DIRECTORY, DATA_FILE_NAME)

        self.train_annotation_path: str = os.path.join(DATA_DIRECTORY, TRAIN_ANNOTATION_FILE_NAME)

        self.test_annotation_path: str = os.path.join(DATA_DIRECTORY, TEST_ANNOTATION_FILE_NAME)


@dataclass
class ModelTrainingConfig:
    def __init__(self):
        self.model_training_artifacts_dir: str = os.path.join(ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)

        self.training_config_file_path: str = os.path.join(CONFIG_FILE_DIR, CONFIG_FILE_NAME)

        self.spacy_format_train_data_path = os.path.join(
                ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR, SPACY_TRAIN_DATA_FORMAT_NAME
            )
        
        self.spacy_format_test_data_path = os.path.join(
                ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR, SPACY_TEST_DATA_FORMAT_NAME
            )
        

@dataclass
class ModelPredictorConfig:
    def __init__(self):
        self.trained_model_path: str = os.path.join(ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR, BEST_MODEL_DIR)

        self.final_excel_file_path: str = os.path.join(os.getcwd(), OUTPUT_FILE_NAME)
