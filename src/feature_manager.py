import pandas as pd
import numpy as np
from scipy.stats import entropy


class FeatureManager:
    @staticmethod
    def get_smallest_category(df):
        df = df.select_dtypes(include=['object', 'category'])

        result = []
        for column in df.columns:
            value_counts = df[column].value_counts(normalize=True)
            value = value_counts.idxmin()
            percent = value_counts.min() * 100

            result.append([column, value, percent])
        return pd.DataFrame(result, columns=['column', 'value', 'frequency(%)']) \
                 .set_index('column') \
                 .sort_values(by='frequency(%)', ascending=True)
    
    @staticmethod
    def get_high_entropy(df, threshold : float = 0.95):
        def calculate_entropy(series):
            value_counts = series.value_counts(normalize=True)
            return entropy(value_counts, base=2)

        threshold = np.log2(df.shape[0]) * threshold
        high_entropy_features = [col for col in df.columns 
                                 if calculate_entropy(df[col]) >= threshold]
        return high_entropy_features
