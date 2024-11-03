# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# import joblib

# # Load the saved Logistic Regression model
# model_filename = 'gradient_boosting_classifier.joblib'
# lr_model = joblib.load(model_filename)
# print("Model loaded successfully.")

# scaler_filename = 'scaler.joblib'
# scaler = joblib.load(scaler_filename)  # Load the previously saved scaler
# print("Scaler loaded successfully.")

# # Load the real data
# data_path = 'processed_airdrops_data_with_more_scam_labelled.csv'
# real_data = pd.read_csv(data_path, encoding='ISO-8859-1')
# print("Real data loaded successfully.")

# # Assuming that real_data should be processed in the same way as your training data
# # Check if real_data contains the same features, exclude target feature if it exists
# if 'is_scam' in real_data.columns:
#     X_real = real_data.drop(['Title', 'is_scam'], axis=1)
# else:
#     X_real = real_data.drop(['Title'], axis=1)

# # Scale the features using the same scaler as the training set
# # It's important to fit the scaler on the training data and transform both the training and new data with it
# # Since we don't have the original scaler object here, ensure that this matches how you processed the training data
# # scaler = StandardScaler()
# # X_real_scaled = scaler.fit_transform(X_real)  # Ideally, you should save and load the scaler used during training

# # Scale the features using the loaded scaler
# X_real_scaled = scaler.transform(X_real)

# # Make predictions
# real_predictions = lr_model.predict(X_real_scaled)
# real_probabilities = lr_model.predict_proba(X_real_scaled)[:, 1]

# # Add predictions to the data frame if needed
# real_data['Prediction'] = real_predictions
# real_data['Probability'] = real_probabilities.round(2)

# # Save or display the results
# output_path = 'real_data_with_predictions_GBM.csv'
# real_data.to_csv(output_path, index=False)
# print(f"Predictions added and saved to {output_path}.")


import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# # Load the saved Logistic Regression model
lr_model_filename = 'logistic_regression_model.joblib'
lr_model = joblib.load(lr_model_filename)
print("Logistic Regression model loaded successfully.")

# Load the saved Random Forest model
rf_model_filename = 'random_forest_model.joblib'
rf_model = joblib.load(rf_model_filename)
print("Random Forest model loaded successfully.")

# Save the trained gradient boosting model
gbm_model_filename = 'gradient_boosting_model.joblib'
gbm_model= joblib.load(gbm_model_filename)
print("Gradient Boosting Model loaded successfully")

# Load the previously saved scaler
scaler_filename = 'scaler.joblib'
scaler = joblib.load(scaler_filename)
print("Scaler loaded successfully.")

# Load the real data
data_path = 'processed_testing_airdrops_data_labelled.csv'
real_data = pd.read_csv(data_path, encoding='ISO-8859-1')
print("Real data loaded successfully.")

# Assuming that real_data should be processed in the same way as your training data
# Check if real_data contains the same features, exclude target feature if it exists
if 'is_scam' in real_data.columns:
    X_real = real_data.drop(['Title', 'is_scam'], axis=1)
else:
    X_real = real_data.drop(['Title'], axis=1)

# Scale the features using the loaded scaler
X_real_scaled = scaler.transform(X_real)

# Make predictions with Logistic Regression
lr_predictions = lr_model.predict(X_real_scaled)
lr_probabilities = lr_model.predict_proba(X_real_scaled)[:, 1]

# Make predictions with Random Forest
rf_predictions = rf_model.predict(X_real_scaled)
rf_probabilities = rf_model.predict_proba(X_real_scaled)[:, 1]

# Make predictions with Gradient Boosting
gbm_predictions = gbm_model.predict(X_real_scaled)
gbm_probabilities = gbm_model.predict_proba(X_real_scaled)[:, 1]

# # Combine the probabilities (example: average)
# combined_probabilities = (0.4 * lr_probabilities + 0.6 * rf_probabilities)
combined_probabilities = (0.3 * lr_probabilities + 0.4 * rf_probabilities + 0.3 * gbm_probabilities)
# combined_probabilities = (0.5 * lr_probabilities + 0.5 * gbm_probabilities)
# combined_probabilities = (0.5 * gbm_probabilities + 0.5 * rf_probabilities)
combined_predictions = [1 if prob > 0.5 else 0 for prob in combined_probabilities]

# # Add predictions to the data frame
real_data['Combined_Prediction'] = combined_predictions
real_data['Combined_Probability'] = combined_probabilities.round(2)*100

# # Add predictions to the data frame if needed
# real_data['Prediction'] = gbm_predictions
# real_data['Probability'] = gbm_probabilities.round(2)


# Save or display the results
output_path = 'testing_data_with_predictions_lr&rf&gbm.csv'
real_data.to_csv(output_path, index=False)
print(f"Predictions added and saved to {output_path}.")
