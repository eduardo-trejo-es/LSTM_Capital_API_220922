from unittest import result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import yfinance as yf
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout

from tensorflow.keras.callbacks import EarlyStopping

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.layers.core import Activation

class Model_Trainer:

  def __init__(self):
    pass
  
  def to_train(self,modelPath,DatasetPath,ThepercentageTrainingData):

    ########     Getting the Data      ######
    csvFileName=DatasetPath

    df=pd.read_csv(csvFileName,index_col=0)
    #Separate dates for future plotting
    Data_dates = df.index
    Data_dates=pd.to_datetime(Data_dates,utc=True)
    Data_dates=Data_dates.tz_localize(None)
    
    Columns_N=df.shape[1]
    #Getting the columns name
    cols = list(df)[0:Columns_N]
    print(cols)


    #New dataframe with only training data - 5 columns
    df_for_training = df[cols].astype(float)
    print(type(df_for_training))
    print(df_for_training.shape)


    #####       Scaling and splitting data    #####
    scaler = MinMaxScaler()

    scaler = scaler.fit(df_for_training)
    DS_raw_scaled = scaler.transform(df_for_training)

    #Scaling for OutPuts "Y" colums
    #DS_raw_Open_scaled=DS_raw_scaled[:,[0]]
    #DS_raw_High_scaled=DS_raw_scaled[:,[1]]
    #DS_raw_Low_scaled=DS_raw_scaled[:,[2]]
    DS_raw_Close_scaled=DS_raw_scaled[:,[3]]
    #DS_raw_Volume_scaled=DS_raw_scaled[:,[4]]
    #DS_raw_DayNumber_scaled=DS_raw_scaled[:,[5]]
    #DS_raw_FFT_Mag_Open_10_scaled=DS_raw_scaled[:,[6]]
    #DS_raw_FFT_Angl_Open_10_scaled=DS_raw_scaled[:,[7]]
    #DS_raw_FFT_Mag_Open_50_scaled=DS_raw_scaled[:,[8]]
    #DS_raw_FFT_Angl_Open_50_scaled=DS_raw_scaled[:,[9]]
    #DS_raw_FFT_Mag_Open_100_scaled=DS_raw_scaled[:,[10]]
    #DS_raw_FFT_Angl_Open_100_scaled=DS_raw_scaled[:,[11]]
    #DS_raw_FFT_Mag_High_10_scaled=DS_raw_scaled[:,[12]]
    #DS_raw_FFT_Angl_High_10_scaled=DS_raw_scaled[:,[13]]
    #DS_raw_FFT_Mag_High_50_scaled=DS_raw_scaled[:,[14]]
    #DS_raw_FFT_Angl_High_50_scaled=DS_raw_scaled[:,[15]]
    #DS_raw_FFT_Mag_High_100_scaled=DS_raw_scaled[:,[16]]
    #DS_raw_FFT_Angl_High_100_scaled=DS_raw_scaled[:,[17]]
    #DS_raw_FFT_Mag_Low_10_scaled=DS_raw_scaled[:,[18]]
    #DS_raw_FFT_Angl_Low_10_scaled=DS_raw_scaled[:,[19]]
    #DS_raw_FFT_Mag_Low_50_scaled=DS_raw_scaled[:,[20]]
    #DS_raw_FFT_Angl_Low_50_scaled=DS_raw_scaled[:,[21]]
    #DS_raw_FFT_Mag_Low_100_scaled=DS_raw_scaled[:,[22]]
    #DS_raw_FFT_Angl_Low_100_scaled=DS_raw_scaled[:,[23]]
    #DS_raw_FFT_Mag_Close_10_scaled=DS_raw_scaled[:,[24]]
    #DS_raw_FFT_Angl_Close_10_scaled=DS_raw_scaled[:,[25]]
    #DS_raw_FFT_Mag_Close_50_scaled=DS_raw_scaled[:,[26]]
    #DS_raw_FFT_Angl_Close_50_scaled=DS_raw_scaled[:,[27]]
    #DS_raw_FFT_Mag_Close_100_scaled=DS_raw_scaled[:,[28]]
    #DS_raw_FFT_Angl_Close_100_scaled=DS_raw_scaled[:,[29]]
    #DS_raw_FFT_Mag_Volume_10_scaled=DS_raw_scaled[:,[30]]
    #DS_raw_FFT_Angl_Volume_10_scaled=DS_raw_scaled[:,[31]]
    #DS_raw_FFT_Mag_Volume_50_scaled=DS_raw_scaled[:,[32]]
    #DS_raw_FFT_Angl_Volume_50_scaled=DS_raw_scaled[:,[33]]
    #DS_raw_FFT_Mag_Volume_100_scaled=DS_raw_scaled[:,[34]]
    #DS_raw_FFT_Angl_Volume_100_scaled=DS_raw_scaled[:,[35]]

    
    #Empty lists to be populated using formatted training data
    DS_finished_X = []
    DS_finished_Close_Y = []
    

    n_future = 1   # Number of units(day, min, hour, etc..) we want to look into the future based on the past days.
    n_past =120


    # Creatig the data batches, each one with 30d days

    for i in range(n_past, len(DS_raw_scaled) - n_future +1):
      DS_finished_X.append(DS_raw_scaled[i - n_past:i, 0:DS_raw_scaled.shape[1]])
      DS_finished_Close_Y.append(DS_raw_Close_scaled[i:i+1, 0:DS_raw_scaled.shape[1]])

    DS_finished_X,DS_finished_Close_Y=np.array(DS_finished_X), np.array(DS_finished_Close_Y)
    
    DS_dates_finished_X = []

    ### Creating the data dates batches
    for a in range(n_past, len(Data_dates) - n_future +1):
      DS_dates_finished_X.append(Data_dates[a - n_past:a])
      #DS_dates_finished_X.append(Data_dates[a - n_past:a, 0:Data_dates.shape[1]])
    DS_dates_finished_X = np.array(DS_dates_finished_X)
    DS_dates_finished_X.shape


    #######    Let's split data     #######
    #It's going to be used 70% of data to train and 30% to test the model

    #This Function split dataset with shape (z,x, y) and is splited in z
    def Split3DimData(DataSet,percentageTrainig):
      percentageTrainDataset = 0
      percentageTrainDataset=int((DataSet.shape[0]*percentageTrainig)/100)
      DataSetSplittedTraining=DataSet[0:percentageTrainDataset]
      DataSetSplittedTesting= DataSet[percentageTrainDataset:]

      return DataSetSplittedTraining, DataSetSplittedTesting

    percentageTrainingData= ThepercentageTrainingData
    #####   training data, testing data  ####
    trainX, testingX = Split3DimData(DS_finished_X,percentageTrainingData)
    trainY_Close,testingY_Close=Split3DimData(DS_finished_Close_Y,percentageTrainingData)

    ##Validated data set, im getting the spected result

    print(testingX.shape)
    print(trainX.shape)

    train_Dates, testing_Dates = Split3DimData(Data_dates,percentageTrainingData)

    print(train_Dates.shape)
    print(testing_Dates.shape)


    ##############      Retriving model       ########


    model = keras.models.load_model(modelPath)



    #######          Model Training      ################


    #--------------------------- Assing Y data to losses dictionary -----
    y_data={ 
      "dense": trainY_Close
    }
    testing_y_data={
      "dense": testingY_Close
    }

    #------------------------- Training model --------------------------------
    
    early_stop= EarlyStopping(monitor='val_loss',mode='min',verbose=1,patience=25)
    
    model.fit(x=trainX,y=y_data, epochs=10, batch_size=15, validation_data=(testingX,testing_y_data),callbacks=[early_stop])
    #history = model.fit(trainX,y=y_data, epochs=125, batch_size=15)


    losses = pd.DataFrame(model.history.history)

    losses.plot()

    model.save(modelPath)
    
    
    Training_result="done... ;)"
    
    return Training_result


    #######    Model evaluation      ########
    def Model_evaluation(self):
      from sklearn.metrics import mean_squared_error,mean_absolute_error,explained_variance_score
      import math

      starBatch=1
      endbatch=0

      Batch_to_predict=testingX[testingX.shape[0]-starBatch:testingX.shape[0]-endbatch]

      print(Batch_to_predict.shape)

      print(testingX.shape)


      #########        Evaluation funtion  #########3


      #Mean square error of testing data

      #DataSet unseen before

      #Nota: Se obtuvo un error del 15% aprox. para los 5 features para el dataset no visto y ya visto

      y_data_testing={ 
        "dense": testingY_Open,
        "dense_1": testingY_High,
        "dense_2": testingY_Low,
        "dense_3": testingY_Close,
        "dense_4": testingY_Volume,
      }

      mean_square_error_testin_DS=model.evaluate(testingX,y_data_testing,verbose=0)

      mean_square_error_testing_DS_nparray=np.array(mean_square_error_testin_DS)
      mean_square_error_testing_DS_nparray=mean_square_error_testing_DS_nparray[0:5]
      mean_square_error_testing_DS_nparray_reshaped=np.reshape(mean_square_error_testing_DS_nparray,(1,5))

      #mean_square_error_training_DS_reshaped=np.array(mean_square_error_training_DS)
      testing_DS_scaled_Back = scaler.inverse_transform(mean_square_error_testing_DS_nparray_reshaped)

      for i in testing_DS_scaled_Back[0]:
        print(math.sqrt(i))
        
      y_data_taining_eval={ 
        "dense": trainY_Open,
        "dense_1": trainY_High,
        "dense_2": trainY_Low,
        "dense_3": trainY_Close,
        "dense_4": trainY_Volume,
      }

      #######          Evaluation Using the model      ##############


      N_Days_to_predict=14
      Prediction_Saved=[]
      #testingX=np.array(testingX)

      for i in range(N_Days_to_predict):
        prediction = model.predict(Batch_to_predict) #the input is a 30 units of time batch
        prediction_Reshaped=np.reshape(prediction,(1,1,5))
        Batch_to_predict=np.append(Batch_to_predict,prediction_Reshaped, axis=1)
        Batch_to_predict=np.delete(Batch_to_predict,0,1)
        print(Batch_to_predict.shape)
        Prediction_Saved.append(prediction_Reshaped[0])
        
        
      predict_Open=[]
      predict_High=[]
      predict_Low=[]
      predict_Close=[]
      predict_Volume=[]

      #Splitting data with scaling back
      for i in range(N_Days_to_predict):
        y_pred_future = Prediction_Saved[i]
        predict_Open.append(y_pred_future[0][0])
        predict_High.append(y_pred_future[0][1])
        predict_Low.append(y_pred_future[0][2])
        predict_Close.append(y_pred_future[0][3])
        predict_Volume.append(y_pred_future[0][4])
        
        
      ####      Getting the candle chart   #####

      BatchUsed_Dates=DS_dates_finished_X[len(DS_dates_finished_X)-starBatch:len(DS_dates_finished_X)-endbatch]

      lastTimedate=BatchUsed_Dates[0][BatchUsed_Dates.shape[1]-1:]
      lastTimedate=lastTimedate[0]


      import pandas as pd
      import numpy as np

      BatchForcasted_Dates=[]
      for i in range(0,N_Days_to_predict):
        BatchForcasted_Dates.append(pd.Timestamp(np.datetime64(lastTimedate)))
        lastTimedate=np.datetime64(lastTimedate) + np.timedelta64(1, 'h')


      AllPrediction_DS_scaled_Back=[]
      for i in Prediction_Saved:
        AllPrediction_DS_scaled_Back.append(scaler.inverse_transform(i))
        
        
      predict_Open=[]
      predict_High=[]
      predict_Low=[]
      predict_Close=[]
      predict_Volume=[]

      #Splitting data with scaling back
      for i in range(N_Days_to_predict):
        y_pred_future = AllPrediction_DS_scaled_Back[i]
        predict_Open.append(y_pred_future[0][0])
        predict_High.append(y_pred_future[0][1])
        predict_Low.append(y_pred_future[0][2])
        predict_Close.append(y_pred_future[0][3])
        predict_Volume.append(y_pred_future[0][4])
        
        
      #--------  data shape it's (x days, 6 columns)
      # Convert timestamp to date
      df_forecast = pd.DataFrame({'Open':predict_Open,'High':predict_High, 'Low':predict_Low,'Close':predict_Close,'Volume':predict_Volume}, index=BatchForcasted_Dates)

      df_forecast.index.name="Date"



      import mplfinance as mpf
      title_chart="Twtr"
      mpf.plot(df_forecast, type='candle',title=title_chart, style='charles')