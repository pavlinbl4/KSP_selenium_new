# при использовании загрузчика броузера позволяет указать папку, куда будут сохраняться файлы

def enable_download(driver, download_dir):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)