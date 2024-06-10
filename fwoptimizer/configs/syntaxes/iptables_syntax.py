"""
syntaxTable
        Table with the syntax of different iptables instructions.
        "Table": {
            "OperationType": {
                "option": "regex of its value"
            }
        }
        
        iptables-save syntax:
        *<table>
        :<chain> <policy> [<packets_count>:<bytes_count>]
        <optional_counter><rule>
        ... more rules ...
        COMMIT
"""

syntaxTable = {

    "filter": {
        "BasicOperations": {    # Basic Filter Match operations
            "-i | --in-interface": 
                r"(?:!\s*)?\w+",
            "-o | --out-interface": 
                r"(?:!\s*)?\w+",
            "-s | --source | --src": 
                r"(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-d | --destination | --dst": 
                r"(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-p | --protocol": 
                r"(?:!\s*)?\w+",
            "-j | --jump": 
                r"\w+",
            "[!]-f | -f | --fragment": 
                r"\s", 
            "-c | --set-counters": 
                "NO_VALUE",
            "-m | --match": 
                r"\w+"  # Match module identifier
        },

        "Extensions": {         # Target Match Extensions
            "LOG": { # -j LOG Extensions
                "--log-level": r"(emerg|alert|crit|error|warning|notice|info|debug|\d+)",
                "--log-prefix": r"\"?[^\"]{0,29}\"?",
                "--log-tcp-sequence": "NO_VALUE",
                "--log-tcp-options": "NO_VALUE",
                "--log-ip-options": "NO_VALUE",
                "--log-uid": "NO_VALUE"
            },
            "REJECT": { # -j REJECT Extensions
                "--reject-with": r"(?:icmp-\w+|tcp-reset|echo-reply)",
                "--log-tcp-sequence": "NO_VALUE",
                "--log-tcp-option": "NO_VALUE"
            },
            "ULOG": {
                #TODO
            }
        },

        "MatchModules": {       # Table Match Extensions
            "multiport": {
                "--source-port | --sport | --sports": r"\d+(?:,\d+)*",
                "--destination-port | --dport | --dports": r"\d+(?:,\d+)*",
                "--port": r"\d+(?:,\d+)*"
            },
            "tcp": {
                "--source-port | --sport": r"(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": r"(?:!\s*)?\d+(?::\d+)?",
                "--tcp-flags": r"(?:!\s*)?\w+(?:,\w+)?\s*(?:(?:!\s*)?\w+(?:,\w+)?)?",
                "--syn": "NO_VALUE",
                "--tcp-option": r"(?:!\s*)?\d+"
            },
            "udp": {
                "--source-port | --sport": r"(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": r"(?:!\s*)?\d+(?::\d+)?"
            },
            "icmp": {
                "--icmp-type": r"(?:!\s*)?\w+"
            },
            "limit": {
                "--limit": r"\d+(?:/\w+)?",
                "--limit-burst": r"\d+"
            },
            "dstlimit": {
                "--dstlimit": "",
                "--dstlimit-mode": "",
                "--dstlimit-name": "",
                "--dstlimit-burst": "",
                "--dstlimit-htable-size": "",
                "--dstlimit-htable-max": "",
                "--dstlimit-htable-gcinterval": "",
                "--dstlimit-htable-expire": ""
            },
            "conntrack": {
                "--ctstate": r"(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "state": {
                "--state": r"(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "set": {
                "--match-set": r"[\w-]+\s+(src|dst)(?:,\s*(src|dst)){0,5}",
                "--return-nomatch": "NO_VALUE",
                "! --update-counters": "NO_VALUE",
                "! --update-subcounters": "NO_VALUE",
                "[!] --packets-eq": r"\d+",
                "--packets-lt": r"\d+",
                "--packets-gt": r"\d+",
                "[!] --bytes-eq": r"\d+",
                "--bytes-lt": r"\d+",
                "--bytes-gt": r"\d+"
            },
            "mac": {
                "--mac-source": ""
            },
            "owner": {
                "--uid-owner": "",
                "--gid-owner": "",
                "--pid-owner": "",
                "--sid-owner": "",
                "--cmd-owner": ""
            },
            "mark": {
                "--mark": ""
            },
            "tos": {
                "--tos": ""  
            },
            "unclean": {
                "": ""
            },
            "addrtype": {
                "--src-type": "",
                "--dst-type": ""  
            },
            "iprange": {
                "--src-range": 
                    r"((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
                "--dst-range": 
                    r"((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            },
            "length": {
                "--length": ""
            },
            "connlimit": {
                "--connlimit-upto": r"\d+",
                "--connlimit-above": r"\d+",
                "--connlimit-mask": r"\d{1,3}",
                "--connlimit-saddr": "NO_VALUE",
                "--connlimit-daddr": "NO_VALUE"
            },
            "recent": {
                "--name": r"\w+",
                "! --set | --set": "NO_VALUE",
                "--rsource": "NO_VALUE",
                "--rdest": "NO_VALUE",
                "--mask": r"\d{1,3}",
                "! --rcheck | --rcheck": "NO_VALUE",
                "! --update | --update": "NO_VALUE",
                "! --remove | --remove": "NO_VALUE",
                "--seconds": r"\d+",
                "--reap": "NO_VALUE",
                "--hitcount": r"\d+",
                "--rttl": "NO_VALUE"
            }
        }
    },

    "nat": {
        "BasicOperations": {    # Basic Filter Match operations
            "-i | --in-interface": 
                r"(?:!\s*)?\w+",
            "-o | --out-interface": 
                r"(?:!\s*)?\w+",
            "-s | --source | --src": 
                r"(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-d | --destination | --dst": 
                r"(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-p | --protocol": 
                r"(?:!\s*)?\w+",
            "-j | --jump": 
                r"\w+",
            "[!]-f | -f | --fragment": 
                r"\s", 
            "-c | --set-counters": 
                "NO_VALUE",
            "-m | --match": 
                r"\w+"  # Match module identifier
        },

        "Extensions": {         # Target Match Extensions
            "SNAT": { 
                "--to-source": r"((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?)(?::(\d+)(-(\d+)))?",
                "--random": "NO_VALUE",
                "--random-fully": "NO_VALUE",
                "--persistent": "NO_VALUE"
            },
            "MASQUERADE": { 
                "--to-ports": r"(\d+)(-(\d+))?",
                "--random": "NO_VALUE",
                "--random-fully": "NO_VALUE"
            },
            "DNAT": {
                "--to-destination": r"((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?)(?::(\d+)(-(\d+)))?",
                "--random": "NO_VALUE",
                "--persistent": "NO_VALUE"
            },
            "REDIRECT": {
                "--to-ports": r"(\d+)(-(\d+))?",
                "--random": "NO_VALUE"
            },
            "BALANCE": {
                "--to-destination": r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            }
        },

        "MatchModules": {       # Table Match Extensions
            "multiport": {
                "--source-port | --sport | --sports": r"\d+(?:,\d+)*",
                "--destination-port | --dport | --dports": r"\d+(?:,\d+)*",
                "--port": r"\d+(?:,\d+)*"
            },
            "tcp": {
                "--source-port | --sport": r"(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": r"(?:!\s*)?\d+(?::\d+)?",
                "--tcp-flags": r"(?:!\s*)?\w+(?:,\w+)?\s*(?:(?:!\s*)?\w+(?:,\w+)?)?",
                "--syn": "NO_VALUE",
                "--tcp-option": r"(?:!\s*)?\d+"
            },
            "udp": {
                "--source-port | --sport": r"(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": r"(?:!\s*)?\d+(?::\d+)?"
            },
            "icmp": {
                "--icmp-type": r"(?:!\s*)?\w+"
            },
            "limit": {
                "--limit": r"\d+(?:/\w+)?",
                "--limit-burst": r"\d+"
            },
            "dstlimit": {
                "--dstlimit": "",
                "--dstlimit-mode": "",
                "--dstlimit-name": "",
                "--dstlimit-burst": "",
                "--dstlimit-htable-size": "",
                "--dstlimit-htable-max": "",
                "--dstlimit-htable-gcinterval": "",
                "--dstlimit-htable-expire": ""
            },
            "conntrack": {
                "--ctstate": r"(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "state": {
                "--state": r"(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "set": {
                "--match-set": r"[\w-]+\s+(src|dst)(?:,\s*(src|dst)){0,5}",
                "--return-nomatch": "NO_VALUE",
                "! --update-counters": "NO_VALUE",
                "! --update-subcounters": "NO_VALUE",
                "[!] --packets-eq": r"\d+",
                "--packets-lt": r"\d+",
                "--packets-gt": r"\d+",
                "[!] --bytes-eq": r"\d+",
                "--bytes-lt": r"\d+",
                "--bytes-gt": r"\d+"
            },
            "mac": {
                "--mac-source": ""
            },
            "owner": {
                "--uid-owner": "",
                "--gid-owner": "",
                "--pid-owner": "",
                "--sid-owner": "",
                "--cmd-owner": ""
            },
            "mark": {
                "--mark": ""
            },
            "tos": {
                "--tos": ""  
            },
            "unclean": {
                "": ""
            },
            "addrtype": {
                "--src-type": "",
                "--dst-type": ""  
            },
            "iprange": {
                "--src-range": r"((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
                "--dst-range": r"((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            },
            "length": {
                "--length": ""
            },
            "connlimit": {
                "--connlimit-upto": r"\d+",
                "--connlimit-above": r"\d+",
                "--connlimit-mask": r"\d{1,3}",
                "--connlimit-saddr": "NO_VALUE",
                "--connlimit-daddr": "NO_VALUE"
            },
            "recent": {
                "--name": r"\w+",
                "! --set | --set": "NO_VALUE",
                "--rsource": "NO_VALUE",
                "--rdest": "NO_VALUE",
                "--mask": r"\d{1,3}",
                "! --rcheck | --rcheck": "NO_VALUE",
                "! --update | --update": "NO_VALUE",
                "! --remove | --remove": "NO_VALUE",
                "--seconds": r"\d+",
                "--reap": "NO_VALUE",
                "--hitcount": r"\d+",
                "--rttl": "NO_VALUE"
            }
        }
    },

    "mangle": {
            #TODO
    },

    "raw": {
            #TODO
    }

}

"""
FieldsFormat
    Table with the assignments between iptables options and their corresponding field.
    "options": "FieldName"
"""

FieldsFormat = {
    # Filter
    "-i | --in-interface": "InInterface",
    "-o | --out-interface": "OutInterface",
    "-s | --source | --src": "SrcIP",
    "-d | --destination | --dst": "DstIP",
    "-p | --protocol": "Protocol",
    "--source-port | --sport | --sports": "SrcPort",
    "--destination-port | --dport | --dports": "DstPort",
    "--ctstate | --state": "State",
    # NAT
    "--to-source": "ToSrc",
    "--to-destination": "ToDst"
}
