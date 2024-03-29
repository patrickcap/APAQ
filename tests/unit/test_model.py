import json
import unittest
from unittest import mock
from unittest.mock import Mock

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression  # type: ignore [import-untyped]
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score  # type: ignore [import-untyped]
from sklearn.model_selection import train_test_split  # type: ignore [import-untyped]

from src.model.model import Model


class TestModel(unittest.TestCase):
    FEATURE_COLUMNS = [
        'altitude',
        'runways_count',
        'total_runway_length',
        'total_arrivals',
        'total_departures',
    ]
    TARGET = ['air_quality']

    def setUp(self) -> None:
        self.model = Model()
        self.data_path = 'data/tests/model_test_subset_dataset.json'
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

    @mock.patch('builtins.open')
    @mock.patch('pickle.load')
    def test_loading_wrong_model(self, mock_pickle_load: Mock, mock_open: Mock) -> None:
        # Mocking the behavior of open
        mock_open.return_value.__enter__.return_value = mock.Mock()
        # Mocking the behavior of pickle.load to return an invalid model
        mock_pickle_load.return_value = LinearRegression()

        test_model_class = Model()

        with self.assertRaises(AttributeError):
            test_model_class.load_trained_model('invalid_model.pkl')

    def test_data_preprocessing(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertIsInstance(targets, pd.DataFrame)
        self.assertEqual(features.shape[1], len(self.FEATURE_COLUMNS))
        self.assertEqual(targets.shape[1], len(self.TARGET))
        self.assertEqual(set(features.columns), set(self.FEATURE_COLUMNS))
        self.assertEqual(set(targets.columns), set(self.TARGET))

    def test_fit(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=0)
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        self.assertGreaterEqual(r2, 0.01)
        self.assertLessEqual(rmse, 50)
        self.assertLessEqual(mae, 30)

    def test_predict(self) -> None:
        targets, features = self.model.preprocessing(self.raw_data)
        x_train, x_test, y_train, _ = train_test_split(features, targets, test_size=0.2, random_state=0)
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        self.assertTrue(all(isinstance(y, float) for y in y_pred))

if __name__ == '__main__':
    unittest.main()
