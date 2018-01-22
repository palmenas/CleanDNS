# CleanDNS: Because Detection is Cool but Proactivity is Better!
This is a Proof of Concept Technology for protecting End Users from malware, advanced threat and other malicious content by preventing DNS malicious Request/Responses.

# Considerations
Virtual Hardware Recommended (ALL Back-level Compatibility):
- CPU Type: x86_64 (AMD64)
- 4vCPUs
- 8GB RAM
- 40GB On demand Virtual Disk
- Intel e1000 Virtual Network Interfaces (Mandatory)

Components Used:
- PFSense 2.3.4-Patch1
- Suricata Module
- Bind Module
- Cron Module
- Service Watchdog Module
- SNORT Community Signature + Emerging Threats for constant update.
- Bring Your Own SNORT OINKCODE to get advanced rules.

Features
- Inline DNS Request Filter (Suricata IPS)
- IPS Filter for IPS Filter for RansomWareTracker IP Reputation IP Reputation
- IPS Filter for Phistank IP Reputation
- IPS Filter for RansomWareTracker IP Reputation
- DNSEC Recursive DNS Requests
- DNS Dynamic Sinkhole By DShield
- DNS Dynamic Sinkhole By Malware Domain BlockList
- DNS Dynamic Sinkhole By MalwareDomainsLists BlockList
- DNS Dynamic Sinkhole By NetworkSec
- DNS Dynamic Sinkhole By OTX AlienVault
- DNS Dynamic Sinkhole By PhishTank
- DNS Dynamic Sinkhole By RansomWareTracker
- DNS Dynamic Sinkhole By Shalla's BlackList
- DNS Dynamic Sinkhole By SquidGuard Contrib
- DNS Dynamic Sinkhole By URLBlackList
- DNS Dynamic Sinkhole By Zeustracker
- DNS Dynamic Last Resort BlackHole (OPENDNS DNS Services)
- DNS Tunneling Filtering (IOdine Proof)
- Local Whitelist / Blacklist for Domain Sinkhole
- Local Whitelist / Blacklist for IP Reputation

# Installation of python new modules
Make sure you install pip
```
[2.3.4-RELEASE][root@cleandns.localdomain.com]/: python2.7 -m ensurepip
Collecting setuptools
Collecting pip
Installing collected packages: setuptools, pip
Successfully installed pip-9.0.1 setuptools-28.8.0
```

Then requests (needed by OTXv2)
```
[2.3.4-RELEASE][root@cleandns.localdomain.com]/: python2.7 -m pip install requests
Collecting requests
  Downloading requests-2.18.4-py2.py3-none-any.whl (88kB)
    100% |################################| 92kB 1.1MB/s
Collecting chardet<3.1.0,>=3.0.2 (from requests)
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133kB)
    100% |################################| 143kB 1.4MB/s
Collecting certifi>=2017.4.17 (from requests)
  Downloading certifi-2018.1.18-py2.py3-none-any.whl (151kB)
    100% |################################| 153kB 910kB/s
Collecting urllib3<1.23,>=1.21.1 (from requests)
  Downloading urllib3-1.22-py2.py3-none-any.whl (132kB)
    100% |################################| 133kB 1.1MB/s
Collecting idna<2.7,>=2.5 (from requests)
  Downloading idna-2.6-py2.py3-none-any.whl (56kB)
    100% |################################| 61kB 1.7MB/s
Installing collected packages: chardet, certifi, urllib3, idna, requests
Successfully installed certifi-2018.1.18 chardet-3.0.4 idna-2.6 requests-2.18.4 urllib3-1.22
```

Finaly OTXv2
```
[2.3.4-RELEASE][root@cleandns.localdomain.com]/: python2.7 -m pip install OTXv2
Collecting OTXv2
  Downloading OTXv2-1.2.tar.gz
Collecting simplejson (from OTXv2)
  Downloading simplejson-3.13.2.tar.gz (79kB)
    100% |################################| 81kB 1.2MB/s
Installing collected packages: simplejson, OTXv2
  Running setup.py install for simplejson ... done
  Running setup.py install for OTXv2 ... done
Successfully installed OTXv2-1.2 simplejson-3.13.2
```

# Contact
cleandns@cleandns.com.br
