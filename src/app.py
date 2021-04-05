import smtplib
import string 
from random import choice
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, send_file
from config import AUTH_ID, AUTH_PW
from config import SUBJECT, HTML

'''
https://answer-id.com/ko/882712
'''

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/tracking/<rand>")
def open_tracking(rand):
	print("%s님이 메일을 열람하였습니다." % rand)
	'''
	Do Something...!
	'''
	return send_file(
		'static/mini.png',
		mimetype='image/gif'
	)

@app.route('/send/<email>')
def send_mail(email):

	# SMTP 서버 접속
	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(AUTH_ID, AUTH_PW)

	# 제목, 내용에서 문자열 치환 전처리
	subject = SUBJECT.replace("%이메일%", email)
	html = HTML.replace('%이메일%', email)
	# 이메일 고유 난수값 생성
	string_pool = string.ascii_letters
	rand = [choice(string_pool) for i in range(10)]
	html = html.replace('%랜덤%', "".join(rand))

	# 이메일 문서 생성
	msg = MIMEMultipart()
	msg['From'] = AUTH_ID
	msg['To'] = email
	msg['Subject'] = subject
	msg.attach(MIMEText(html, 'html'))

	# 이메일 전송
	smtp.sendmail(
		AUTH_ID,
		email,
		msg.as_string()
	)
	smtp.quit()
	return {'msg': 'success'}


if __name__ == '__main__':
	app.run(debug=True)