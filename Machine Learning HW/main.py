import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer

# Load the dataset
data = pd.read_csv('malicious_phish.csv')

# Data Exploration
print("First few rows of the dataset:")
print(data.head())

print("\nSummary statistics of the dataset:")
print(data.describe())

print("\nNumber of missing values in each column:")
print(data.isnull().sum())

print("\nDistribution of the target column:")
print(data['url'].value_counts())

# Data Imputation for Missing Values
imputer = SimpleImputer(strategy='median')
data_imputed = imputer.fit_transform(data)

# Convert Categorical Variables to Numeric (One-Hot Encoding)
data_encoded = pd.get_dummies(pd.DataFrame(data_imputed, columns=data.columns), columns=['type'])

# Feature Scaling (Min-Max Scaling)
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data_encoded)

# Data Splitting
X = data_scaled.drop(columns=['url'])
y = data_scaled['url']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Creation and Training
model = LogisticRegression()
model.fit(X_train, y_train)

# Model Validation and Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))
