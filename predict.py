import pandas as pd
import numpy as np
import pickle


def salinity(salinity_score):

  '''
  conditions for salinity are based on research
  '''

  if salinity_score >= 1:
    return 'good'
  elif salinity_score < 0:
    return 'poor'
  else :
    return 'Needs Treatment'

# salinity_class = salinity(salinity_score)

def predict_quality(df2, data):
    
    with open('water-model1.pkl', 'rb') as f:
        model = pickle.load(f)

    preds = model.predict(data)
    preds = pd.DataFrame(preds)
    df2['Class'] = 0
    for row in range(df2.shape[0]):
        if salinity(df2.loc[row, 'Salinity']) == 'good':
            if preds.iloc[row, 0] == 2:
                df2.loc[row, 'Class'] = 2
            else :
                df2.loc[row, 'Class'] = preds.iloc[row, 0] 
        elif salinity(df2.loc[row, 'Salinity']) == 'Needs Treatment':
            if preds.iloc[row, 0] == 1:
                df2.loc[row,'Class'] = 1
            else :
                df2.loc[row,'Class'] = 0
        else :
            df2.loc[row,'Class'] = 0
    print('haha')

    # df2['Class'] = preds
    dict = {0:'Needs Treatment', 1:'poor', 2:'good'}
    df2 = df2.replace({"Class": dict})
    return df2