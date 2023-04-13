import bpy
import csv

rooms = bpy.data.collections["Rooms"].all_objects

rooms_data = [["Room name", "Coo1", "Coo2", "Coo3", "Coo4"]]

for room in rooms:
    data = [room.name]
    for v in room.data.vertices:
        data.append(v.co.to_tuple())
    rooms_data.append(data)

output_file = 'C:/Projects/NavigationServer/Data/RoomsMetadata.csv'

with open(output_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for row in rooms_data:
        csv_writer.writerow(row)
