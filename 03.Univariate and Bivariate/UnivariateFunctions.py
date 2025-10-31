import pandas as pd
import warnings
warnings.filterwarnings("ignore")
def getQuanQual(dataset):
    quan = []
    qual = []
    for columnName in dataset.columns:
        # print(columnName)
        if(dataset[columnName].dtype == 'O' ):
            # print("qual")
            qual.append(columnName)
        else:
            if columnName not in ['active', 'smoke','alco','cardio']:
            
            # print("quan")
               quan.append(columnName)
    
    return quan, qual
    
def getProcessedData():   
    # Assiging Dataset

    dataset = pd.read_csv("HeartFailureDataset.csv")
    dataset1= dataset
    # Convert categorical variables in the dataset into dummy (indicator) variables 

    dataset = pd.get_dummies(dataset, drop_first=True)
    
    # Getting the column information of the dataset

#     dataset.info()
    df = dataset
#     print(df)
    

    # Identifying the columns required for processing
    ###### Required Columns     : age,gender,height,weight,ap_hi,ap_lo,cholesterol, gluc,smoke,alco,active, cardio
    ###### Not-Required Column: id

    #Removal of unwanted column(s)
    dataset.drop('id', axis=1, inplace=True)
#     dataset.drop('age', axis=1, inplace=True)
#     dataset.info()

    # Check for Non-Zero cum categorical columns

    dataset.isnull().sum()

    # Replacing columns with 'NaN' values with '0' and itse validation

    dataset.dropna(inplace=True)
    dataset.isnull().sum()

#     print("DATASET:\n",dataset)

    # Displaying first few rows from the header

#     dataset.head()


    # Displaying first few rows before the tail

#     dataset.tail()

    # Remove row duplication if any

    dataset.drop_duplicates()

    # This converts the Gender column into gender_Male, where Male will denoted as '0' and Female will be denoted as '1'


    # Display column names

#     dataset.columns

    # Assigining Independent & Dependent rows
    independent= dataset[['gender_Male', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
           'smoke', 'alco']]
    dependent = dataset[['active' ]]
#     dataset.drop('active', axis=1, inplace=True)

    # Split dataset into train and test sets
    from sklearn.model_selection import train_test_split
    X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(independent, dependent, test_size=0.30, random_state=0)

    return dataset,df,independent,dependent,X_TRAIN, X_TEST, Y_TRAIN, Y_TEST


def getUniVariate(descriptive,quan,dataset):
    for columnName in quan:
        descriptive[columnName]["Mean"]   =dataset[columnName].mean()
        descriptive[columnName]["Median"] =dataset[columnName].median()
        descriptive[columnName]["Mode"]   =dataset[columnName].mode()[0]
        descriptive[columnName]["Q1"]     =dataset.describe()[columnName]["25%"]
        descriptive[columnName]["Q2"]     =dataset.describe()[columnName]["50%"]
        descriptive[columnName]["Q3"]     =dataset.describe()[columnName]["75%"]

        descriptive[columnName]["IQR"]    =descriptive[columnName]["Q3"] - descriptive[columnName]["Q1"]
        descriptive[columnName]["1.5Rule"]=descriptive[columnName]["Q3"] * 1.5    
        descriptive[columnName]["Lesser"] =descriptive[columnName]["Q1"] - descriptive[columnName]["1.5Rule"]
        descriptive[columnName]["Greater"]=descriptive[columnName]["Q3"] + descriptive[columnName]["1.5Rule"]
        descriptive[columnName]["Min"]    =dataset[columnName].min()
        descriptive[columnName]["Max"]    =dataset[columnName].max()
        csum = dataset[columnName].sum()
        descriptive[columnName]["Unique_Values"]     = dataset[columnName].value_counts().index
        descriptive[columnName]["Frequency"]         = dataset[columnName].value_counts().values
        descriptive[columnName]["Relative_Frequency"]= descriptive[columnName]["Frequency"] / csum
        descriptive[columnName]["Cusum"]             = descriptive[columnName].cumsum()

    return descriptive
