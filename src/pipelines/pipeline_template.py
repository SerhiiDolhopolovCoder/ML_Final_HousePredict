from abc import ABC, abstractmethod
import logging

import pandas as pd

from split_data_type import SplitDataType
from feature_manager import FeatureManager


#реалізація патерну Template Method
class PipelineTemplate(ABC):
    def __init__(self, df, split_data_type: SplitDataType):
        self.__df = df
        self.split_data_type = split_data_type

    def build(self) -> pd.DataFrame:
        df = self.__df.copy()
        df = self._drop_not_needed(df)
        df = self._fill_null(df)
        df = self._preprocess_features(df)
        df = self._encode(df)
        df = self._normalize(df)
        df = self._drop_high_correlation(df)
        return df

    @abstractmethod
    def _drop_not_needed(self, df) -> pd.DataFrame:
        pass
        
    @abstractmethod
    def _fill_null(self, df) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def _preprocess_features(self, df) -> pd.DataFrame:
        pass

    @abstractmethod
    def _encode(self, df) -> pd.DataFrame:
        pass
        
    @abstractmethod
    def _normalize(self, df) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def _drop_high_correlation(self, df) -> pd.DataFrame:
        pass
    
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        allowed_methods = ['_drop_not_needed', '_fill_null', '_encode', 
                           '_preprocess_features', '_normalize', 
                           '_drop_high_correlation']
        if callable(attr) and name in allowed_methods:
            return self.__log(attr)
        return attr
    
    def __log(self, func):
        def wrapper(df, *args, **kwargs):
            result = func(df, *args, **kwargs)
            
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging_message = (
                    f"{self.split_data_type.name} - Function: {func.__name__}\n"
                    f"Size: {result.shape}\n"
                    f"Columns with None: {FeatureManager.get_features_with_none(result)}\n"
                )
                logging.getLogger().debug(logging_message)

            return result
        return wrapper