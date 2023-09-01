'''
A module with utility classes to interact with the CX API.
'''
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(category=InsecureRequestWarning)

class AoscxHandler:
    '''
    handler for interacting with CX API.
    '''

    def __init__(self, switch_info:str, login_info:dict[str,str]) -> None:
        self.session = requests.Session()
        self.base_url = f'https://{switch_info}/rest/v10.04/'
        print('logging into the switch...')
        response = self.login(login_info)
        if response.status_code != 200:
            raise ValueError('login failed. Check credentials')
        print('login successful.')

    def login(self, login_info:dict[str,str]) -> requests.Response:
        '''
        wrapper function for logging into a CX device.
        '''
        return self._post('login',login_info)

    def get_ip_bindings(self) -> dict:
        '''
        wrapper function for retrieving IP bindings. Does NOT correspond to ARP table.
        '''
        ip_bindings = self._get('system/ip_bindings')
        data = self._check_response_status_code(ip_bindings)
        return data

    def get_vlan_macs(self, vlan:str) -> dict:
        '''
        wrapper function for retriving MACs in the supplied VLAN.
        '''
        vlan_macs = self._get(f'system/vlans/{vlan}/macs')
        data = self._check_response_status_code(vlan_macs)
        return data

    def get_vlans(self) -> dict:
        '''
        wrapper function for retrieving VLAN information from a CX device.
        '''
        vlans = self._get('system/vlans')
        data = self._check_response_status_code(vlans)
        return data

    def _check_response_status_code(self, resp:requests.Response) -> dict:
        '''
        utility method to check whether an API call was successful. 
        Return the json payload on success.
        '''
        if resp.status_code != 200:
            raise ConnectionError('Failed to call the API endpoint.')
        return resp.json()

    def _post(self, uri:str, data:dict[str, str],
              headers:dict[str,str]='') -> requests.Response:
        '''
        utility method for session post calls that ignores self signed certs
        '''
        if not isinstance(headers,str):
            return self.session.post(f'{self.base_url}{uri}',data, headers=headers, verify=False)
        return self.session.post(f'{self.base_url}{uri}', data, verify=False)
    def _get(self, uri:str, headers:dict[str,str]='') -> requests.Response:
        '''
        utility method for session get calls that ignores self signed certs
        '''
        if not isinstance(headers,str):
            return self.session.get(f'{self.base_url}{uri}', headers=headers, verify=False)
        return self.session.get(f'{self.base_url}{uri}', verify=False)
