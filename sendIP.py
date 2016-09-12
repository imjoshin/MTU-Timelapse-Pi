import smtplib, auth, subprocess

ip = subprocess.Popen("wget http://ipinfo.io/ip -qO -", shell=True, stdout=subprocess.PIPE).communicate()[0]

msg = "\r\n".join([
  "From: " + auth.EMAIL,
  "To: " + auth.EMAIL,
  "Subject: Raspberry Pi IP",
  "",
  "IP: " + ip
  ])

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(auth.EMAIL, auth.EPASS)
server.sendmail(auth.EMAIL, auth.EMAIL, msg)
server.quit()
