from flask import Flask, send_file, make_response
from datetime import datetime
import os
from collections import defaultdict

app = Flask(__name__)
# Necessary files for file management
root_dir = os.path.dirname(os.path.abspath(__file__))
check_in_dict = defaultdict(list)
# End file vars


@app.route('/<kiosk>', methods=['POST'])
def check_in(kiosk):
    check_in_dict[kiosk].insert(0, datetime.now())
    return make_response(kiosk + " has checked in successfully.", 200)


@app.route('/getlog', methods=['GET'])
def get_log():
    try:
        with open("log.txt", "w") as file:
            file.writelines("Kiosk Log File\nDate of Report: " + str(datetime.now()) + "\n\n")
            for kiosk in check_in_dict:
                file.writelines("Kiosk Name: " + kiosk + "\n")
                if datetime.now().date() == check_in_dict[kiosk][0].date():
                    now_min = sum([datetime.now().time().hour * 60, datetime.now().time().minute])
                    k_min = sum([check_in_dict[kiosk][0].time().hour * 60, check_in_dict[kiosk][0].time().minute])
                    if now_min - k_min > 240:
                        check_in_dict[kiosk].insert(0, False)
                        file.writelines("WARNING: " + kiosk + " has not recently checked in!!\n\n")
                else:
                    check_in_dict[kiosk].insert(0, False)
                    file.writelines("WARNING: " + kiosk + " has not recently checked in!!\n")
                for checkin in check_in_dict[kiosk]:
                    if checkin is False:
                        continue
                    file.writelines("Checked in at: " + checkin.strftime("%Y/%m/%d %H:%M") + "\n")
                file.writelines("\n\n")
        return send_file(str(os.path.join(root_dir, 'log.txt')), attachment_filename='log.txt')
    except Exception as e:
        return str(e), 400


@app.route('/clear', methods=['POST'])
def clear():
    check_in_dict.clear()
    return make_response("Check in dictionary cleared", 200)

# TODO: Write a method to return an html page for status of kiosks
@app.route('/online', methods=['GET'])
def online():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
