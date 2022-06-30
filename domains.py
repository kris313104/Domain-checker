import os
import pprint
import re
import socket
from cProfile import label
from ipaddress import ip_address
from os.path import exists

import whois


def whois_address():
    domains_file_name = "/"+input("enter domains file name from desktop(.txt): ")
    desktop = os.path.expanduser("~/Desktop")

    if(exists(desktop+domains_file_name)):
        print("exists")
        domains = open(desktop+domains_file_name, "r")
        length = len(domains.readlines())
        domains = open(desktop+domains_file_name, "r")
        raport = open(desktop+"/raport.txt", "w")
        for i in range(0, length):
            # print(domains.readline())
            raport.write("=============================================\n")
            
            url_regex = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
            ip_regex = '^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$'
            address = domains.readline().strip()
            
            
            url_match = re.search(url_regex, address)
            id_match = re.search(ip_regex, address)
            if (url_match):
                
                print("valid domain name:"+address)
                w = whois.whois(address)
                from pprint import pprint

                # pprint(w)
                if(w['domain_name'] == None):
                    print("domain does not exist: "+ address)
                    raport.write("domain does not exist: "+ address + "\n")
                    continue
                print("domain name:",w['domain_name'], "\n")
                raport.write("domain name: "+str(w['domain_name']) + "\n")
                raport.write("=============================================\n")
            

                print("owner:",w['registrar'], "\n")
                raport.write("owner: "+str(w['registrar']) + "\n")

                if (isinstance(w['creation_date'], list)):
                    print("creation date:", w['creation_date'][0], "\n")
                    raport.write("creation date: "+ str(w['creation_date'][0]) + "\n")
                else:
                    print("creation date:", w['creation_date'], "\n")  
                    raport.write("creation date: "+ str(w['creation_date']) + "\n")  


                if (isinstance(w['expiration_date'], list)):
                    print("expiration date:", w['expiration_date'][0], "\n")
                    raport.write("expiration date: "+ str(w['expiration_date'][0]) + "\n")
                    
                else:
                    print("expiration date:", w['expiration_date'], "\n")  
                    raport.write("expiration date: "+ str(w['expiration_date']) + "\n")  

                if(isinstance(w['expiration_date'], list)):
                    print("time until expiration:", (w['expiration_date'][0] - w['creation_date'][0]).days, "days", "\n")
                    raport.write("time until expiration: " + str((w['expiration_date'][0] - w['creation_date'][0]).days) + "days" + "\n")
                else:
                    print("time until expiration:", (w['expiration_date'] - w['creation_date']).days, "days", "\n")
                    raport.write("time until expiration: " + str((w['expiration_date'] - w['creation_date']).days) + "days" + "\n")
                print("=============================================\n\n")
                raport.write("=============================================\n\n")
            
            elif(id_match):
                print("give an domain name not ip")
            else:
                print("invalid address: "+address)
        raport.close()
        domains.close()
    else:
        print("file does not exist")
        exit()
        
whois_address()

# Napisz program, który dla podanych nazw domenowych (w pliku tekstowym), sprawdza:
#  właściciela,
#  datę rejestracji,
#  datę wygaśnięcia,
#  oblicza ile pozostało dni do wygaśnięcia od bieżącej daty.
# Dane powinny byd zwrócone w postaci raportu do pliku tekstowego "raport.txt".
