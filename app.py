import nmap
from flask import Flask , render_template,request

network_dic = {'Library':['172.17.63.254','/20'] , 'Hall13':['172.23.157.254','/21'] , 'L20':['172.17.31.254','/21'] , 'Studentlounge':['172.17.23.254','/21'], 'KD':['172.17.47.254','/21']}
class Network(object):
    def __init__(self):
        ip = '127.0.0.1'
        self.ip = ip
        subnet = '/24'
        self.subnet = subnet
    def networkscanner(self):
        network = self.ip + self.subnet
        # network = '172.23.157.254/24'
        print("SCANNNINGGGG ----->>>")
        nm = nmap.PortScanner()
        result = nm.scan(hosts=network ,arguments='-sn')
        print(nm.scanstats())
        x = nm.scanstats()
        return ("The number of host connected to this network is " + x['uphosts'])

app = Flask(__name__)

N = Network()

def nmapf(a):
    N.ip = network_dic[a][0]
    N.subnet = network_dic[a][1]
    return N.networkscanner()

@app.route("/",methods=['GET','POST'])
def main():
    output = 'hosts'
    if(request.method=='POST'):
        Place_request = request.form.get('location')
        output = nmapf(Place_request)
        print(output)
    return render_template('index.html',output1 = output)


app.run(debug=True)