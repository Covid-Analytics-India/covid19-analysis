# from processes import data  # production
#from services.processes import data  # deploy
#file_loc = '.' # production
file_loc = '' # deploy
import pandas as pd
data = pd.read_csv(file_loc + './data/data.csv')
notes_cleaned = data[data["notes"].str.contains("Travelled", na=False)]
v = notes_cleaned[['notes']]
notes_cleaned = notes_cleaned[v.replace(v.stack().value_counts()).gt(5).all(1)]

notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled from Dubai, UAE', 'Travelled from Dubai')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled from London', 'Travelled from UK')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled to Delhi', 'Travelled from Delhi')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled to Delhi', 'Travelled from Delhi')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled from Delhi and Contact history with TN-P5 and TN-P6', 'Travelled from Delhi')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled from Iran, Resident of Ladakh( S.N Medical College ) - Evacuee', 'Travelled from Iran')
notes_cleaned["notes"] = notes_cleaned["notes"].str.replace('Travelled from Iran, Resident of Ladakh( AIIMS ) - Evacuee', 'Travelled from Iran')

notes_cleaned = notes_cleaned.rename(columns={'notes':'Available Information'})
# Rename column name to Available Information
notes_cleaned = notes_cleaned.rename(columns={'notes':'Available Information'})


pie_data = {}
pie_data['travel'] = notes_cleaned['Available Information'].unique()
pie_data = pd.DataFrame.from_dict(pie_data)
pie_data['per'] = 0

Travelled_from_Italy = 0
Travelled_from_Dubai = 0
Travelled_from_MiddleEast = 0
Travelled_from_UK = 0
Travelled_from_SaudiArabia = 0
Travelled_from_Delhi = 0
Travelled_from_IranResidentofLadakhSNMedicalCollegeEvacuee = 0
Travelled_from_IranResidentofLadakhAIIMSEvacuee = 0

for row in notes_cleaned.index:
  if(notes_cleaned['Available Information'][row] == "Travelled from Italy"):
    Travelled_from_Italy += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Dubai"):
    Travelled_from_Dubai += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Middle East"):
    Travelled_from_MiddleEast += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from UK"):
    Travelled_from_UK += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Saudi Arabia"):
    Travelled_from_SaudiArabia += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Delhi"):
    Travelled_from_Delhi += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Iran, Resident of Ladakh( S.N Medical College ) - Evacuee"):
    Travelled_from_IranResidentofLadakhSNMedicalCollegeEvacuee += 1
  elif(notes_cleaned['Available Information'][row] == "Travelled from Iran, Resident of Ladakh( AIIMS ) - Evacuee"):
    Travelled_from_IranResidentofLadakhAIIMSEvacuee += 1

total = notes_cleaned.shape[0]
pie_data['travel'].unique()
pie_data['per'][pie_data['travel'] == ('Travelled from Italy') ] = (Travelled_from_Italy/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Dubai') ] = (Travelled_from_Dubai/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Middle East') ] = (Travelled_from_MiddleEast/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from UK') ] = (Travelled_from_UK/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Delhi') ] = (Travelled_from_Delhi/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Saudi Arabia') ] = (Travelled_from_SaudiArabia/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Iran, Resident of Ladakh( S.N Medical College ) - Evacuee') ] = (Travelled_from_IranResidentofLadakhSNMedicalCollegeEvacuee/total)*100
pie_data['per'][pie_data['travel'] == ('Travelled from Iran, Resident of Ladakh( AIIMS ) - Evacuee') ] = (Travelled_from_IranResidentofLadakhAIIMSEvacuee/total)*100

pie_data_percentage = pd.Series( pie_data['per'] ).tolist(),
pie_data_travel = pd.Series( pie_data['travel'] ).tolist(),
