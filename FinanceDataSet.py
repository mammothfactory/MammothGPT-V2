# To create a local clone of the Hugging Face Hub Dataset you can use the following command
# git clone https://huggingface.co/datasets/Mammoth-Factory-Corp/FinanceDataSet
# https://git-lfs.github.com/ is required to clone data down from Hugging Face

from datasets import load_dataset
from huggingface_hub import Repository

import GlobalConstants as GC


class FinanceDataSet():

    def _info(self):
        """
        https://huggingface.co/docs/datasets/dataset_script
        
        """
        pass


    def load():
        """
        Process and cache the dataset in typed Arrow tables for caching from the Hugging Face Hub located at https://huggingface.co/Mammoth-Factory-Corp
        Arrow table are arbitrarily long, typed tables which can store nested objects and be mapped to numpy/pandas/python generic type
        See https://huggingface.co/docs/datasets/load_hub
        """
        dataset = load_dataset("Mammoth-Factory-Corp/FinanceDataSet")


    def upload():
        # https://huggingface.co/docs/datasets/upload_dataset
        pass
        dataset.push_to_hub("/home/jupiter/MammothGPT-V2/DatasetConfiguration/ValuationTable.csv")
