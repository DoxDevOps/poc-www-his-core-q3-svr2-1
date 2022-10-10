import requests
import json
import platform
import subprocess
import os
from fabric import Connection
from dotenv import load_dotenv
load_dotenv()
#from dotenv import dotenv_values
#config = dotenv_values(".env")
#API_KEY = os.getenv('API_KEY')

""" 
* Gets data from Xi API
* @param url
* returns json
"""
def get_xi_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data[0]['fields']
    return data


def alert(url, params):
    """sends sms alert"""
    try:
        headers = {'Content-type': 'application/json; charset=utf-8'}
        r = requests.post(url, json=params, headers=headers)
        print("SMS sent successfully")
        
    except Exception as e:
        print("Failed to send SMS with exception: ", e)
        return False
    return True

recipients = ["+265998006237", "+265991450316","+265992182669", "+265995246144", "+265998276712", "+265999600511", "+265992277183","+265995532195","+265991239213"]
#* Get cluster details
cluster = get_xi_data('http://10.44.0.52:8000/sites/api/v1/get_single_cluster/43')

for site_id in cluster['site']:
    site = get_xi_data('http://10.44.0.52:8000/sites/api/v1/get_single_site/' + str(site_id))

    # functionality for ping re-tries
    count = 0

    while(count < 3):

        #* lets check if the site is available
        param = '-n' if platform.system().lower()=='windows' else '-c'
        if subprocess.call(['ping', param, '1', site['ip_address']]) == 0:
            
            # shipping backup script
            #push_backup_script = "rsync " + "-r $WORKSPACE/devops_core_backup.sh " + site['username'] + "@" + site['ip_address'] + ":/var/www"
            #os.system(push_backup_script)
            
            # backing up application folder [Core & ART]
            #backup_script = "ssh " + site['username'] + "@" + site['ip_address'] + " 'cd /var/www && chmod 777 devops_core_backup.sh && ./devops_core_backup.sh'"
            #os.system(backup_script)
            
            #* ship core to remote site
            push_core = "rsync " + "-r $WORKSPACE/HIS-Core " + site['username'] + "@" + site['ip_address'] + ":/var/www"
            os.system(push_core)
            
            #* ship core setup script to remote site
            push_core_script = "rsync " + "-r $WORKSPACE/core_setup.sh " + site['username'] + "@" + site['ip_address'] + ":/var/www/HIS-Core"
            os.system(push_core_script)
            
            # run setup script
            run_core_script = "ssh " + site['username'] + "@" + site['ip_address'] + " 'cd /var/www/HIS-Core && ./core_setup.sh'"
            os.system(run_core_script)

            result = Connection("" + site['username'] + "@" + site['ip_address'] + "").run('cd /var/www/HIS-Core && git describe', hide=True)
            
            msg = "{0.stdout}"
            
            version = msg.format(result).strip()
            
            core_version = "v1.4.2"
            
            if core_version == version:
                msgx = "Hi there,\n\nDeployment of HIS-Core to " + version + " for " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF/LIN HIS."
            else:
                msgx = "Hi there,\n\nSomething went wrong while checking out to the latest HIS-Core version. Current version is " + version + " for " + site['name'] + ".\n\nThanks!\nEGPAF/LIN HIS."

            # send sms alert
            for recipient in recipients:
                msg = "Hi there,\n\nDeployment of HIS-Core to " + version + " for " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF/LIN HIS."
                params = {
                    "api_key": os.getenv('API_KEY'),
                    "recipient": recipient,
                    "message": msgx
                }
                alert("http://sms-api.hismalawi.org/v1/sms/send", params)

            # close the while loop
            count = 3

        else:
            # increment the count
            count = count + 1

            # make sure we are sending the alert at the last pint attempt
            if count == 3:
                for recipient in recipients:
                    msg = "Hi there,\n\nDeployment of HIS-Core to v1.4.2 for " + site['name'] + " failed to complete after several connection attempts.\n\nThanks!\nEGPAF/LIN HIS."
                    params = {
                        "api_key": os.getenv('API_KEY'),
                        "recipient": recipient,
                        "message": msg
                    }
                    alert("http://sms-api.hismalawi.org/v1/sms/send", params)
