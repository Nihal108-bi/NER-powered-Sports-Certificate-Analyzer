from dataclasses import dataclass


# Data Transformation Artifacts
@dataclass
class DataTransformationArtifacts:
    train_spacy_format_data_path: str
    test_spacy_format_data_path: str


@dataclass
class ModelTrainerArtifacts:
    trained_model_path: str