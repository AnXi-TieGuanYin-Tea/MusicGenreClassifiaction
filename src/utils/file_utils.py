#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 02:01:21 2018

@author: Akihiro Inui
"""
import os
import pandas as pd


class FileUtil:


    @staticmethod
    def is_valid_file(input_filename: str) -> bool:
        """
        # Confirm the filename is a valid file
        :param   input_filename: the name of the file to read in.
        :return  True if it is valid file and False if it is invalid file
        """
        return not FileUtil.is_invalid_file(input_filename)

    @staticmethod
    def is_invalid_file(input_filename: str) -> bool:
        """
        # Confirm the filename is a valid file
        :param   input_filename: the name of the file to read in.
        :return  True if it is invalid file and False if it is valid file
        """
        return not os.path.isfile(input_filename)

    @staticmethod
    def is_valid_directory(directory_path: str) -> bool:
        """
        # Check if the directory path is a valid or invalid directory
        :param directory_path:
        :return: True if it is valid directory and False if it is invalid directory
        """
        return not FileUtil.is_invalid_directory(directory_path)

    @staticmethod
    def is_invalid_directory(directory_path: str) -> bool:
        """
        # Check if the directory path is a valid or invalid directory
        :param  directory_path:
        :return: True if it is invalid directory and False if it is valid directory
        """
        return not os.path.isdir(directory_path)

    @staticmethod
    def get_file_length(i_filename):
        """
        Count the number of lines in a file and return that count.
        :type i_filename string
        :param i_filename: the name of the file, which will have its lines counted.
        :rtype integer
        :return: the number of lines in the file.
        """
        i = 0
        with open(i_filename, "r", encoding='utf8') as input_file:
            for i, l in enumerate(input_file):
                pass
        return i + 1

    @staticmethod
    def get_folder_names(directory_path:str) -> list:
        """
        Return list of directories under the given path
        :param directory_path: path to the directory
        :return: list of directories under the given path
        """
        assert FileUtil.is_invalid_directory(directory_path) is False, "Invalid directory path"
        return os.listdir(directory_path)

    @staticmethod
    def excel2dataframe(input_file_path: str):
        """
        # Read excel file into pandas dataframe
        :param  input_file_path: input excel file
        :return pandas data frame
        """
        # Read excel and write out as csv file
        return pd.read_excel(input_file_path, index=False)

    @staticmethod
    def dataframe2csv(input_dataframe, output_filename: str):
        """
        # Write data frame to csv file
        :param  input_dataframe: input pandas data frame
        :param  output_filename: output csv file name
        """
        input_dataframe.to_csv(output_filename, index=False)

    @staticmethod
    def csv2dataframe(input_filename: str):
        """
        # Read csv file to data frame
        :param  input_dataframe: input csv file
        :return : output data frame
        """
        return pd.read_csv(input_filename)