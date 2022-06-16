# project: p7
# submitter: mhashemineja
# partner: none
# hours: 3

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

class UserPredictor():
    def __init__(self):
        self.xcols=["age","past_purchase_amt","total_time_spent","badge"]
        self.xcols_num=self.xcols[:-1]
        self.xcols_category=[self.xcols[-1]]
        self.xcols_poly=[self.xcols[0]]
        self.index_for_cleaning=0
    
    def fit(self, train_users, train_logs, train_y):
        self.clean(train_users,train_logs)
        self.df["y"]=train_y["y"]
#         print(self.df)
#         print(self.train_logs)
        
        #(PolynomialFeatures(),["past_purchase_amt"])
        combined = make_column_transformer((PolynomialFeatures(),self.xcols_poly),(StandardScaler(),self.xcols_num),(OneHotEncoder(),self.xcols_category))
        model = Pipeline([("transformer", combined),("lr",LogisticRegression()),])
        self.m= model.fit(self.df[self.xcols],self.df["y"])
    
    def predict(self, test_users, test_logs):
        self.clean(test_users,test_logs)
        prediction = self.m.predict(self.df[self.xcols])
        return prediction
        #(LabelEncoder(),["badge"]),
    
    def clean(self, train_users, train_logs):
        self.df=train_users
        self.train_logs = train_logs
        self.df["total_time_spent"]=self.df.apply(lambda user : self.cleaner_time_spent(user),axis=1)
        self.index_for_cleaning=0
        
    def cleaner_time_spent(self,user):
        total_time_spent = 0
        user_id = user["user_id"]
        for seconds in self.train_logs["seconds"][self.index_for_cleaning:]:
            if self.train_logs["url"][self.index_for_cleaning] == "/laptop.html":
                if self.train_logs["user_id"][self.index_for_cleaning] == user_id:
                    total_time_spent += seconds
                    self.index_for_cleaning += 1
                elif self.train_logs["user_id"][self.index_for_cleaning] > user_id:
                    return total_time_spent
                elif user_id not in self.train_logs["user_id"]:
                    return total_time_spent
                else:
                    print("error in cleaner_time_spent")
            else:
                self.index_for_cleaning += 1
        return total_time_spent
        
def main():
    from main import UserPredictor
    
    train_users = pd.read_csv("data/train_users.csv")
    train_logs = pd.read_csv("data/train_logs.csv")
    train_y = pd.read_csv("data/train_y.csv")
    
    model = UserPredictor()
    model.fit(train_users, train_logs, train_y)
    
    test_users = pd.read_csv("data/test1_users.csv")
    test_logs = pd.read_csv("data/test1_logs.csv")
    y_pred = model.predict(test_users, test_logs)

if __name__ == "__main__":
    main()
            
# Credits:
# and labelencoder idea (to to standardize everything)
# https://stackoverflow.com/questions/42204250/how-to-do-onehotencoding-in-sklearn-pipeline