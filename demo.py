from diabetic.pipeline.pipeline import Pipeline
from diabetic.exception import HousingException
from diabetic.logger import logging
from diabetic.config import configuration 


def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()


    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()
