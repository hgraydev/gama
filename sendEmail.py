import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self, receiver, filename):
        self.subject = "Notificacion General de Rastreo de Eventos"
        self.body = "Rastreo de Eventos en COMPRANET"
        self.sender_email = "iscodigo.soporte@gmail.com"
        self.receiver_email = receiver
        self.password = "53d3rd3v3l0p3r._"
        self.filename = filename
        self.config()
        self.openFile();
        self.send();
    
    def config(self):
        # Create a multipart message and set headers
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        self.message["Subject"] = self.subject
        self.message["Bcc"] = self.receiver_email  # Recommended for mass emails
        self.message.attach(MIMEText(self.body, "plain"))

    def openFile(self):
        # Open PDF file in binary mode
        with open(self.filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.filename}",
        )
        self.message.attach(part)
        self.text = self.message.as_string()
        self.context = ssl.create_default_context()

    def send(self):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.text)
