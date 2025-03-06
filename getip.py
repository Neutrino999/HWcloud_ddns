import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 获取公网IP
def get_public_ip():
    try:
        response = requests.get('http://host:5010/get_ip')
        data = response.json()
        ip = data.get('ip')
        return ip
    except Exception as e:
        print(f"Error while fetching IP: {e}")
        return None

# 读取存储的上次IP
def read_last_ip(file_path='ip.txt'):
    try:
        with open(file_path, 'r') as file:
            last_ip = file.read().strip()
            return last_ip
    except FileNotFoundError:
        return None  # 如果文件不存在，说明没有记录过IP

# 将当前IP写入ip.txt
def write_current_ip(ip, file_path='ip.txt'):
    try:
        with open(file_path, 'w') as file:
            file.write(ip)
    except Exception as e:
        print(f"Error while writing IP to file: {e}")

# 发送邮件通知
def send_email(subject, body, to_email):
    try:
        from_email = 'from_email'  # 发件邮箱地址
        from_password = 'from_password'  # 发件邮箱密码
        to_email = 'to_email'  # 收件邮箱地址

        # 设置SMTP服务器
        smtp_server = 'smtp.163.com'  # 163邮箱的SMTP服务器
        smtp_port = 465  # 163邮箱SMTP端口号

        # 设置邮件内容
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # 连接到SMTP服务器并发送邮件
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error while sending email: {e}")

def main():
    current_ip = get_public_ip()
    if current_ip:
        print(f"Current IP: {current_ip}")

        # 读取之前存储的IP
        last_ip = read_last_ip()

        # 如果IP不一致，更新并发送邮件通知
        if last_ip != current_ip:
            print(f"IP has changed from {last_ip} to {current_ip}")
            write_current_ip(current_ip)  # 更新文件中的IP

            # 运行python脚本ddns.py更新DNS记录
            os.system('python ddns.py')

            # 发送邮件通知
            subject = "IP Address Changed"
            body = f"The IP address has changed from {last_ip} to {current_ip}."
            to_email = 'recipient@example.com'  # 收件人邮箱地址
            send_email(subject, body, to_email)
        else:
            print("IP has not changed.")
    else:
        print("Failed to fetch current IP.")

if __name__ == "__main__":
    main()