import pandas as pd
import json

## Reading excel file and saving ParcelIds in parcelId.json
# parcelId_json_path = './parcelId.json'
# data = pd.read_excel(r"D:\parcelIds05.xlsx")
# df = pd.DataFrame(data, columns=['Parcel ID'])
# parcelIds = []
# df = df.to_json()
# jsonData = json.loads(df)
# jsonData = jsonData["Parcel ID"]
#
# for x in jsonData:
#     parcelIds.append((jsonData[x]))
#
# jsonObject = {
#     "parcelIds": parcelIds
# }
#
# with open(parcelId_json_path, mode='w') as file:
#     json.dump(jsonObject, file, indent = 4)

## Cleaning the ParcelIds removing repeated ones in tempParcelId.json
uniqueParcelIds = []
with open('./tempParcelId00.json', mode='r') as file:

    data = json.load(file)
    parcelId_arrays = data["parcelIds"]
    uniqueParcelIds.append(parcelId_arrays[0])
    for o in parcelId_arrays:
        for p in uniqueParcelIds:
            if o != p:
                uniqueParcelIds.append(o)
    file.seek(0)

    data = {
        "parcelIds": uniqueParcelIds
    }

    with open('./tempParcelId.json', mode='w') as file:
        json.dump(data, file, indent = 4)

## Inserting a parcelId into tempParcelId.json making sure no repeats

# isAlreadyPresent = 0
# with open('./tempParcelId00.json', mode='r') as file0:
#     targetData = json.load(file0)
#     targetParcelId_arrays = targetData['parcelIds']
#     with open('./tempParcelId.json', mode='r') as file1:
#         fromData = json.load(file1)
#         fromParcelId_arrays = fromData['parcelIds']
#
#         for o1 in fromParcelId_arrays:
#             for o0 in targetParcelId_arrays:
#                 if o1 == o0:
#                     isAlreadyPresent = 1
#             if isAlreadyPresent == 0:
#                 targetParcelId_arrays.append(o1)
#                 print("Appended---",o1)
#             else:
#                 print("All already exist in the original json ")
#
#         file0.seek(0)
#
#         data = {
#             "parcelIds": targetParcelId_arrays
#         }
#
#         with open('./tempParcelId0.json', mode='w') as file:
#             json.dump(data, file, indent = 4)











