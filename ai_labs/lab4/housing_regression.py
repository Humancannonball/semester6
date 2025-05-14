import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os
import warnings
warnings.filterwarnings('ignore')

# Create results directory if it doesn't exist
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

# 1. Data Acquisition and Exploration
print("1. Data Acquisition and Exploration")
# Load the dataset
data = pd.read_csv('housing.csv')

# Display basic information
print("\nDataset Shape:", data.shape)
print("\nFirst 5 rows:")
print(data.head())
print("\nDataset Info:")
print(data.info())
print("\nStatistical Summary:")
print(data.describe())

# Check for missing values
print("\nMissing Values Count:")
print(data.isnull().sum())

# Identify target variable
target = 'median_house_value'
X = data.drop(target, axis=1)
y = data[target]

# 2. Data Preprocessing
print("\n2. Data Preprocessing")

# Handle missing values
print("\nHandling missing values...")
X_numeric = X.select_dtypes(include=[np.number])
numeric_features = X_numeric.columns
categorical_features = ['ocean_proximity']

# Create a column transformer for preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ])

# Visualize data distributions
plt.figure(figsize=(15, 10))
for i, feature in enumerate(numeric_features):
    plt.subplot(3, 3, i+1)
    sns.histplot(X[feature], kde=True)
    plt.title(f'Distribution of {feature}')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'feature_distributions.png'))
plt.close()

# Visualize correlation matrix
plt.figure(figsize=(12, 8))
correlation_matrix = X_numeric.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'correlation_matrix.png'))
plt.close()
print("\nMulticollinearity Analysis: Created correlation matrix visualization. High correlation between features like 'total_rooms', 'total_bedrooms', 'households', and 'population' indicates multicollinearity, which can inflate variance of coefficient estimates and make models less stable.")

# 3. Regression Modeling
print("\n3. Regression Modeling")

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Dictionary to store model results
model_results = {}

# Function to evaluate models
def evaluate_model(model, model_name, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    model_results[model_name] = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'Predictions': y_pred
    }
    
    print(f"{model_name} - MAE: {mae:.2f}, MSE: {mse:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}")
    
    # Plot predictions vs actual
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title(f'{model_name}: Predictions vs Actual')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f'{model_name.lower().replace(" ", "_")}_predictions.png'))
    plt.close()
    
    # Plot residuals
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title(f'{model_name}: Residuals Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f'{model_name.lower().replace(" ", "_")}_residuals.png'))
    plt.close()
    
    # Plot learning curve for sklearn models (excluding RNN)
    if model_name != 'RNN':
        train_sizes, train_scores, test_scores = learning_curve(
            model, X_train, y_train, cv=5, scoring='r2', 
            train_sizes=np.linspace(0.1, 1.0, 5))  # Reduced number of points from 10 to 5
        
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        test_mean = np.mean(test_scores, axis=1)
        test_std = np.std(test_scores, axis=1)
        
        plt.figure(figsize=(10, 6))
        plt.plot(train_sizes, train_mean, label='Training score')
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
        plt.plot(train_sizes, test_mean, label='Validation score')
        plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1)
        plt.xlabel('Training Set Size')
        plt.ylabel('R² Score')
        plt.title(f'{model_name}: Learning Curve')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, f'{model_name.lower().replace(" ", "_")}_learning_curve.png'))
        plt.close()

# Prepare and evaluate models
print("\nTraining and evaluating models...")
models = {
    'Linear Regression': Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ]),
    'Polynomial Regression': Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('poly_features', PolynomialFeatures(degree=2)),
        ('regressor', LinearRegression())
    ]),
    'Decision Tree': Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', DecisionTreeRegressor(random_state=42))
    ]),
    'Random Forest': Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
}

# Train and evaluate sklearn models
for name, model in models.items():
    evaluate_model(model, name, X_train, X_test, y_train, y_test)

# RNN model
print("\nTraining RNN model...")
# Process data for RNN
X_rnn = preprocessor.fit_transform(X_train)
X_test_rnn = preprocessor.transform(X_test)

# Reshape data for RNN input [samples, time steps, features]
X_rnn_reshaped = X_rnn.reshape((X_rnn.shape[0], 1, X_rnn.shape[1]))
X_test_rnn_reshaped = X_test_rnn.reshape((X_test_rnn.shape[0], 1, X_test_rnn.shape[1]))

# Build RNN model
rnn_model = Sequential([
    LSTM(50, activation='relu', input_shape=(1, X_rnn.shape[1])),
    Dropout(0.2),
    Dense(1)
])

rnn_model.compile(optimizer='adam', loss='mse')

# Train RNN model
history = rnn_model.fit(
    X_rnn_reshaped, 
    y_train, 
    epochs=30,  # Reduced from 50 to 30
    batch_size=32,
    validation_split=0.2,
    verbose=0
)

# Evaluate RNN model
y_pred_rnn = rnn_model.predict(X_test_rnn_reshaped).flatten()
mae_rnn = mean_absolute_error(y_test, y_pred_rnn)
mse_rnn = mean_squared_error(y_test, y_pred_rnn)
rmse_rnn = np.sqrt(mse_rnn)
r2_rnn = r2_score(y_test, y_pred_rnn)

model_results['RNN'] = {
    'MAE': mae_rnn,
    'MSE': mse_rnn,
    'RMSE': rmse_rnn,
    'R2': r2_rnn,
    'Predictions': y_pred_rnn
}

print(f"RNN - MAE: {mae_rnn:.2f}, MSE: {mse_rnn:.2f}, RMSE: {rmse_rnn:.2f}, R2: {r2_rnn:.4f}")

# Plot RNN predictions vs actual
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rnn, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('RNN: Predictions vs Actual')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'rnn_predictions.png'))
plt.close()

# Plot RNN residuals
residuals = y_test - y_pred_rnn
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('RNN: Residuals Distribution')
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'rnn_residuals.png'))
plt.close()

# Plot RNN learning curve
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.title('RNN: Learning Curve')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'rnn_learning_curve.png'))
plt.close()

# 4. Model Evaluation and Interpretation
print("\n4. Model Evaluation and Interpretation")

# Create comparison table
results_df = pd.DataFrame({
    model_name: {
        'MAE': results['MAE'],
        'MSE': results['MSE'],
        'RMSE': results['RMSE'],
        'R2': results['R2']
    } for model_name, results in model_results.items()
})

# Save model comparison results to CSV
results_df.T.to_csv(os.path.join(results_dir, 'model_comparison.csv'))

print("\nModel Comparison:")
print(results_df.T)

# Find best model based on R2
best_model = results_df.T['R2'].idxmax()
print(f"\nBest performing model based on R2 score: {best_model}")

# Plot comparison of model performance
plt.figure(figsize=(12, 8))
sns.barplot(x=results_df.T.index, y=results_df.T['R2'])
plt.title('R² Score Comparison')
plt.ylabel('R² Score')
plt.xlabel('Model')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'model_comparison_r2.png'))
plt.close()

plt.figure(figsize=(12, 8))
sns.barplot(x=results_df.T.index, y=results_df.T['RMSE'])
plt.title('RMSE Comparison')
plt.ylabel('RMSE')
plt.xlabel('Model')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(results_dir, 'model_comparison_rmse.png'))
plt.close()

print(f"\nAnalysis completed. All visualizations have been saved in the '{results_dir}' folder.")
