import os, platform

if(platform.system() == 'Windows'):
    pass
else:
    GOOGLE_CHROME_BIN =  os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH =  os.environ.get('CHROMEDRIVER_PATH')