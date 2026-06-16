# Dataset Link:
https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset

The dataset is highly imbalanced, with fraudulent transactions representing a very small fraction of all records. Despite achieving high classification performance, the model may be biased toward fraud patterns primarily observed in TRANSFER and CASH_OUT transaction types.

# Models used Logistic Regression, Random Forest
used in case of binary outputs i.e either fraud or not fraud
Random forest accuracy 99%
logistic Regression accuracy 94%

# RUN COMMAND : 
streamlit run fraud_detection.py
# Install all requirements
pip install -r requirements.txt
