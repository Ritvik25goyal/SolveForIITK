# import nmap
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from time import sleep
from flask import Flask , jsonify, render_template,request

'''For mac address analysis  still working in progress'''
# from mac_vendor_lookup import MacLookup , BaseMacLookup
# MacLookup().update_vendors()
# def mac_scan(mac_address):
#     try:
#         print(MacLookup().lookup(mac_address))
#     except:
#         print("unkown")
progress = "the progress"
output = 'Here comes the output. wait for it'
network_dic = {'Library':['172.17.63.254','/20'] , 'Hall13':['172.23.157.254','/21'] , 'L20':['172.17.31.254','/21'] , 'Studentlounge':['172.17.23.254','/21'], 'KD':['172.17.47.254','/21']}

def networkscanner(ip,subnet):
    network = ip + subnet
    print("SCANNNINGGGG ----->>>")
    # nm = nmap.PortScanner()
    # result = nm.scan(hosts=network ,arguments='-sn')
    # '''for printing vendor of each mac address'''
    # # for i in result['scan']:
    # #     if (i=="172.23.157.156"):
    # #         continue
    # #     mac_scan(result['scan'][i]['addresses']['mac'])

    nmap_proc = NmapProcess(targets=network, options="-sn")
    nmap_proc.run_background()
    while nmap_proc.is_running():
        global progress 
        progress = "Progress : "+str(nmap_proc.progress)+"%"
        print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,nmap_proc.progress))
        sleep(10)
    nmap_report = NmapParser.parse(nmap_proc.stdout)
    return ("The number of host connected to this network is " + str(nmap_report.hosts_up))
    


app = Flask(__name__)



def do_scan(a):
    ip = network_dic[a][0]
    subnet = network_dic[a][1]
    return (networkscanner(ip,subnet))

@app.route("/",methods=['GET','POST'])
def main():
    global output
    global progress
    if(request.method=='POST'):
        Place_request = request.form.get('location')
        output = do_scan(Place_request)
        print(output)
    return render_template('index.html',output1 = output,progress_perc=progress)

@app.route('/update_data')
def update_data():
    return render_template('index.html',output1 = output,progress_perc = progress)

app.run()