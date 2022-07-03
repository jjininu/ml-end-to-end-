from flask import Flask
from diabetic.logger import *
from diabetic.exception import *

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("We are testing custom exception")
        return "CI CD pipeline has been established."
    except Exception as e:
        raise CustomException(e,sys) from e
        


if __name__=="__main__":
    app.run()
