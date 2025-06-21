import os
import sys
import logging
from src.constant import *
from src.exception import NerException
from src.entity.config_entity import ModelTrainingConfig
from src.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifacts


# initiatlizing logger
logger = logging.getLogger(__name__)


class ModelTraining:
    def __init__(self, model_trainer_config: ModelTrainingConfig, data_transformation_artifacts: DataTransformationArtifacts) -> None:
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifacts: data_transformation_artifacts


    def initiate_model_training(self) -> ModelTrainerArtifacts:
        try:
            logger.info(
                "Entered the initiate_model_training method of Model training class"
            )

            os.makedirs(
                self.model_trainer_config.model_training_artifacts_dir, exist_ok=True
            )
            logger.info(
                f"Created {os.path.basename(self.model_trainer_config.model_training_artifacts_dir)} directory."
            )

            # Downloading the config file for training
            config_file_path = os.path.join(os.getcwd(), CONFIG_FILE_NAME)

            os.system(
                f"python -m spacy init config {config_file_path} --lang en --pipeline ner --optimize accuracy"
            )

            # Training
            best_model_path = os.path.join(ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)
            os.system(
                f"python -m spacy train {self.model_trainer_config.training_config_file_path} --output {best_model_path} --paths.train {self.model_trainer_config.spacy_format_train_data_path} --paths.dev {self.model_trainer_config.spacy_format_test_data_path}"
            )
            logger.info("Model training Done...!!")
            print("Model training Done...!!")

            model_trainer_artifacts = ModelTrainerArtifacts(trained_model_path=best_model_path)
            logger.info(
                "Exited the initiate_model_training method of Model training class"
            )
            return model_trainer_artifacts
        
        except Exception as e:
            raise NerException(e, sys) from e
