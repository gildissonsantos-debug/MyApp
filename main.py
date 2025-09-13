import re
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivy.core.clipboard import Clipboard
from telegram_connector import TelegramConnector
import json
import os
from datetime import datetime

SESSION_FILE = "session.json"

class TelegramApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connector = TelegramConnector(self.on_receive_message, self.on_critical_error)
        self.dialog = None
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.last_bot_message = ""
        self._pending_api_id = None
        self._pending_api_hash = None
        self._pending_phone = None

    def build(self):
        return Builder.load_file("myapp.kv")

    def on_start(self):
        Clock.schedule_once(lambda dt: self.try_auto_login(), 0.2)

    def try_auto_login(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
            api_id = data.get("api_id")
            api_hash = data.get("api_hash")
            phone = data.get("phone")
            bot_username = data.get("bot_username")
            if api_id and api_hash and phone and bot_username:
                self.connector.start(api_id, api_hash, phone, bot_username, auto=True)
                self.root.current = "chat"
                self.root.ids.bot_label.text = f"Bot: {bot_username}"
                self.root.ids.top_app_bar.title = "Meu Bot"
                return
        self.root.current = "login"

    def save_session(self, api_id, api_hash, phone, bot_username):
        with open(SESSION_FILE, "w") as f:
            json.dump({
                "api_id": api_id,
                "api_hash": api_hash,
                "phone": phone,
                "bot_username": bot_username
            }, f)

    def show_message(self, msg):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(text=msg)
        self.dialog.open()

    def goto_phone_screen(self):
        api_id = self.root.ids.api_id.text.strip()
        api_hash = self.root.ids.api_hash.text.strip()
        if not api_id or not api_hash:
            self.show_message("Preencha API ID e API Hash")
            return
        self._pending_api_id = api_id
        self._pending_api_hash = api_hash
        self.root.current = "phone_screen"

    def send_code(self):
        phone = self.root.ids.phone_input.text.strip()
        if not phone:
            self.show_message("Digite o telefone com DDI, ex: +5511999999999")
            return
        self._pending_phone = phone
        try:
            self.connector.start_phone_login(self._pending_api_id, self._pending_api_hash, phone, on_code_sent=self.on_code_sent, on_error=self.on_critical_error)
            self.show_message("Código enviado! Verifique seu Telegram ou SMS.")
        except Exception as e:
            self.show_message(f"Erro ao enviar código: {e}")

    def on_code_sent(self):
        self.root.current = "code_screen"

    def confirmar_codigo(self):
        code = self.root.ids.code_input.text.strip()
        if not code:
            self.show_message("Digite o código recebido")
            return
        self.connector.sign_in_with_code(self._pending_phone, code, on_success=self.on_login_success, on_error=self.on_critical_error)

    def on_login_success(self):
        self.root.current = "bot_screen"

    def confirmar_bot(self):
        bot_username = self.root.ids.bot_input.text.strip()
        if not bot_username.startswith("@"):
            bot_username = "@" + bot_username
        self.connector.set_bot_username(bot_username)
        self.save_session(self._pending_api_id, self._pending_api_hash, self._pending_phone, bot_username)
        self.root.ids.bot_label.text = f"Bot: {bot_username}"
        self.root.ids.top_app_bar.title = "Meu Bot"
        self.root.current = "chat"

    def send_message(self):
        text = self.root.ids.msg_input.text.strip()
        if not text:
            return
        self.connector.send_message(text)
        self.add_chat_message(text, "user")
        self.root.ids.msg_input.text = ""

    def add_chat_message(self, text, sender, msg_time=None):
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivy.uix.widget import Widget
        from kivy.uix.scrollview import ScrollView
        from kivy.metrics import dp
        from kivy.core.window import Window

        user_color = (0.22, 0.80, 0.65, 1)
        bot_color = (0.15, 0.19, 0.23, 1)
        text_user = (1, 1, 1, 1)
        text_bot = (0.97, 0.97, 0.97, 1)
        align_right = sender == "user"
        max_width = Window.width * 0.5
        min_width = dp(48)

        if not msg_time:
            msg_time = datetime.now().strftime('%H:%M')

        line = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            padding=(dp(4), dp(2), dp(4), dp(2)),
            spacing=0,
            size_hint_y=None,
        )

        if align_right:
            line.add_widget(Widget())

        msg_bg_color = user_color if align_right else bot_color
        msg_text_color = text_user if align_right else text_bot

        msg_box = MDBoxLayout(
            orientation="vertical",
            md_bg_color=msg_bg_color,
            padding=(dp(10), dp(6), dp(10), dp(2)),
            size_hint_x=None,
            adaptive_height=True,
            radius=[16, 16, 6, 16] if align_right else [16, 16, 16, 6],
        )

        if align_right:
            # Linha única, scroll horizontal, fonte menor, alinhado à direita
            scroll = ScrollView(do_scroll_x=True, do_scroll_y=False, bar_width=dp(2), size_hint=(None, None), height=dp(22))
            lbl = MDLabel(
                text=text.replace('\n', ' '),
                theme_text_color="Custom",
                text_color=msg_text_color,
                font_style="Body2",
                font_size="12sp",
                halign="right",
                valign="middle",
                size_hint_x=None,
                size_hint_y=None,
                height=dp(22),
                shorten=False,
                max_lines=1,
            )
            lbl.texture_update()
            label_width = lbl.texture_size[0]
            baloon_width = max(min_width, min(label_width + dp(40), max_width))
            lbl.width = baloon_width - dp(20)
            scroll.width = lbl.width
            msg_box.width = baloon_width
            scroll.add_widget(lbl)
            msg_box.add_widget(scroll)
            # Horário alinhado à direita, menor ainda
            time_label = MDLabel(
                text=msg_time,
                font_size="10sp",
                halign="right",
                valign="middle",
                theme_text_color="Custom",
                text_color=(0.9, 0.9, 0.9, 0.7),
                size_hint_x=None,
                size_hint_y=None,
                height=dp(16),
                width=baloon_width - dp(20),
            )
            msg_box.add_widget(time_label)
        else:
            # Mensagem do bot: pode quebrar linha, fonte normal
            lbl = MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color=msg_text_color,
                font_style="Body2",
                font_size="13sp",
                halign="left",
                valign="middle",
                adaptive_height=True,
                text_size=(max_width - dp(20), None),
                size_hint_y=None,
                shorten=False,
            )
            msg_box.width = max_width
            msg_box.add_widget(lbl)
            # Horário alinhado à esquerda, menor ainda
            time_label = MDLabel(
                text=msg_time,
                font_size="10sp",
                halign="left",
                valign="middle",
                theme_text_color="Custom",
                text_color=(0.9, 0.9, 0.9, 0.7),
                size_hint_x=None,
                size_hint_y=None,
                height=dp(16),
                width=max_width - dp(20),
            )
            msg_box.add_widget(time_label)

        line.add_widget(msg_box)
        if not align_right:
            line.add_widget(Widget())

        self.root.ids.chat_layout.add_widget(line)
        Clock.schedule_once(lambda dt: self.root.ids.scroll_chat.scroll_to(line), 0.1)
        if sender == "bot":
            self.last_bot_message = text

    def copy_last_bot_message(self):
        if self.last_bot_message:
            Clipboard.copy(self.last_bot_message)
            self.show_message("Copiada com sucesso!")
        else:
            self.show_message("Ainda não há resposta para copiar.")

    def on_receive_message(self, text):
        text = re.sub(r"CONSULTASBOT", "MEU BOT", text, flags=re.IGNORECASE)
        now = datetime.now().strftime('%H:%M')
        Clock.schedule_once(lambda dt: self.add_chat_message(text, "bot", now), 0)

    def on_critical_error(self, msg):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.show_message(msg)
        Clock.schedule_once(lambda dt: self.goto_login_screen(), 1.5)

    def goto_login_screen(self):
        self.root.current = "login"
        self.connector.reset()

if __name__ == "__main__":
    TelegramApp().run()