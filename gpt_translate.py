#encoding:utf-8
import openai
import sys
import configparser
import os

class Setting(object):
    def __init__(self) -> None:
        # 若当前目录无setting.cfg文件则返回报错
        if os.path.exists(os.path.join(os.getcwd(), 'settings.cfg')):
            self.__config_file = os.path.join(os.getcwd(), 'settings.cfg')
        else:
            print('No setting.cfg file.')
            sys.exit(1)
        # 读取配置文件
        self.__config = configparser.ConfigParser()
        self.__config.read(self.__config_file)

    def write_config(self) -> None:
        # 写入修改后的值进配置文件
        with open(self.__config_file, 'w') as config_file:
            self.__config.write(config_file)

    def get_config_apikey(self) -> str:
        return self.__config.get('option', 'openai-apikey')
    
    def set_config_apikey(self, api_key:str) -> None:
        # 修改配置文件的值
        self.__config.set('option','openai-apikey', api_key)
        
    def get_config_language(self) -> str:
        return self.__config.get('option', 'target-language')
    
    def set_config_language(self, target_language:str) -> None:
        self.__config.set('option', 'target-language', target_language)

class Translate(object):
    def __init__(self) -> None:
        self.setting = Setting()
        openai.api_key = self.setting.get_config_apikey()

    def translate_text(self, text:str, target_language:str) -> str:
        self.completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role":"assistant", "content":f"You're a helpful {target_language} translator."},
                {"role":"user", "content":f"{text}"}
            ]
        )

        # 先用utf-8方式编码返回的内容再解码
        translated_text = self.completion.choices[0].message.get('content').encode('utf8').decode()

        return translated_text
    
if __name__ == '__main__':
    translate = Translate()
    setting = Setting()
    key = setting.get_config_apikey()
    print(f'{key}')
    setting.set_config_apikey('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')
    key = setting.get_config_apikey()
    print(f'{key}')

    language = setting.get_config_language()
    print(f'{language}')
    setting.set_config_language("English")

