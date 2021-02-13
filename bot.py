import mechanize
import time
start = time.time()

br = mechanize.Browser()


for i in range (10):
    response = br.open("http://localhost:5000")
    br.select_form("transformer")         # works when form has a name
    control = br.form.find_control("url")
    control.value = "http://i.com"
    response = br.submit()
    print ()

end = time.time()
print (end - start)