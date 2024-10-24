# -*- coding: utf-8 -*-
"""TransformXfunction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NcHHaqMeLsM0QL6mBfhbSnD0hF5ErMrc
"""

def transformX(df, categorical_columns, categorical_columns_two_options, full_pipeline):
    import pandas as pd
    import numpy as np
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
    from sklearn.compose import ColumnTransformer

    # Identify categorical and numeric columns

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    #print(categorical_columns)
    # Remove 'SeniorCitizen' from numeric columns to passthrough without scaling
    if 'SeniorCitizen' in numeric_columns:
        numeric_columns.remove('SeniorCitizen')

    # # Define preprocessing pipeline for numeric and categorical columns

    # # Numeric pipeline (Imputation + Scaling)
    # numeric_transformer = Pipeline(steps=[
    #     ('imputer', SimpleImputer(strategy='median')),  # Impute missing numeric values
    #     ('scaler', StandardScaler())  # Scale the numeric features
    # ])

    # # Categorical pipeline (Two-option categories: Ordinal Encoding, Other Categorical: OneHotEncoding)
    # categorical_two_opt_transformer = Pipeline(steps=[
    #     ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing categorical (binary)
    #     ('onehot', OrdinalEncoder())  # Ordinal encode binary categories
    # ])

    # categorical_transformer = Pipeline(steps=[
    #     ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing categorical
    #     ('onehot', OneHotEncoder(drop='first'))  # One-hot encode other categorical features
    # ])

    # Combine all the transformers into a ColumnTransformer
    # full_pipeline = ColumnTransformer(transformers=[
    #     ('num', numeric_transformer, numeric_columns),
    #     ('cat_two_opt', categorical_two_opt_transformer, categorical_columns_two_options),
    #     ('cat', categorical_transformer, categorical_columns),
    #     ('passthrough', 'passthrough', ['SeniorCitizen'])  # Pass 'SeniorCitizen' unchanged
    # ])

    # Apply the full pipeline to the data
    df_prepared = full_pipeline.transform(df)
    
    # Get new column names after one-hot encoding
    encoded_categorical_columns = full_pipeline.transformers_[2][1]['onehot'].get_feature_names_out(categorical_columns)

    # Combine numeric, ordinal, and one-hot encoded feature names
    all_columns = numeric_columns + categorical_columns_two_options + list(encoded_categorical_columns) + ['SeniorCitizen']

    # Convert the transformed NumPy array back to a DataFrame
    df_prepared = pd.DataFrame(df_prepared, columns=all_columns)
    #print(numeric_columns)

    return df_prepared