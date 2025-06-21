import sys
import logging
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTraining
from src.entity.config_entity import DataTransformationConfig, ModelTrainingConfig
from src.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from src.exception import NerException


# initializing logger
logger = logging.getLogger(__name__)


class TrainPipeline:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainingConfig()


    # This method is used to start the data validation
    def start_data_transformation(self) -> DataTransformationArtifacts:
        logger.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config)

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logger.info("Performed the data transformation operation")
            
            logger.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )
            return data_transformation_artifact

        except Exception as e:
            raise NerException(e, sys) from e


    # This method is used to start the model trainer
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifacts) -> ModelTrainerArtifacts:
        logger.info("Entered the start_model_trainer method of TrainPipeline class")
        try:
            model_trainer = ModelTraining(
                data_transformation_artifacts=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_training()

            logger.info(
                "Exited the start_model_trainer method of TrainPipeline class"
            )
            return model_trainer_artifact

        except Exception as e:
            raise NerException(e, sys) from e
        

    def run_pipeline(self) -> None:
        logger.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            data_transformation_artifact = self.start_data_transformation()
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact) 

            logger.info(
                "Exited the run_pipeline method of TrainPipeline class"
            )

        except Exception as e:
            raise NerException(e, sys) from e