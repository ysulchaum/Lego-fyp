import json

filename = 'brick_voxel'
brickID = '3024'

with open(filename + '.json', 'r') as brick:
    brick_data = json.load(brick)

#dim = (int(brick_data["Dimension"][0]/4), int(brick_data["Dimension"][2]/4), int(brick_data["Dimension"][1]/4 - 1))
brick = brick_data[brickID]

file1 = open(f"{brickID}_line.dat", "w")
L = [f"0 Name: {brickID}.dat\n"]  
file1.writelines(L)
file1.close()

store = '2 16'
for i in range(len(brick)):
    for j in range(i + 1, len(brick)):
        if  (brick[i][0] == brick[j][0] and brick[i][1] == brick[j][1]) or \
            (brick[i][0] == brick[j][0] and brick[i][2] == brick[j][2]) or \
            (brick[i][1] == brick[j][1] and brick[i][2] == brick[j][2]):
            file1 = open(f"{brickID}_line.dat", "a")
            appendd = [f"{store} {brick[i][0]} {brick[i][1]} {brick[i][2]} {brick[j][0]} {brick[j][1]} {brick[j][2]}\n"]
            file1.writelines(appendd)
            file1.close()




print(store)
