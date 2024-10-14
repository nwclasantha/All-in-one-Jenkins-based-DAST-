#!/usr/bin/env python3
import os
import sys
import re
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# Configure logging
logging.basicConfig(
    filename='email_sender.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Main class for sending emails
class MailSender:
    def __init__(self, smtp_host, smtp_port, mail_uname, mail_pwd, from_email, recipients_mail_list):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.mail_uname = mail_uname
        self.mail_pwd = mail_pwd
        self.from_email = from_email
        self.recipients_mail_list = recipients_mail_list
        logging.info("Initialized MailSender.")

    def send_email(self, mail_subject, mail_content_html, attachment_fpaths):
        logging.info(f"Preparing to send email with subject: {mail_subject}")
        
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ','.join(self.recipients_mail_list)
        msg['Subject'] = mail_subject
        msg.attach(MIMEText(mail_content_html, 'html'))

        for path in attachment_fpaths:
            try:
                with open(path, "rb") as f:
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
                msg.attach(part)
                logging.info(f"Attached file: {path}")
            except FileNotFoundError as e:
                logging.error(f"File not found: {path}. Error: {str(e)}")
                raise

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                logging.info(f"Connecting to SMTP server: {self.smtp_host}:{self.smtp_port}")
                server.login(self.mail_uname, self.mail_pwd)
                server.sendmail(self.from_email, self.recipients_mail_list, msg.as_string())
                logging.info("Email sent successfully.")
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred: {str(e)}")
            raise Exception(f"Error occurred while sending email: {str(e)}")


# Subclass for handling pipeline-related email sending logic
class PipelineMailSender(MailSender):
    def __init__(self, smtp_host, smtp_port, mail_uname, mail_pwd, from_email, recipients_mail_list, pipeline_type):
        super().__init__(smtp_host, smtp_port, mail_uname, mail_pwd, from_email, recipients_mail_list)
        self.pipeline_type = pipeline_type
        logging.info("Initialized PipelineMailSender.")

    def get_mail_content(self):
        logging.info(f"Fetching email content for pipeline type: {self.pipeline_type}")
        
        content_map = {
            "SAST": {
                "subject": "The SAST Assessments Reports",
                "attachments": ["SAST_Reports.zip"],
                "html": ''' Dear Team, <br/><br/> This is the <b>SAST Risk Assessments Reports</b> against GitLab<br/>
                            <br/><b>The Types of Security Scanning have been processed as follows:</b><br/>
                            1. Credential Scanning<br/>
                            2. Open-source Libraries (OSS) Scanning<br/>
                            3. Known Vulnerabilities according to CVSS 3.x<br/>
                            4. Shell/Terraform/Cloudformation/YAML/Dockerfiles<br/>
                            5. Python Code/Java Code/JS/Go/Angular<br/>
                            6. Hardcoding against Data Breaching<br/><br/>Thank You'''
            },
            "DAST": {
                "subject": "The DAST Assessments Reports",
                "attachments": ["All_ZAP_Reports.zip"],
                "html": ''' Dear Team, <br/><br/> This is the <b>DAST/Pen Testing Assessments Reports</b> against Targeted Web Application(s)<br/>
                            <br/><b>The OWASP Top 10 vulnerabilities reported:</b><br/>
                            1. Broken access control<br/>
                            2. Cryptographic failures<br/>
                            3. Injection<br/>
                            4. Insecure design<br/>
                            5. Security misconfiguration<br/>
                            6. Vulnerable and outdated components<br/>
                            7. Identification and authentication failures<br/>
                            8. Software and data integrity failures<br/>
                            9. Security logging and monitoring failures<br/>
                            10. Server-side request forgery (SSRF)<br/><br/>Thank You'''
            },
            "IPAbusedDB": {
                "subject": "IP Abuse Investigation Assessments Reports",
                "attachments": ["report.xlsx"],
                "html": ''' Dear Team, <br/><br/> This is the <b>IP Abuse Investigation Assessments Reports</b> against Codecommit<br/>
                            <br/><b>The Types of Security Investigation have been processed as follows:</b><br/>
                            1. IP Address<br/>
                            2. Total Reports<br/>
                            3. Domain<br/>
                            4. Usage Type<br/>
                            5. ISP<br/>
                            6. Abuse Confidence<br/>
                            7. Score<br/>
                            8. Is Whitelisted<br/>
                            9. Last Reported At<br/><br/>Thank You'''
            },
            # Add more pipeline cases as required...
        }

        for key, value in content_map.items():
            if re.search(key, self.pipeline_type, re.IGNORECASE):
                logging.info(f"Email content for {self.pipeline_type} found.")
                return value['subject'], value['attachments'], value['html']

        logging.warning(f"No matching email content found for pipeline type: {self.pipeline_type}")
        return None, None, None

def main():
    if len(sys.argv) < 6:
        logging.error("Insufficient arguments provided.")
        print("Usage: python script.py <mailUname> <AppmailPwd> <PipelineType> <fromEmail> <recipientMail>")
        sys.exit(1)

    try:
        mail_uname = sys.argv[1]
        mail_pwd = sys.argv[2]
        pipeline_type = sys.argv[3]
        from_email = sys.argv[4]
        recipients_mail_list = [sys.argv[5]]

        smtp_host = "smtp.office365.com"
        smtp_port = 587

        # Initialize the PipelineMailSender subclass
        pipeline_mail_sender = PipelineMailSender(smtp_host, smtp_port, mail_uname, mail_pwd, from_email, recipients_mail_list, pipeline_type)

        # Get the subject, attachments, and HTML content for the email
        mail_subject, attachment_fpaths, mail_content_html = pipeline_mail_sender.get_mail_content()

        if not mail_subject:
            logging.error(f"Unknown pipeline type: {pipeline_type}")
            sys.exit(1)

        # Send the email
        pipeline_mail_sender.send_email(mail_subject, mail_content_html, attachment_fpaths)

        logging.info("The email has been sent successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
