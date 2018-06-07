from network import LTE
import urequests as requests
lte = LTE()

def send_at_cmd_pretty(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    for line in response:
        print(line)




send_msg(lat,lon,dev_id,reason):
print("gps is")
print(lat,lon)
print("Mac ID is ..")
print(dev_id)
print("Wakeup reason")
print(reason)

send_at_cmd_pretty('AT+CFUN=0')
send_at_cmd_pretty('AT!="clearscanconfig"')
send_at_cmd_pretty('AT!="addscanfreq band=28 dl-earfcn=9410"')
send_at_cmd_pretty('AT+CGDCONT=1,"IP","telstra.m2m"')
send_at_cmd_pretty('AT+CEREG=2')
send_at_cmd_pretty('AT+CFUN=1')


lteAttachAttemptCount = 0


while not lte.isattached():
    lteAttachAttemptCount += 1
    print("Count")
    print(lteAttachAttemptCount)
    time.sleep(1)
    send_at_cmd_pretty('AT!="showphy"')
    send_at_cmd_pretty('AT!="fsm"')
    send_at_cmd_pretty('AT+CEREG?')
    if(lteAttachAttemptCount > 60):
        print("Attach failed: Send LTE RESET ..")
        flashLed(led_red, 3)
        send_at_cmd_pretty('AT^RESET')
        print("Reset chip in 1 seconds ..")
        time.sleep(1)
        machine.reset()


lteConnectAttemptCount = 0

lte.connect()
while not lte.isconnected():
    lteConnectAttemptCount += 1
    print("Count")
    print(lteConnectAttemptCount)
    time.sleep(4.0)
    if(lteConnectAttemptCount > 5):
        flashLed(led_red, 5)
        print("Connect failed: Send LTE RESET ..")
        send_at_cmd_pretty('AT^RESET')
        print("Reset chip in 1 seconds ..")
        time.sleep(1)
        machine.reset()


print ('connected - yipee !!!!!!!!!!!!!') # used for debugging
flashLed(led_green, 5)
print("now upload to platform......")

#  r = requests.get("http://ratserver.australiaeast.cloudapp.azure.com/smart-trap/apiGW/apiGWcatM1.php", json={'ph': '8.2', 'orp': '624', 'flow': '5', 'temp': '20.3'} )

r = requests.get("http://ratserver.australiaeast.cloudapp.azure.com/smart-trap/apiGW/apiGWcatM1.php", json={'devId': dev_id, 'lat': lat, 'lon': lon} )

print(r)
print(r.text)
# It's mandatory to close response objects as soon as you finished
# working with them. On MicroPython platforms without full-fledged
# OS, not doing so may lead to resource leaks and malfunction.
r.close()

print('disconnect & detach modem')
lte.disconnect()
lte.dettach()
lte.deinit()
print('clean up')
lte = None
gc.collect()
print('Done sendEvent')








