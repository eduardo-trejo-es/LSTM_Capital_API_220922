import sys
sys.path.append("/Users/eduardo/Desktop/LSTM_Capital_API_220922/FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/Pakages/DataSetgenPacks")

# import all classes
from Retriver_and_Processor_Dataset import DatasetGenerator

dataSet_Gen = DatasetGenerator()

dateStart='2001-01-01'
dateEnd= '2023-03-02'


#######______________ CRUDE_Oil 'CL=F' _____________  ################
itemName='CL=F'

Original_Path_Retiving="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data.csv"
Onlyonecolumn="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_onlyClose.csv"
LastOnetwice="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_LastOneTwice.csv"
DirectionPrice="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_DirePrice.csv"
DayNumAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Dataand_DayNum.csv"
MonthAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_And_month.csv"
yearAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_Data_And_year.csv"
FFTAddedPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/DatasetGen/CRUDE_OIL/CRUDE_OIL_CloseFFT_100.csv"


"""
#dataSet_Gen.RetivingDataPrices_Yahoo(itemName,dateStart, dateEnd,Original_Path_Retiving,Original_Path_Retiving)
dataSet_Gen.UpdateToday(itemName,Original_Path_Retiving)
#columns to pop up
#dataSet_Gen.AddRepeatedLastOne(Original_Path_Retiving, LastOnetwice)

columns=['Open','High','Low','Volume']
#columns=['Open','High','Low']
#columns=['Volume']

dataSet_Gen.PopListdf(columns,Original_Path_Retiving,Onlyonecolumn)
#dataSet_Gen.AddColumnPRCNTG(Original_Path_Retiving,PRCNTGAddedPath)
#if inversed:
#    dataSet_Gen.AddColumnInverseDirePrice(Original_Path_Retiving,DirectionPrice)
#else: 
#    dataSet_Gen.AddColumnDirePrice(Original_Path_Retiving,DirectionPrice)



dataSet_Gen.AddColumnWeekDay(Onlyonecolumn, DayNumAddedPath,False)

dataSet_Gen.AddColumnMothandDay(DayNumAddedPath, MonthAddedPath,False)

dataSet_Gen.AddColumnYear(MonthAddedPath,yearAddedPath)
#
#Generate new FFT columns done :)

"""

#Column=['Open_CL=F','High_CL=F','Low_CL=F','Close_CL=F','Volume_CL=F','Open_HG=F','High_HG=F','Low_HG=F','Close_HG=F','Volume_HG=F','Open_X','High_X','Low_X','Close_X','Volume_X']
#Column=['Open','High','Low','Close']
Column='Close'
frec=[100]
#frec=[10,50,100 
inicialPath=yearAddedPath
FFTNew_FileData=FFTAddedPath
backdaysToconsider=21
firstDone=False
for i in frec:
    if firstDone==True:
        inicialPath=FFTAddedPath
        FFTNew_FileData=FFTAddedPath 
    dataSet_Gen.getTheLastFFTValue(backdaysToconsider,i,Column,inicialPath, FFTNew_FileData)
    firstDone=True