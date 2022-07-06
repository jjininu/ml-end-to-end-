from diabetic.Entity.entity_config import DataIngestionConfig
import sys,os
from diabetic.exception import CustomException
from diabetic.logger import logging
from diabetic.Entity.entity_artifact import DataIngestionArtifacts
import tarfile
import numpy as np
#from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from diabetic.exception import CustomException
import urllib

class DataIngestion:
    def __init__(self,dataingestionconfig:DataIngestionConfig):
        self.dataingestionconfig = dataingestionconfig


    def download_data (self):
        logging.info("data ingestion started")
        try:
            url = self.dataingestionconfig.dataset_download_url
            download_folder_location = self.dataingestionconfig.tgz_download_dir
            file_name = os.path.basename(url)
            tgz_file_path =os.path.join(download_folder_location,file_name)
            urllib.request.urlretrieve(url, tgz_file_path)
            if os.path.exists(tgz_file_path):
                os.remove(tgz_file_path)
            os.makedirs(tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path
        except Exception as e:
            raise CustomException(e,sys)
    
    def extract_tgz (self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    def split_data_as_train_test(self) -> DataIngestionArtifacts:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            diabetic_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{diabetic_file_path}]")
            diabetic_data_frame = pd.read_csv(diabetic_file_path)

   
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(diabetic_data_frame, diabetic_data_frame):
                strat_train_set = diabetic_data_frame.loc[train_index]#.drop(["income_cat"],axis=1)
                strat_test_set = diabetic_data_frame.loc[test_index]#.drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.dataingestionconfig.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifacts(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e,sys) from e
    
    def initiate_data_ingestion(self):
        try:
            tgz_file_path = self.download_data()
            self.extract_tgz(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e,sys) from e

