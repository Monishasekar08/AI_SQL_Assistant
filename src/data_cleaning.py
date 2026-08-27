import pandas as pd

#load the dataset
df=pd.read_csv("data/Superstore.csv")
print(df.columns)
print("Original data:")
print(df.head())

#checking the missing values
print("\nMissing values:")
print(df.isnull().sum())

#Remove duplicate rows
df=df.drop_duplicates()

#Convert orderdate column to datetime format
#print(df.columns)
#df["OrderDate"]=pd.to_datetime(df["OrderDate"],errors="coerce")

#check data types
print("\nData types:")
print(df.dtypes)

#save cleaned dataset
df.to_csv("data/cleaned_data.csv",index=False)
print("\nData cleaned successfully")
print("cleaned dataset saved as data/cleaned_data.csv")