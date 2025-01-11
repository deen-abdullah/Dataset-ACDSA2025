import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.datasets import make_classification

def main():
    file_path = 'Dataset/Balanced Gender/balanceGender.csv'  # Set the path to your CSV file

    class_label = 'gender'
    
    # Load data from CSV file
    data = pd.read_csv(file_path)
    feature_columns = ['time','memory','cyclomatic_complexity', 'program_length', 'slocP', 'volume']
    target_column = class_label
    
    # Extract features and target
    X = data[feature_columns]
    y = data[target_column]
    
    # Convert categorical target to numeric values (if necessary)
    y = pd.get_dummies(y, drop_first=True)

    X, y = make_classification(n_samples=2866, n_classes=2, random_state=42)

    # Create a Random Forest Classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    dt_classifier = DecisionTreeClassifier(random_state=42)
    nb_classifier = GaussianNB()
    sm_classifier = SVC(kernel='linear', random_state=42)
    
    # Use 10-fold Stratified Cross-Validation
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    # Evaluate the model using cross-validation
    rf_accuracies = cross_val_score(rf_classifier, X, y, cv=cv, scoring='accuracy')
    dt_accuracies = cross_val_score(dt_classifier, X, y, cv=cv, scoring='accuracy')
    nb_accuracies = cross_val_score(nb_classifier, X, y, cv=cv, scoring='accuracy')
    sm_accuracies = cross_val_score(sm_classifier, X, y, cv=cv, scoring='accuracy')
    
    print(f'RF Accuracy: {rf_accuracies.mean():.4f}')
    print(f'DT Accuracy: {dt_accuracies.mean():.4f}')
    print(f'Bayes Net Accuracy: {nb_accuracies.mean():.4f}')
    print(f'SMO Accuracy: {sm_accuracies.mean():.4f}')
    
if __name__ == '__main__':
    main()