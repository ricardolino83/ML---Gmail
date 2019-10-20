import datetime
import email
import imaplib
import mailbox
import re
import os.path
from os import path

def buscaemail(selectmailbox):
    mail.select(selectmailbox)

    result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i):
        email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', email_uid, '(RFC822)')

        for response_part in email_data:
            # se for a tupla a extraímos o conteúdo
            if isinstance(response_part, tuple):
                # o primeiro elemento da tupla é o cabeçalho
                # de formatação e o segundo elemento possuí o
                # conteúdo que queremos extrair
                message = email.message_from_bytes(response_part[1])

                # com o resultado conseguimos pegar as
                # informações de quem enviou o email e o assunto
                mail_from = message['from']
                mail_to = message['to']
                mail_date = message['date']
                mail_subject = message['subject']

                # agora para o texto do email precisamos de um
                # pouco mais de trabalho pois ele pode vir em texto puro
                # ou em multipart, se for texto puro é só ir para o
                # else e extraí-lo do payload, caso contrário temos que
                # separar o que é anexo e extrair somente o texto
                if message.is_multipart():
                    mail_content = ''
                    # no caso do multipart vem junto com o email
                    # anexos e outras versões do mesmo email em
                    # diferentes formatos como texto imagem e html
                    # para isso vamos andar pelo payload do email
                    for part in message.get_payload():
                        # se o conteúdo for texto text/plain que é o
                        # texto puro nós extraímos
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                if 'devops' in mail_content.lower():
                    file_name = "email_" + str(x) + "-" + str(data[0].split()[x]) + ".txt"
                    if not path.exists(file_name):
                        output_file = open(file_name, 'w')
                        output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(mail_from, mail_to,mail_date, mail_subject, mail_content))
                        output_file.close()

#Caso a caixa seja muito grande pode alterar o numero de linhas
#imaplib._MAXLINE = 1000000
imaplib._MAXLINE = 2000000 

EMAIL_ACCOUNT = "<seuemail>@gmail.com"  # substitua <seuemail> pelo seu email.
PASSWORD = "<suasenha>"  # substitua <suasenha> pela sua senha

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)

code, mailboxes = mail.list()
x = 0
for mailbox in mailboxes:
    for i in mailbox.decode("utf-8"):
        x += 1
        if i == "/":
            teste1 = str(mailbox.decode("utf-8"))
            tamanho = len(teste1)
            xmailbox = teste1[x+2:tamanho]
            if xmailbox != '"[Gmail]"':
                print(xmailbox)
                mail.select(mailbox=xmailbox, readonly=False)
                result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
                i = len(data[0].split())
                print(i)
                buscaemail(xmailbox)
                break
    x = 0

mail.logout()
mail.close