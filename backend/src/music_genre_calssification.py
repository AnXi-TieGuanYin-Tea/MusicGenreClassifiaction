#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Christmas 2018

@author: Akihiro Inui
"""

import os
from src.utils.file_utils import FileUtil
from src.classifier.classifier_wrapper import Classifier
from src.common.config_reader import ConfigReader
from src.data_process.data_process import DataProcess
from src.feature_extraction.audio_feature_extraction import AudioFeatureExtraction


class MusicGenreClassification:
    """
    # Content-based music genre classification
    # 1. Frame based feature extraction
    # 2. Data processing (Normalization, Encoding label(string to number))
    # 3. Make data set (Shuffle order, train/test separation, write train.csv/test.csv in "feature" directory with time)
    # 4. Train model / Save model (save trained model in "model" directory with time)
    # 5. Test classifier (test.csv)
    # 6. Make a prediction to a dummy data (dummy_data.csv)
    """

    def __init__(self, audio_feature_extraction: classmethod, classifier: classmethod, dataset_path: str, setting_file: str):
        """
        Init
        :param  audio_feature_extraction: audio feature extraction class
        :param  classifier:               classifier class
        :param  dataset_path:             path to data set
        :param  setting_file:             config file
        """
        self.AFE = audio_feature_extraction(setting_file)
        self.CLF = classifier(setting_file)
        self.dataset_path = dataset_path
        self.cfg = ConfigReader(setting_file)
        self.setting_file = setting_file

    def feature_extraction(self):
        """
        Feature extraction to data set
        :return feature_dataframe:  extracted feature in pandas data frame
        """
        # Extract all features from dataset and store them into dataframe
        return self.AFE.extract_dataset(self.dataset_path, "mean")

    def make_dataset(self, dataframe, output_directory: str):
        """
        Make data set
        :param  dataframe:   extracted feature in data frame
        :param  output_directory: output directory to write out the train and test data
        :return train_data:  train data
        :return train_label: train label
        :return test_data:   test data
        :return test_label:  test label
        """
        # Get time and make a new directory name
        directory_name_with_time = os.path.join(output_directory, FileUtil.get_time())

        train_data, test_data, train_label, test_label = DataProcess.make_dataset(dataframe, self.cfg.label_name,
                                                                                  self.cfg.test_rate, self.cfg.shuffle,
                                                                                  directory_name_with_time)
        return train_data, test_data, train_label, test_label

    def read_dataset(self, input_data_directory_with_date):
        """
        Read data set
        :param  input_data_directory_with_date: name of the directory where train and test data exist
        :return train_data:  train data
        :return train_label: train label
        :return test_data:   test data
        :return test_label:  test label
        """
        # Read data set
        train_data, test_data, train_label, test_label = DataProcess.read_dataset(input_data_directory_with_date,
                                                                                  self.cfg.label_name)

        return train_data, test_data, train_label, test_label

    def data_process(self, dataframe):
        """
        Apply data process to features
        :param  dataframe:            extracted feature in data frame
        :param  label_name:           name of label column in data frame
        :return processed_dataframe:  extracted feature in pandas data frame
        """
        # Make a copy of dataframe
        processed_dataframe = dataframe.copy()
        # Apply normalization to data frame
        processed_dataframe = DataProcess.normalize_dataframe(processed_dataframe, self.cfg.label_name)
        # Factorize label
        processed_dataframe = DataProcess.factorize_lebel(processed_dataframe, self.cfg.label_name)
        return processed_dataframe

    def training(self, train_data, train_label, output_directory):
        """
        Train model and save it under output_directory
        :param  train_data:  train data
        :param  train_label: train label
        :param  output_directory: output directory for model
        :return trained model
        """
        # Train classifier
        model = self.CLF.training(train_data, train_label)

        # Save mode with current time
        self.CLF.save_model(model, os.path.join(output_directory, FileUtil.get_time()))
        return model

    def test(self, model, test_data, test_label) -> float:
        """
        Make predictions to test data set
        :param  model:       trained model
        :param  test_data:   test data
        :param  test_label:  test label
        :return prediction accuracy
        """
        # Make prediction
        return self.CLF.test(model, test_data, test_label)

    def predict(self, model, target_data):
        """
        Make prediction to a given target data and return the prediction result with accuracy for each sample
        :param  model: trained model
        :param  target_data: target data
        :return prediction array with probability
        """
        return self.CLF.predict(model, target_data)


def main():
    # File location
    setting_file = "../../config/master_config.ini"
    music_dataset_path = "../../data"
    model_directory_path = "../../model"
    output_data_directory = "../../feature"
    feature_extraction = False
    training = True
    input_data_directory = "../../feature/2019-01-23_23:19:56.871484"
    model_file = "../../model/2019-01-23_23:19:59.720996/mlp.h5"
    dummy_sample = "../../dummy_data.csv"

    # Instantiate mgc class
    MGC = MusicGenreClassification(AudioFeatureExtraction, Classifier, music_dataset_path, setting_file)

    # Apply feature extraction and write out csv file if it does not exist
    if feature_extraction is True:
        # Apply feature extraction to all audio files
        print("Start feature extraction")
        extracted_feature_dataframe = MGC.feature_extraction()
        # Apply data process
        clean_dataframe = MGC.data_process(extracted_feature_dataframe)
        train_data, test_data, train_label, test_label = MGC.make_dataset(clean_dataframe, output_data_directory)
    else:
        # Read data from directory
        train_data, test_data, train_label, test_label = MGC.read_dataset(input_data_directory)

    if training is True:
        # Training model
        model = MGC.training(train_data, train_label, model_directory_path)
    else:
        # Load model
        model = MGC.CLF.load_model(model_file)

    # Test classifier
    accuracy = MGC.test(model, test_data, test_label)

    # Make prediction
    #dummy_dataframe = FileUtil.csv2dataframe(dummy_sample)
    #prediction_array = MGC.predict(model, dummy_dataframe)
    #max_class = np.argmax(prediction_array)
    #print(prediction_array)
    #print(max_class)

    print("Start prediction")
    print("Final accuracy is {0}".format(accuracy))


if __name__ == "__main__":
    main()