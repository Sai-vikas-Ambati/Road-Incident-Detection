import requests
import json
import openpyxl
import time

workbook = openpyxl.load_workbook("Sept6.xlsx")  # loads the existing .xlsx file
worksheet = workbook.active
worksheet.cell(row=1, column=1, value="normal_traffic")
worksheet.cell(row=1, column=2, value="traffic_delay")
worksheet.cell(row=1, column=3, value="TIME")

def main(i):
    worksheet = workbook.active
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin=17.443736358962692,78.47755695419899&destination=17.444236001504468,78.47097376785939&key=YOUR_API_KEY_HERE&departure_time=now&traffic_model=best_guess'
    get_url = requests.get(url)
    load_text = json.loads(get_url.text)
    a1 = load_text["routes"][0]["legs"][0]["duration"]["value"]
    a2 = load_text["routes"][0]["legs"][0]["duration_in_traffic"]["value"]
    dis = load_text["routes"][0]["legs"][0]["distance"]["value"]
    
    worksheet.cell(row=i, column=1, value=a1)
    worksheet.cell(row=i, column=2, value=a2)
    worksheet.cell(row=i, column=3, value=time.strftime("%H:%M:%S"))
    workbook.save("Sept6.xlsx")

end_time = time.time() + 60 * 60 * 24
i = (worksheet.max_row) + 1
while time.time() <= end_time:
    main(i)
    i += 1
    time.sleep(2 * 60)  # for every 2 minutes
