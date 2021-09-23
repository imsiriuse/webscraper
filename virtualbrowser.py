#driver create
#create instance of chrome by proxy
#proxy is IPadress in form n.n.n.n:nnnn
def createChromeMachine(proxy):
    #import libraries
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from fake_useragent import UserAgent
    
    print("opening chrome proxy: " + proxy)
    chrome_options = Options()

    #setting proxy server for chrome
    #chrome_options.add_argument("--proxy-server=" + proxy)
    
    #optimalization settings
    prefs = {'profile.default_content_setting_values': { 'cookies': 2, 'images': 2,'javascript': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2, 'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2,'media_stream': 2, 'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    
    chrome_options.add_experimental_option('prefs', prefs)
    
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    #disable console
    chrome_options.add_argument("--log-level=3")
    
    #to be run as headless (do not open window)
    chrome_options.add_argument("--headless")
    
    #define random user agent from pool
    chrome_options.add_argument("--user-agent=" + UserAgent().random)
    
    #creating instance of chrome browser
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver
