import os
import sys

from cellSegmentation.logger import logging
from cellSegmentation.exception import AppException
from cellSegmentation.components.data_ingestion import DataIngestion
from cellSegmentation.components.data_validation import DataValidation
from cellSegmentation.components.model_trainer import ModelTrainer
from cellSegmentation.entity.config_entity import DataIngestionConfig, DataValidationConfig, ModelTrainerConfig
from cellSegmentation.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact, ModelTrainerArtifact


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.model_trainer_config = ModelTrainerConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Start data ingestion in Train Pipeline")
            logging.info("Getting data from url")
            
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info("Exited data ingestion in Train Pipeline")
            logging.info("Got data from url")
            
            return data_ingestion_artifact
        except Exception as e:
            raise AppException(e, sys)
        
    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    )-> DataValidationArtifact:
        
        logging.info("Enter data validation in Train Pipeline")
        try:
            data_validation = DataValidation(
                data_ingestion_artifacts=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed data validation operation")
            logging.info("Exited data validation in Train Pipeline")
            
            return data_validation_artifact
            
        except Exception as e:
            raise AppException(e, sys)
        
    def start_model_trainer(self) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise AppException(e, sys)
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            model_trainer_artifact = self.start_model_trainer()
            if data_validation_artifact.validation_status == True:
                model_trainer_artifact = self.start_model_trainer()
            else:
                raise Exception("Your data is not in correct format")
        except Exception as e:
            raise AppException(e, sys)
        
        
    
    
        
