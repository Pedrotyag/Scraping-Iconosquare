






def from_to_email(path_to_pdf, subject, message, destination, cco = None):

    """Caso enviado de um email comum essa função substituiria o script "email_inst"
    que envia o email via automação web (a pedido de amom)
    """
    
    EMAIL_ADDRESS = psw.EMAIL_ADDRESS
    EMAIL_PASSWORD = psw.EMAIL_PASSWORD

    with smtplib.SMTP('smtp.gmail.com', 587) as server:

        server.starttls()
        
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        #Craft message (obj)
        msg = MIMEMultipart()

        message = f'{message}'#\n\nSend from Hostname: {gethostname()}'

        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destination

        if(type(cco)==list):
            msg['Bcc'] = ', '.join(cco)
        elif(type(cco) == type(None)):
            pass
        else:
            msg['Bcc'] = cco

        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        # Attach the pdf to the msg going by e-mail
        with open(path_to_pdf, "rb") as f:
            
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(path_to_pdf.split('/')[1]))
        msg.attach(attach)
        # send msg
        server.send_message(msg)



def dados_relatorio(erros, results, hours):
    status = 'OK'

    dados = {'${table1}': df_erros_pages,
         '${table2}': df_quant,
         '${table3}': df_faltantes,
         '${table4}': df_tempos,
         '${table5}': df_hours,
         '${status_processo}':status}
    
    return dados

def editor_doc_relatório(dados, modelo_in = 'auxiliares/MODELO RELATORIO DE PROTOCOLIZACAO.docx', modelo_out = 'Relatório de protocorização de ofícios do buracômetro.docx', width = 250):
    ano = str(datetime.now()).split('-')[0]
    
    document_base = Document(modelo_in)

    document = Document()

    header = document.sections[0].header
    paragraph = header.paragraphs[0]

    logo_run = paragraph.add_run()
    logo_run.text = ' '*50
    logo_run.add_picture('head_relatorio.png', width=Inches(1.0))


    #style
    obj_styles = document.styles
    obj_charstyle = obj_styles.add_style('CommentsStyle', WD_STYLE_TYPE.CHARACTER)
    obj_font = obj_charstyle.font
    obj_font.size = Pt(11)
    obj_font.name = 'Times New Roman'

    for paragraph in document_base.paragraphs:
       
        count = 0

        for i in dados:
            
            if(i in str(paragraph.text) and 'table' in i):
                
                count += 1

                df = dados[i]

                t = document.add_table(df.shape[0]+1, df.shape[1])
                t.style = 'TableGrid'
                
                # add the header rows.
                for j in range(df.shape[-1]):
                    t.cell(0,j).text = df.columns[j]

                # add the rest of the data frame
                for z in range(df.shape[0]):
                    for j in range(df.shape[-1]):
                        t.cell(z+1,j).text = str(df.values[z,j])

                
               
            elif(i in paragraph.text and 'table' not in i):

                count +=1

                paragraph_new = document.add_paragraph()

                paragraph_new.text = paragraph.text.replace(i, dados[i])

            else:
                 
                pass
        
        if(count == 0):

            if("Relatório da protocolização – Buracômetro" in paragraph.text):
                paragraph_new = document.add_paragraph('\t'*3 + paragraph.text)

            else:

                 paragraph_new = document.add_paragraph(paragraph.text)


    document.save(modelo_out)


def relatório_protocolizacao(erros, results, hours):

    dados = dados_relatorio(erros, results, hours)

    editor_doc_relatório(dados, modelo_in = 'auxiliares/MODELO RELATORIO DE PROTOCOLIZACAO.docx', modelo_out = 'Relatório de protocorização de ofícios do buracômetro.docx', width = 250)

    docx_to_pdf("Relatório de protocorização de ofícios do buracômetro.docx")