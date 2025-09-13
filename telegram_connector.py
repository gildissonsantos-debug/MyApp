import threading
import asyncio
from queue import Queue, Empty
from telethon import TelegramClient, events

class TelegramConnector:
    """
    Lida com a conexão e chat com o bot no Telegram, usando Telethon e login por SMS.
    """
    def __init__(self, msg_callback, error_callback):
        self.msg_callback = msg_callback
        self.error_callback = error_callback
        self.worker_thread = None
        self.queue = Queue()
        self.client = None
        self.loop = None
        self.bot_username = None
        self.bot_user_id = None
        self._stop_event = threading.Event()
        self._on_code_sent = None
        self._on_sign_in_success = None
        self._on_sign_in_error = None

    def start(self, api_id, api_hash, phone, bot_username, auto=False):
        """
        Login automático usando sessão salva (não reenvia código).
        """
        self.bot_username = bot_username
        self._stop_event.clear()
        self.worker_thread = threading.Thread(
            target=self._worker,
            args=(api_id, api_hash, phone, bot_username),
            daemon=True
        )
        self.worker_thread.start()

    def _worker(self, api_id, api_hash, phone, bot_username):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.client = TelegramClient("session_sms", api_id, api_hash, loop=self.loop)
            self.loop.run_until_complete(self.client.connect())

            @self.client.on(events.NewMessage())
            async def handler(event):
                try:
                    if self.bot_user_id is None:
                        if getattr(event.sender, "username", None):
                            if event.sender.username.lower().lstrip("@") == bot_username.lower().lstrip("@"):
                                self.bot_user_id = event.sender_id
                        if hasattr(event.peer_id, "user_id") and event.is_private:
                            entity = await self.client.get_entity(bot_username)
                            self.bot_user_id = entity.id

                    is_from_bot = False
                    if self.bot_user_id is not None:
                        event_uid = None
                        if hasattr(event, "sender_id") and event.sender_id:
                            event_uid = event.sender_id
                        elif hasattr(event.peer_id, "user_id"):
                            event_uid = event.peer_id.user_id
                        if event_uid == self.bot_user_id:
                            is_from_bot = True

                    user = getattr(event.sender, "username", None)
                    bot_user = bot_username.lstrip("@").lower()
                    if (user and user.lower() == bot_user) or is_from_bot:
                        if self.msg_callback:
                            self.msg_callback(event.message.message)
                except Exception as e:
                    print("Erro no handler:", e)

            async def main_loop():
                while not self._stop_event.is_set():
                    try:
                        cmd, args = self.queue.get(timeout=0.2)
                        if cmd == "send_message":
                            msg = await self.client.send_message(bot_username, *args)
                            if self.bot_user_id is None:
                                entity = await self.client.get_entity(bot_username)
                                self.bot_user_id = entity.id
                    except Empty:
                        await asyncio.sleep(0.1)

            self.loop.create_task(main_loop())
            self.loop.run_until_complete(self.client.run_until_disconnected())
        except Exception as e:
            if self.error_callback:
                self.error_callback(f"Erro ao conectar: {e}")

    def start_phone_login(self, api_id, api_hash, phone, on_code_sent=None, on_error=None):
        """
        Inicia o envio do código de login por SMS/Telegram.
        """
        def worker():
            try:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                self.client = TelegramClient("session_sms", api_id, api_hash, loop=self.loop)
                self.loop.run_until_complete(self.client.connect())
                self.loop.run_until_complete(self.client.send_code_request(phone))
                if on_code_sent:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: on_code_sent(), 0)
            except Exception as e:
                if on_error:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: on_error(f"Erro ao enviar código: {e}"), 0)
        threading.Thread(target=worker, daemon=True).start()

    def sign_in_with_code(self, phone, code, on_success=None, on_error=None):
        """
        Finaliza o login após usuário digitar o código.
        """
        def worker():
            try:
                async def do_sign_in():
                    await self.client.sign_in(phone, code)
                self.loop.run_until_complete(do_sign_in())
                if on_success:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: on_success(), 0)
            except Exception as e:
                if on_error:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: on_error(f"Erro no login: {e}"), 0)
        threading.Thread(target=worker, daemon=True).start()

    def set_bot_username(self, bot_username):
        self.bot_username = bot_username
        self.bot_user_id = None

    def send_message(self, text):
        self.queue.put(("send_message", (text,)))

    def reset(self):
        self._stop_event.set()
        self.client = None
        self.loop = None
        self.worker_thread = None
        self.bot_user_id = None