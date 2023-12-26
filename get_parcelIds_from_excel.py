import pandas as pd
import json

parcelId_json_path = './parcelId.json'
data = pd.read_excel(r"D:\parcelIds03.xlsx")
df = pd.DataFrame(data, columns=['Parcel ID'])
parcelIds = []
df = df.to_json()
jsonData = json.loads(df)
jsonData = jsonData["Parcel ID"]

for x in jsonData:
    parcelIds.append((jsonData[x]))

jsonObject = {
    "parcelIds": parcelIds
}

with open(parcelId_json_path, mode='w') as file:
    json.dump(jsonObject, file, indent = 4)

uniqueParcelIds = []
with open('./tempParcelId.json', mode='r') as file:

    data = json.load(file)
    parcelId_arrays = data["parcelIds"]
    uniqueParcelIds.append(parcelId_arrays[0])
    for o in parcelId_arrays:
        if o != uniqueParcelIds[-1]:
            uniqueParcelIds.append(o)
    file.seek(0)

    data = {
        "parcelIds": uniqueParcelIds
    }

    with open('./tempParcelId.json', mode='w') as file:
        json.dump(data, file, indent = 4)







