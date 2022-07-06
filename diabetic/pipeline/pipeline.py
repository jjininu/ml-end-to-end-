from diabetic.config.config import Configuartion
from diabetic.logger import logging
from diabetic.exception import CustomException

from diabetic.Entity.entity_artifact   import DataIngestionArtifacts
from diabetic.Entity.entity_config import DataIngestionConfig
from diabetic.component.data_ingestion import DataIngestion

import os,sys

class Pipeline:

    def __init__(self,config: Configuartion = Configuartion()) -> None:
        try:
            self.config=config


        except Exception as e:
            raise CustomException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e    

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e

    