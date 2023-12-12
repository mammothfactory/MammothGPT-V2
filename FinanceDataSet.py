# To create a local clone of the Hugging Face Hub Dataset you can use the following command
# git clone https://huggingface.co/datasets/Mammoth-Factory-Corp/FinanceDataSet
# https://git-lfs.github.com/ is required to clone data down from Hugging Face

#import datasets
from datasets import load_dataset, load_dataset_builder
from datasets.features import Features, Value
from datasets import get_dataset_split_names

from transformers import AutoTokenizer

#from huggingface_hub import Repository TODO REMOVE if not needed

import GlobalConstants as GC


class FinanceDataSet():


    def _info(self):
        """ See https://huggingface.co/docs/datasets/dataset_script
        
        """
        return FinanceDataSet(description="The Sales table of a singular parcel ID from qPublic.net website", features=Features({
            'multiParcel': Value('string'),
            'salePrice': Value('string'),    #TODO Change to interger
            'instrument': Value('string'),
            'bookPage': Value('string'),
            'qualification': Value('string'),
            'vacantOrImproved': Value('string'),
            'saleDate': Value('string'),
            'grantee': Value('string'),
            'grantor': Value('string'),        
        }),
        )


    def load(self, runningTest:bool = False):
        """
        Download to local disk, process and cache the dataset in typed Arrow tables by caching from the Hugging Face Hub located at https://huggingface.co/Mammoth-Factory-Corp
        Arrow table are arbitrarily long, typed tables which can store nested objects and be mapped to numpy/pandas/python generic type
        See https://huggingface.co/docs/datasets/load_hub
        """
        if not runningTest:
            dataset = load_dataset("Mammoth-Factory-Corp/FinanceDataSet", split="train")
        else:
            splits = get_dataset_split_names("Mammoth-Factory-Corp/FinanceDataSet")
            if 'test' in splits:
                dataset = load_dataset("Mammoth-Factory-Corp/FinanceDataSet", split="test")
            else:
                print("You have not split the FinanceDataSet into training and testing sets")
                
        return dataset
        

    def preview(self, dataPointName:str = 'salePrice') -> str:
        """ Load a dataset builder and inspect a dataset’s attributes without committing to downloading it
        
        Args:
            dataPointName (str): The "features" attribute in the DatasetInfo() object to preview 

        Returns:
            Value() object for the match dictionary key passed in by the dataPointName argument; OTHERWISE, a None type if dataPointName doesn't exist
        
        BELOW IS A SAMPLE DatasetInfo() OBJECT 
        DatasetInfo(description='', 
        citation='', 
        homepage='', 
        license='', 
        features={'id': Value(dtype='int64', id=None), 'multiParcel': Value(dtype='string', id=None), 'salePrice': Value(dtype='string', id=None), 'instrument': Value(dtype='string', id=None), 
        'bookPage': Value(dtype='string', id=None), 'qualification': Value(dtype='string', id=None), 'vacantOrImproved': Value(dtype='string', id=None), 'saleDate': Value(dtype='string', id=None), 
        'grantee': Value(dtype='string', id=None), 'grantor': Value(dtype='string', id=None)}, 
        post_processed=None, 
        supervised_keys=None,
        task_templates=None, 
        builder_name='csv', 
        dataset_name='finance_data_set', 
        config_name='default', 
        version=0.0.0, 
        splits={'train': SplitInfo(name='train', num_bytes=395, num_examples=3, shard_lengths=None, dataset_name='finance_data_set')}, 
        download_checksums={'hf://datasets/Mammoth-Factory-Corp/FinanceDataSet@eea4880f87dd1aab01a060292f658978bdd4d168/SalesTable.csv': {'num_bytes': 397, 'checksum': None}}, 
        download_size=397, 
        post_processing_size=None, 
        dataset_size=395, 
        size_in_bytes=792)
        """
        ds_builder = load_dataset_builder("Mammoth-Factory-Corp/FinanceDataSet")
        #data = ds_builder.info.description TODO Why is this always an empty string???
        data = ds_builder.info.features
        
        try:
            valueObject = data[dataPointName] 
        
        except KeyError:
            return None
        
        return valueObject


    def access(self, ds, row:int = None, col:str = None):
        """ Access an entire row or column of data
            https://huggingface.co/docs/datasets/access#indexing
            
        Args:
            row (int): Index of the row to access.
            col (str): Name of the column to access.

        Returns:
            Value associated with the specified row or column.

        Raises:
            ValueError: If both row and col are provided or both are None.
             KeyError, IndexError: If the specified row or column doesn't exist in the data set.
        """
        try:
            if row is None and col is None:
                return None
            elif row is not None and col is not None:
                raise ValueError("Either row OR col must be specified when calling access(), not both please remove one argument'")
            
            result = ds[col] if row is None else ds[row]
            
        except (KeyError, IndexError):
            return None
        
        return result


    def createTokenizer(self):
        """ Use a pretrained BERT model to convert text in FinanceDataSet .csv to numbers 
            https://huggingface.co/bert-base-uncased

        Returns:
            _type_: _description_
        """
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
        return tokenizer
        
        
        
    def upload(self):
        # https://huggingface.co/docs/datasets/upload_dataset
        # dataset.push_to_hub("/home/jupiter/MammothGPT-V2/DatasetConfiguration/ValuationTable.csv")
        pass


if __name__ == "__main__":
    test = FinanceDataSet()
    runTest = False
    ds = test.load(runTest)
    # print(ds)
    # print(ds.features.keys())
    
    printPreview = False
    if printPreview:
        print(test.preview(""))
        print(test.preview("multiParcel"))
        print(test.preview("MultiParcel"))  # Capital "M" should cause this to return NONE
    
    allMultiParcelData = test.access(ds, col='multiParcel')
    print(allMultiParcelData)
    
    allDataPointsForRow2 = test.access(ds, row=2)
    print(allDataPointsForRow2)
    print(allDataPointsForRow2['multiParcel'])
    
    
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  #test.createTokenizer()  # 
    # Tokenizer each column of the FinanceDataSet one at a time
    i = 0
    tokens = {}
    for dataPointName in ds.features.keys(): 
        tokens[i] =  tokenizer(str(test.access(ds, col=dataPointName)))
        i = i + 1
    
    print(tokens)
    dataset = test.map(tokens, batch=True)
    
    print(dataset)
    
    assert allMultiParcelData[2] == allDataPointsForRow2['multiParcel'],  ValueError("Reversing the indexing order caused an error")
    
    tooManyArguments = test.access(ds, row=1, col='salePrice')
    print(tooManyArguments)
    