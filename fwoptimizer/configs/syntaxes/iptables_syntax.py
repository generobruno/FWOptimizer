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

syntaxTable = {

    "filter": { 
        "RuleOperations": {
            "-i | --in-interface": "(?:!\s*)?\w+",
            "-o | --out-interface": "(?:!\s*)?\w+",
            "-s | --source| --src": "(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-d | --destination| --dst": "(?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?",
            "-p | --protocol": "(?:!\s*)?\w+",

            "-j | --jump": "\w+",

            "[!]-f | -f | --framgent": "\s",

            "-c | --set-counters": None,
            
            "-m": "\w+", #TODO Revisar 

            "--source-port | --sport": "(?:!\s*)?\d+(?::\d+)?",
            "--destination-port | --dport": "(?:!\s*)?\d+(?::\d+)?",

            "--tcp-flags": "(?:!\s*)?\w+(?:,\w+)?\s*(?:(?:!\s*)?\w+(?:,\w+)?)?",
            "--syn": None,
            "--tcp-option": "(?:!\s*)?\d+",

            "--icmp-type": "(?:!\s*)?\w+",
            
             "--src-range": "((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
             "--dst-range": "((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-((?:!\s*)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        },
        "Extensions": {
            # Jump LOG Extensions
            "-j|LOG|--log-level": "\\d+",
            "-j|LOG|--log-prefix": "\"[^\"]+\"",
            "-j|LOG|--log-ip-options": None,
            "-j|LOG|--log-tcp-sequence": None,
            "-j|LOG|--log-tcp-option": None,

            # Jump REJECT Extensions
            "-j|REJECT|--reject-with": "(?:icmp-\\w+|tcp-reset|echo-reply)",
            "-j|REJECT|--log-tcp-sequence": None,
            "-j|REJECT|--log-tcp-option": None,
            
            # Protocol Extensions
            "-p|--protocol|--match|multiport|--source-port": "\\d+(?:,\\d+)*",
            "-p|--protocol|--match|multiport|--destination-port": "\\d+(?:,\\d+)*",
            "-p|--protocol|--match|multiport|--port": "\\d+(?:,\\d+)*",

            # Match Extensions 
            "--match|limit|--limit": "\\d+(?:/\\w+)?",
            "--match|limit|--limit-burst": "\\d+",
            "--match|state|--state": "(NEW|ESTABLISHED|RELATED|INVALID)"
        }
    },

    "NAT": {
            #TODO
    },

    "Mangle": {
            #TODO
    }
    
}