#encoding:UTF-8
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QShortcut, QKeySequence
from gpt_translate import Translate, Setting
from Ui_translate import Ui_MainWindow
import sys
import openai

LANGUAGE_DICT = {
    "中文":"Chinese",
    "English":"English"
}

class Translate_window(QMainWindow, Ui_MainWindow, Translate):
    def __init__(self) -> None:
        # 初始化
        super().__init__()
        self.setting = Setting()
        self.setupUi(self)
        self.setWindowTitle("GPT Translate")
        self.application_translate_init()
        # openai.api_base = "https://api.openai-proxy.com/v1"
        
        # 绑定事件
        # 翻译语言交换
        self.swap_button.clicked.connect(self.swap_translate_language)
        # 翻译按键事件
        self.translate_button.clicked.connect(self.start_translate)
        # 清除翻译原文事件
        self.clean_pushButton.clicked.connect(self.clear_original_text)
        # 设置页面确认和取消事件
        self.setting_confirm_buttonBox.accepted.connect(self.setting_confirm)
        self.setting_confirm_buttonBox.rejected.connect(self.switch_to_translate_page)
        # 设置快捷翻译组合键
        self.translate_shortcut = QShortcut(QKeySequence("Ctrl+T"), self.original_text)
        self.translate_shortcut.activated.connect(self.start_translate)
        # 设置选项事件
        self.setting_toolbar.triggered.connect(self.switch_to_setting_page)
        # API-KEY显示按键
        self.api_key_echo_switch.clicked.connect(self.api_key_show)
        # # 设置API
        # self.api_key_lineEdit.textChanged.connect(lambda:self.setting.set_config_apikey(self.api_key_lineEdit.text()))
        # # 设置GPT模型
        # self.gpt_model_comboBox.textActivated[str].connect(lambda:self.setting.set_config_gpt_model(self.gpt_model_comboBox.currentText()))

    def application_translate_init(self):
        # 初始化翻译目标语言
        language_entry = LANGUAGE_DICT.get(self.target_language_comboBox.currentText())
        self.target_language = language_entry

        # 初始化GPT翻译模型
        self.gpt_model = self.setting.get_config_gpt_model()
        gpt_model_index = self.gpt_model_comboBox.findText(self.gpt_model)
        if gpt_model_index != -1:
            self.gpt_model_comboBox.setCurrentIndex(gpt_model_index)
        else:
            print("init gpt model error.")
        
        # 初始化api-key
        self.api_key_lineEdit.setText(self.setting.get_config_apikey())
        openai.api_key = self.setting.get_config_apikey()

        # 初始化代理
        api_proxy = self.setting.get_config_proxy()
        if len(api_proxy) == 0:
            self.centralwidget.setStatusTip(f"未检测到OpenAI API 代理, 当前使用api地址为: {openai.api_base}")
            self.api_proxy_lineEdit.setText("")
        else:
            self.api_proxy_lineEdit.setText(api_proxy)
            api_proxy = api_proxy + "/v1"
            openai.api_base = api_proxy
            self.centralwidget.setStatusTip(f"正在使用OpenAI API 代理, 代理地址为: {openai.api_base}")

    def api_key_show(self):
        echo_mode = self.api_key_lineEdit.echoMode()
        if echo_mode == self.api_key_lineEdit.EchoMode.Normal:
            self.api_key_lineEdit.setEchoMode(self.api_key_lineEdit.EchoMode.Password)
        else:
            self.api_key_lineEdit.setEchoMode(self.api_key_lineEdit.EchoMode.Normal)
    
    def clear_original_text(self):
        self.original_text.clear()
    
    def start_translate(self):
        text = self.translate_text(self.original_text.toPlainText(),self.target_language,self.gpt_model)
        self.target_text.setPlainText(text)

    def setting_confirm(self):
        self.setting.set_config_gpt_model(self.gpt_model_comboBox.currentText())
        self.setting.set_config_apikey(self.api_key_lineEdit.text())
        self.setting.set_config_proxy(self.api_proxy_lineEdit.text())
        self.setting.write_config()
        self.switch_to_translate_page()
    
    def switch_to_setting_page(self):
        self.application_translate_init()
        self.stackedWidget.setCurrentWidget(self.setting_page)

    def switch_to_translate_page(self):
        self.application_translate_init()
        self.stackedWidget.setCurrentWidget(self.translate_page)

    def swap_translate_language(self):
        # temp_index = self.native_language_comboBox.findText(self.target_language_comboBox.currentText())
        # self.target_language_comboBox.setCurrentIndex(
        #     self.target_language_comboBox.findText(
        #         self.native_language_comboBox.currentText()
        #     )
        # )
        # self.native_language_comboBox.setCurrentIndex(temp_index)

        native_index = self.native_language_comboBox.findText(self.target_language_comboBox.currentText())
        if native_index != -1:
            target_index = self.target_language_comboBox.findText(self.native_language_comboBox.currentText())
            if target_index != -1:
                self.target_language_comboBox.setCurrentIndex(target_index)
                self.native_language_comboBox.setCurrentIndex(native_index)
            else:
                print("无法找到目标语言选项")
        else:
            print("无法找到源语言选项")
        
        self.target_language = LANGUAGE_DICT.get(self.target_language_comboBox.currentText())

        
def main():
    app = QApplication(sys.argv)
    ui = Translate_window()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()