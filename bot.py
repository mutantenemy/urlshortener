import mechanize
import time
hostname="http://localhost:5000/"
start = time.time()

br = mechanize.Browser()
codes = []

for i in range (100):
    response = br.open(hostname)
    br.select_form("transformer")         # works when form has a name
    control = br.form.find_control("url")
    control.value = "http://" + str(i) + ".com"
    response = br.submit()
    for link in br.links():
        codes.append(link.url[len(hostname):])
    print (codes[i])

stop = time.time()
endCreation = stop - start

# for i in range (1):
#     print ("requesting accesst to: " + hostname + str(codes[i]))
#     response = br.open(hostname+str(codes[i]))
#     print (i)

end = time.time()
endChecking = end - stop

print("TIME ELAPSED: " + str(endChecking + endCreation))
print("Time creating: " + str(endCreation))
print("Time checking: " + str(endChecking))
