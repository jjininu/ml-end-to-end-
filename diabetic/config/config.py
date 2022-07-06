from distutils.command.config import config
from diabetic.Entity.entity_config import DataIngestionConfig, DataValidationConfig,TrainingPipelineConfig
from diabetic.logger  import * 
from diabetic.logger import logging                        
from diabetic.Entity import entity_config,entity_artifact
from diabetic.constant.constant import *
import diabetic.exception
import os,sys
from diabetic.util import util
from diabetic.exception import CustomException



class Configuartion:

    def __init__ (self,config_file_path=CONFIG_FILE_PATH,current_time_stamp = CURRENT_TIME_STAMP ) -> None:
        self.config_file_path = config_file_path
        self.current_time_stamp = CURRENT_TIME_STAMP
        self.training_pipeline_config  = self.get_training_pipeline_config()
        self.config_info = util.read_yaml_file(self.config_file_path)

    def get_data_ingestion_config(self) ->DataIngestionConfig:
        try:
            artifact = self.training_pipeline_config.artifact_dir
            data_ingestion_config = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_dir = os.path.join(artifact,data_ingestion_config,
                                               data_ingestion_config[DATA_INGESTION_ARTIFACT_DIR],
                                                   self.current_time_stamp)
            data_ingestion_url = data_ingestion_config[DATA_INGESTION_DOWNLOAD_URL_KEY]
            data_ingestion_tgz_dir = data_ingestion_config[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            data_ingestion_tgz = os.path.join(data_ingestion_dir,data_ingestion_tgz_dir)
            raw_data_dir = os.path.join(data_ingestion_dir,DATA_INGESTION_RAW_DATA_DIR_KEY)
            ingested_data = os.path.join(data_ingestion_dir,
                                       data_ingestion_config[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            ingested_train_dir = os.path.join(ingested_data,data_ingestion_config[DATA_INGESTION_TRAIN_DIR_KEY])
            ingested_test_dir= os.path.join(ingested_data,data_ingestion_config[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config=DataIngestionConfig(
                                     dataset_download_url=data_ingestion_url,
                                     tgz_download_dir = data_ingestion_tgz,
                                     raw_data_dir = raw_data_dir,
                                     ingested_train_dir = ingested_train_dir,
                                     ingested_test_dir = ingested_test_dir)
        except Exception as e:
            raise diabetic.exception(e,sys) from e

    def get_data_validation(self)->DataValidationConfig:
            try:
                schema_file_path = os.path.join(ROOT_DIR,config)
                artifact = self.training_pipeline_config.artifact_dir
                schema_dir = DATA_VALIDATION_ARTIFACT_DIR_NAME
                data_validation_dir = os.path.join(artifact,schema_dir,self.current_time_stamp)
                data_validation_schema_file = os.path.join(ROOT_DIR,schema_file_path,)
                data_validation_report_file = os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME_KEY)
                report_page_file_path = os.path.join(data_validation_dir,
                                    data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

                data_validation_config = DataValidationConfig(schema_file_path=data_validation_dir,
                                                              report_file_path = data_validation_report_file,
                                                              report_page_file_path = report_page_file_path)

            except Exception as e:
                raise CustomException(e,sys)


    

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            main = os.cwd()
            config_info = util.read_yaml_file(file_path=CONFIG_FILE_PATH)
            pipeline_config = config_info[TRAINING_PIPELINE_CONFIG_KEY]
            pipelilename = pipeline_config[TRAINING_PIPELINE_NAME_KEY]
            pipeline_artifact = pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            artifact_dir = os.path.join(main,pipelilename,pipeline_artifact)

            trainingpipelineconfig = TrainingPipelineConfig( artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {trainingpipelineconfig}")
            return trainingpipelineconfig

            


            
        except Exception as e:
            raise diabetic.exception(e,sys)







