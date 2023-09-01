import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class AOSCX_HANLDER:

    def __init__(self, switch_info:str, login_info:dict[str,str]) -> None:
        self.session = requests.Session()
        self.BASE_URL = f'https://{switch_info}/rest/v10.04/'
        print('logging into the switch...')
        response = self.login(login_info)
        if response.status_code != 200:
            raise ValueError('login failed. Check credentials')
        else:
            print('login successful.')

    def login(self, login_info:dict[str,str]) -> requests.Response:
        return self._post('login',login_info)

    def get_vlans(self):
        return self._get('system/vlans').json()
    
    def _post(self, uri:str, data:dict[str, str], headers:dict[str,str]={}) -> requests.Response:
        if headers != {}:
            return self.session.post(f'{self.BASE_URL}{uri}',data, headers=headers, verify=False)
        else:
            return self.session.post(f'{self.BASE_URL}{uri}', data, verify=False)
        
    def _get(self, uri:str, headers:dict[str,str]={}) -> requests.Response:
        if headers != {}:
            return self.session.get(f'{self.BASE_URL}{uri}', headers=headers, verify=False)
        else:
            return self.session.get(f'{self.BASE_URL}{uri}', verify=False)