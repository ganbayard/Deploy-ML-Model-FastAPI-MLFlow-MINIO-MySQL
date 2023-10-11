# from fastapi import FastAPI, Depends, Request
# from models import Price,PricePredictions
# import os
# from sqlalchemy.orm import Session
# from mlflow.sklearn import load_model
# import mlflow
# from database import engine, get_db, create_db_and_tables

# # Tell where is the tracking server and artifact server
# os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001/'
# os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9001/'

# # # Learn, decide and get model from mlflow model registry
# # model_name = "RFElectricityPricePrediction"
# # model_version = 3
# # model = load_model(
# #     model_uri=f"models:/{model_name}/{model_version}"
# # )

# logged_model = 'runs:/5eb79564587a4af5a00f85bc5072a4e4/model'

# # Load model as a PyFuncModel.
# model = mlflow.pyfunc.load_model(logged_model)

# print(model)
# app = FastAPI()
# print(app)
# # Creates all the tables defined in models module
# create_db_and_tables()


# # Note that model will coming from mlflow
# def makePrediction(model, request):
#     # parse input from request
#     Day = request["Day"]
#     Month = request["Month"]
#     ForecastWindProduction = request["ForecastWindProduction"]
#     SystemLoadEA = request["SystemLoadEA"]
#     SMPEA = request["SMPEA"]
#     ORKTemperature = request["ORKTemperature"]
#     ORKWindspeed = request["ORKWindspeed"]
#     CO2Intensity = request["CO2Intensity"]
#     ActualWindProduction = request["ActualWindProduction"]
#     SystemLoadEP2 = request["SystemLoadEP2"]

#     # Make an input vector
#     features = [[Day,
#                  Month,
#                  ForecastWindProduction,
#                  SystemLoadEA,
#                  SMPEA,
#                  ORKTemperature,
#                  ORKWindspeed,
#                  CO2Intensity,
#                  ActualWindProduction,
#                  SystemLoadEP2]]

#     # Predict
#     prediction = model.predict(features)

#     return prediction[0]



# # Insert Prediction information
# def insertPrice(request, prediction, client_ip, db):
#     newPrice = PricePredictions(
#         Day = request["Day"],
#         Month = request["Month"],
#         ForecastWindProduction = request["ForecastWindProduction"],
#         SystemLoadEA = request["SystemLoadEA"],
#         SMPEA = request["SMPEA"],
#         ORKTemperature = request["ORKTemperature"],
#         ORKWindspeed = request["ORKWindspeed"],
#         CO2Intensity = request["CO2Intensity"],
#         ActualWindProduction = request["ActualWindProduction"],
#         SystemLoadEP2 = request['SystemLoadEP2'],
#         prediction=prediction,
#         client_ip=client_ip
#     )

#     with db as session:
#         session.add(newPrice)
#         session.commit()
#         session.refresh(newPrice)

#     return newPrice



# # Electirical Price Prediction endpoint
# @app.post("/prediction/priceprediction")
# async def predictPrice(request: Price, fastapi_req: Request,  db: Session = Depends(get_db)):
#     prediction = makePrediction(model, request.dict())
#     db_insert_record = insertPrice(request=request.dict(), prediction=prediction,
#                                           client_ip=fastapi_req.client.host,
#                                           db=db)
#     return {"prediction": prediction, "db_record": db_insert_record}


from fastapi import FastAPI, Request
import os
from mlflow.sklearn import load_model
import mlflow

app = FastAPI()

# Tell where is the tracking server and artifact server
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5001/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9001/'

logged_model = 'runs:/5eb79564587a4af5a00f85bc5072a4e4/model'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)

@app.post("/prediction/priceprediction")
async def predict_price(request: dict):
    # Parse input from request
    Day = request["Day"]
    Month = request["Month"]
    ForecastWindProduction = request["ForecastWindProduction"]
    SystemLoadEA = request["SystemLoadEA"]
    SMPEA = request["SMPEA"]
    ORKTemperature = request["ORKTemperature"]
    ORKWindspeed = request["ORKWindspeed"]
    CO2Intensity = request["CO2Intensity"]
    ActualWindProduction = request["ActualWindProduction"]
    SystemLoadEP2 = request["SystemLoadEP2"]

    # Make an input vector
    features = [[
        Day, Month, ForecastWindProduction, SystemLoadEA,
        SMPEA, ORKTemperature, ORKWindspeed, CO2Intensity,
        ActualWindProduction, SystemLoadEP2
    ]]

    # Predict
    prediction = model.predict(features)

    return {"prediction": prediction[0]}
