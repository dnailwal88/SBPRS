import pickle
import numpy as np
import pandas as pd

def get_top5(username):
    with open("data/dfSentiment.pk",'rb') as f:
        dfSentiment=pickle.load(f)
    with open("models/user_final_rating.pk",'rb') as f:
        user_final_rating=pickle.load(f)
    with open("models/tfidf_vectorizer.pk",'rb') as f:
        tfidf=pickle.load(f)
    with open("models/rfc_model.pk",'rb') as f:
        rfc=pickle.load(f)
    if username in user_final_rating.index:
        recommendations=list(user_final_rating.loc[username].sort_values(ascending=False)[0:20].index)
        dfTemp=dfSentiment[dfSentiment.id.isin(recommendations)]
        X=tfidf.transform(dfTemp["reviews_processed"])
        dfTemp['user_sentiment_pred']=rfc.predict(X)
        dfTempG=dfTemp.groupby(['id','name']).agg({'user_sentiment_pred':['count','sum']})
        dfTempG.columns=['total_count','pos_count']
        dfTempG.reset_index(inplace=True)
        dfTempG['pos_per']=dfTempG['pos_count']/dfTempG['total_count']
        print(dfTempG.sort_values('pos_per',ascending=False)[:5])
        top5_list=dfTempG.sort_values('pos_per',ascending=False)[:5].name.tolist()
        return top5_list
    else:
        return []