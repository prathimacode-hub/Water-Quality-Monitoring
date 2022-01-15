import pandas as pd
import numpy as np
import pickle

def predict_quality(df2, data):
    
    with open('water-model1.pkl', 'rb') as f:
        model = pickle.load(f)

    preds = model.predict(data)
    preds = pd.DataFrame(preds)
    df2['Class'] = preds
    dict = {0:'Needs Treatment', 1:'poor', 2:'good'}
    df2 = df2.replace({"Class": dict})
    return df2