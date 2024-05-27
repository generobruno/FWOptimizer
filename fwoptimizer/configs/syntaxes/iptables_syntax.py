""" syntaxTable
        Tabla con la sintaxis de las distintas instrucciones de iptables.
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
#TODO Revisar optional option value "[]"
syntaxTable = {

    "filter": { 
        
        "BasicOperations": {    # Basic Filter Match operations
            "-i | --in-interface": "(?:!\s*)?\w+",
            "-o | --out-interface": "(?:!\s*)?\w+",
            "-s | --source | --src": "(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-d | --destination | --dst": "(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-p | --protocol": "(?:!\s*)?\w+",
            "-j | --jump": "\w+",
            "[!]-f | -f | --fragment": "\s", 
            "-c | --set-counters": None,
            "-m | --match": "\w+"  # Match module identifier
        },
        
        "Extensions": {         # Target Match Extensions
            "LOG": { # -j LOG Extensions
                "--log-level": "\\d+",
                "--log-prefix": "\"[^\"]+\"",
                "--log-ip-options": None,
                "--log-tcp-sequence": None,
                "--log-tcp-option": None
            },
            "REJECT": { # -j REJECT Extensions
                "--reject-with": "(?:icmp-\\w+|tcp-reset|echo-reply)",
                "--log-tcp-sequence": None,
                "--log-tcp-option": None
            },
            "ULOG": {
                #TODO
            }
        },
        
        "MatchModules": {       # Table Match Extensions
            "multiport": {
                "--source-port | --sport | --sports": "\\d+(?:,\\d+)*",
                "--destination-port | --dport | --dports": "\\d+(?:,\\d+)*",
                "--port": "\\d+(?:,\\d+)*"
            },
            "tcp": {
                "--source-port | --sport": "(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": "(?:!\s*)?\d+(?::\d+)?",
                "--tcp-flags": "(?:!\s*)?\w+(?:,\w+)?\s*(?:(?:!\s*)?\w+(?:,\w+)?)?",
                "--syn": None,
                "--tcp-option": "(?:!\s*)?\d+"
            },
            "udp": {
                "--source-port | --sport": "(?:!\s*)?\d+(?::\d+)?",
                "--destination-port | --dport": "(?:!\s*)?\d+(?::\d+)?"
            },
            "icmp": {
                "--icmp-type": "(?:!\s*)?\w+"
            },
            "limit": {
                "--limit": "\\d+(?:/\\w+)?",
                "--limit-burst": "\\d+"
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
                "--ctstate": "(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "state": {
                "--state": "(NEW|ESTABLISHED|RELATED|INVALID)"
            },
            "set": {
                "--match-set": "\\w+\\s+(src|dst)(?:,\\s*(src|dst)){0,5}",
                "--return-nomatch": None,
                "! --update-counters": None,
                "! --update-subcounters": None,
                "[!] --packets-eq": "\\d+",
                "--packets-lt": "\\d+",
                "--packets-gt": "\\d+",
                "[!] --bytes-eq": "\\d+",
                "--bytes-lt": "\\d+",
                "--bytes-gt": "\\d+"
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
                "--src-range": "((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
                "--dst-range": "((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            },
            "length": {
                "--length": ""
            }
        }
    },

    "nat": {
            #TODO
    },

    "mangle": {
            #TODO
    },
    
    "raw": {
            #TODO
    }
    
}