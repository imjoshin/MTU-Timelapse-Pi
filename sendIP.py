import smtplib, auth, subprocess, urllib2


while True:
        try:
            response = urllib2.urlopen('http://google.com',timeout=1)
            break
        except urllib2.URLError:
            pass

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
