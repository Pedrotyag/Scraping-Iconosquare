import imaplib
import email
import re

from urllib.parse import urlparse, parse_qs

import pandas as pd

import requests


class email_manager_class():
    def __init__(self, *args, **kwargs):
        
        self.EMAIL_ADRESS = "ptiago1414@gmail.com"
        self.PASSWORD = "bgetzrcqvjcsscds"

    def email_ids_list(self):

        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.EMAIL_ADRESS, self.PASSWORD)
        self.mail.select('inbox')

        result, data = self.mail.search(None, '(FROM "<no-reply@iconosquare.com>" SUBJECT "Your comments export")')
        ids = data[0]
        self.id_list = ids.split()

        if(not self.id_list):
            return False
        
        latest_email_id = int(self.id_list[-1])

        return self.mail, self.id_list

    def list_links(self, mail, id_list):

        print('-'*8 + ' Lendo a caixa de entrada ' + '-'*8 + '\n')
        print(f'Foram encontrados {len(id_list)} emails sobre "iconosquare comments"\n')

        self.links = []

        for i in id_list:

            result, data = mail.fetch(str(i.decode('utf-8')), "(RFC822)")
            raw_email = data[0][1]

            email_message = email.message_from_string(raw_email.decode('utf-8'))

            #print('\n\nFrom: ' + email_message['From'])
            #print('Subject: ' + email_message['Subject'] + '\n')
            #print('Body: ' + str(email_message.get_payload()))

            j = str(email_message.get_payload()[0])    
            
            # initializing substrings
            sub1 = "Download]"
            sub2 = "The Iconosquare team"
            
            # getting index of substrings
            idx1 = str(j).find(sub1)
            idx2 = str(j).find(sub2)
            
            # length of substring 1 is added to
            # get string from next character
            res = str(j)[idx1 + len(sub1) + 1: idx2]
            
            res = res.replace("(", '').replace(")", '').replace("\n", '')

            # printing result
            #print("The extracted string : " + res + '\n')

            self.links.append(res)
        
        print(f'Foram enconrados {len(self.links)} links\n\n')

        return self.links
    
    
    def search_link(self, list_links_in, list_links_comp):

        print('\n' + '-'*8 + ' Verificando se há link novo ' + '-'*8 + '\n')

        self.list_links_out = list(set(list_links_in) - set(list_links_comp))

        if(len(self.list_links_out) > 1 or not self.list_links_out):

            if(not self.list_links_out):
                print("Atenção: Lista Vazia\n")
            else:
                print("Erro: Lista com mais de um EMAIL!!\n")
                raise

            return False
        
        else:

            self.list_links_out = self.list_links_out[0]

            print(f"Foi encontrado um link novo: {self.list_links_out}\n")
            return self.list_links_out
        
    def read_list_comp(self, link, date, subject):

        self.link = link
        self.date = date
        self.subject = subject

        df_list = pd.read_csv('link.csv')

        self.list_comp = df_list['link'].to_list()

    def download_file(self, link_file):
        
        if(type(link_file) == list):
            return False
        
        #Testing if the link is downloadable
        headers=requests.head(link_file).headers
        downloadable = 'attachment' in headers.get('Content-Disposition', '')

        if(not downloadable):
            return False

        # Make http request for remote file data
        data = requests.get(link_file)

        headers=requests.head(link_file).headers
        downloadable = 'attachment' in headers.get('Content-Disposition', '')

        # Define the local filename to save data
    
        d = data.headers['content-disposition']
        self.local_file = re.findall("filename=(.+)", d)[0]

        # Save file data to local copy
        with open(self.local_file, 'wb')as file:
            file.write(data.content)

        return True

    def create_df_excel(self):

        self.df = pd.read_excel(self.local_file, header = 3)

        self.df['subject'] = self.subject
        self.df['post_date'] = self.date
        self.df['post_link'] = self.link
        self.df['report_link'] = self.list_links_out

        self.df.to_csv(''.join([i for i in self.local_file.split('.')][:-1]) + '.csv' )

        print('\n' + '-'*8 + ' Dados novos ' + '-'*8 + '\n')
        print(self.df)

        return self.df
    
    def create_df_csv(self, local_file):

        self.df_csv = pd.read_csv(local_file, sep = ";")

        print('\n' + '-'*8 + ' Seguidores ' + '-'*8 + '\n')
        print(self.df_csv)

        return self.df_csv


# Email_manager = email_manager_class()

# Email_manager.email_ids_list()
# Email_manager.list_links(Email_manager.mail, Email_manager.id_list)

# Email_manager.read_list_comp('https://www.instagram.com/reel/Crt3rxduG74/')


# Email_manager.search_link(Email_manager.links, Email_manager.list_comp)
# Email_manager.download_file(Email_manager.list_links_out)

# Email_manager.create_df()

