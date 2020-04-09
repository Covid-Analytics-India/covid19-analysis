from services.processes import data # deploy
# from processes import  data # production
grouped = data.groupby( 'Diagnosed date' )['Diagnosed date', 'confirmed'].sum().reset_index()
s = 0
grouped['tot_confirmed'] = grouped['confirmed']
for row in grouped.index:
    grouped['tot_confirmed'][row] += s
    s = grouped['tot_confirmed'][row]

# print(grouped)