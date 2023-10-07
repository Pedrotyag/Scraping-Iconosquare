import os, platform

if(platform.system() == 'Windows'):
    EMAIL_ADDRESS = ''
else:
    GOOGLE_CHROME_BIN =  os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH =  os.environ.get('CHROMEDRIVER_PATH')

    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')