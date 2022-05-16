# this file is for test purpose
import sys
from predict import predict

# constants
MODEL = 'stacking_model'
STATE = int(sys.argv[1])
DISTRICT = int(sys.argv[2])
YEAR = int(sys.argv[3])
SEASON = int(sys.argv[4])
CROP = int(sys.argv[5])
AREA = float(sys.argv[6])


# [[state, district, year, season, crop, area]]
data = [[STATE, DISTRICT, YEAR, SEASON, CROP, AREA]]

result = predict(data, MODEL)

# expected answer : 2000.00 / got : 2030.39
# print('Result / Prediction : ', result)

print(result)
