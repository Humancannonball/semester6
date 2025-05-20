Regression analysis using a dataset with variuos features. Your objective is to explore the dataset, preprocess it, and apply regression techniques to predict the target variable.

Objectives:

    Explore and preprocess the dataset to prepare it for regression modeling.
    Implement different regression algorithms.
    Evaluate the performance of the regression models using appropriate metrics.

Workflow

    Data Acquisition and Exploration (1 point):
        Obtain the dataset and load it into your environment. Datasets are provided below.
        Manually explore the dataset to understand its structure, features, and descriptive statistics. Identify the target variable and potential predictor variables.
    Data Preprocessing (2 points):
        Handle missing and incorrect values: Identify and address missing and incorrect values using data analysis techniques.
        Encode categorical variables: If present, convert categorical features into numerical representations.
        Feature scaling: Normalize or standardize numerical features to ensure consistency in scale.
        Visualize the distribution of your data. Create plots (such as histograms or boxplots) to see how each variable is distributed. This will help you understand the range, patterns, and potential outliers in your data.
        Visualize a correlation matrix between variables and identify if multicollinearity is present. Why it is important and how it can affect results?
    Regression Modeling (5 points):
        Split the dataset into training and testing sets.
        Implement regression algorithms:
            Linear Regression
            Polynomial Regression
            Decision Trees
            Random Forests
            Recurrent Neural Networks (RNNs) using Keras/TensorFlow
        Train each model on the training set and fine-tune hyperparameters if necessary.
        Evaluate the performance of each model on the testing set using following metrics to assess model‘s fit and accuracy for the task: Mean Absolute Error (MAE), Mean Squared Error (MSE) and R2 score. Organize the scores for each model into a table for comparison.
        Visualize the following plots to better understand how your model is performing:
            Plot predictions versus actual prices.
            Plot residuals distribution (histogram).
            Learning curves (if applicable).
            Include any additional relevant plots that explain the model’s performance or behavior.
    Model Evaluation and Interpretation (2 points):
        Use the evaluation metrics and visualizations to compare how each regression model performed.
        Look for any patterns, trends, or outliers in the results, and try to identify possible reasons behind them. Based on your analysis, explain which model performed the best on your dataset and why.

## Project Structure

- `data/`: Directory to store the dataset (e.g., `housing.csv`).
- `notebooks/` or `scripts/`: Directory for Jupyter notebooks or Python scripts.
  - `data_exploration.ipynb`: Notebook for initial data exploration and understanding.
  - `preprocessing.ipynb`: Notebook/script for data cleaning and preprocessing.
  - `model_training.ipynb`: Notebook/script for training and evaluating regression models.
- `results/`: Directory to save model outputs, plots, and performance metrics.
- `README.md`: This file.
- `requirements.txt`: Python dependencies.

## Setup

1.  **Clone the repository (if applicable) or create the project directory.**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Download the dataset:**
    The dataset used is the California Housing Prices dataset from Kaggle.
    -   Link: [https://www.kaggle.com/datasets/camnugent/california-housing-prices](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
    -   Place the downloaded `housing.csv` file into the `data/` directory.

## Running the Code

1.  **Data Exploration and Preprocessing:**
    *   Open and run the `data_exploration.ipynb` notebook to understand the dataset.
    *   Open and run the `preprocessing.ipynb` notebook/script to clean and prepare the data. This might save a processed dataset.
2.  **Model Training and Evaluation:**
    *   Open and run the `model_training.ipynb` notebook/script. This will:
        *   Load the preprocessed data.
        *   Train the specified regression models (Linear Regression, Polynomial Regression, Decision Trees, Random Forests, RNNs).
        *   Evaluate the models using MAE, MSE, and R2 score.
        *   Generate visualizations (predictions vs. actual, residuals, learning curves).

## Results

*   Performance metrics (MAE, MSE, R2 score) for each model will be displayed in a table.
*   Visualizations will be generated and saved in the `results/` directory, including:
    *   Plots of predictions versus actual values.
    *   Histograms of residuals.
    *   Learning curves (if applicable).
*   A summary of the best performing model and interpretation of the results will be provided in the `model_training.ipynb` notebook or a separate report.

Context

This is the dataset used in the second chapter of Aurélien Géron's recent book 'Hands-On Machine learning with Scikit-Learn and TensorFlow'. It serves as an excellent introduction to implementing machine learning algorithms because it requires rudimentary data cleaning, has an easily understandable list of variables and sits at an optimal size between being to toyish and too cumbersome.

The data contains information from the 1990 California census. So although it may not help you with predicting current housing prices like the Zillow Zestimate dataset, it does provide an accessible introductory dataset for teaching people about the basics of machine learning.
Content

The data pertains to the houses found in a given California district and some summary stats about them based on the 1990 census data. Be warned the data aren't cleaned so there are some preprocessing steps required! The columns are as follows, their names are pretty self explanitory:

longitude

latitude

housing_median_age

total_rooms

total_bedrooms

population

households

median_income

median_house_value

ocean_proximity
