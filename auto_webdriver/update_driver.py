# pip install webdriver-auto-update
from pathlib import Path


from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate

# Target directory to store chromedriver
driver_directory = str(Path.home())

# Create an instance of WebdriverAutoUpdate
driver_manager = WebdriverAutoUpdate(driver_directory)

# Call the main method to manage chromedriver
driver_manager.main()
