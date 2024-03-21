import requests
import json
import urllib3
from bs4 import BeautifulSoup
import sys

urllib3.disable_warnings()

class ctbb_subs:
    def __init__(self, t_name, outfile):
        self.api_url_all = f"https://huntdash.xyz/api/targets/"
        self.sub_api = f"https://huntdash.xyz/targets/"
        self.api_key = ""
        self.headers = {"X-Critical-Thinker": f"{self.api_key}"}
        self.t_name = t_name
        self.status = None
        self.stats = []
        self.outfile = outfile

    def target_check(self):
        try:
            # checking if the target exists
            res = requests.get(self.api_url_all, headers=self.headers, verify=False, timeout=10)
            if res and res.status_code == 200:
                all_jparse = json.loads(res.text)
                for key in all_jparse['targets']:
                    if self.t_name == key['name']:
                        self.status = True
                    else:
                        self.status = False
        except Exception as err:
            print(f"[-] Something went wrong {err}")
    def fetch_subs(self):
        full_url = self.sub_api+self.t_name+"/subdomains/"
        try:
            res = requests.get(full_url, headers=self.headers, verify=False, timeout=10)
            if res and res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                card_headers = soup.find_all('div', class_='card-header')
                for i in card_headers:
                    print(i.a.text)
                    self.stats.append(i.a.text)


            else:
                print("[-] Service down... Maybe!")
        except Exception as err:
            print(f"[-] Something went wrong {err}")


    def results(self):
        self.target_check()
        if self.status:
            print(f"[+] {self.t_name} was found on the database...")
            self.fetch_subs()
            with open(self.outfile, 'a') as file:
                for sub in self.stats:
                    file.write("\n"+sub)
            file.close()
            print(f"\n{len(self.stats)} subdomains were found")
        else:
            print(f"[-] Unfortunately {self.t_name} was not found on the database...")

def usage():
    if len(sys.argv) < 3:
        print("""
        Usage: python ctbb_subs.py <target_name> <output_file>
        
        Note: Hunterdash.xyz works based on target name not domain name
              So u should grab the program name from the url for instance
              https://hackerone.com/zomato the target name is zomato
              it doesn't have to be on Hackerone, it can be on other platforms :)
        """)
        sys.exit(0)
try:
    script, target_name, output = sys.argv
except Exception as err:
    usage()

def main(target, file):
    ref = ctbb_subs(target, file)
    ref.results()

main(target_name, output)

