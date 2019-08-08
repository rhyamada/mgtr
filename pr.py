from prometheus_client import start_http_server, Summary
import random
import time
from ldap3 import Server, Connection, NONE

LDAP_TIME = Summary('ldap_processing_seconds', 'Time spent ldap')

@LDAP_TIME.time()
def testa_ldap(host):
    try:    
        server = Server(host, get_info=NONE)
        conn = Connection(server, 'uid=estacao,ou=redelocal,ou=corp,dc=serpro,dc=gov,dc=br', 'estacao@rlsl', auto_bind=True)
        conn.search('dc=serpro,dc=gov,dc=br', '(&(objectclass=person)(uid=estacao))')
        print(conn.entries)
    except:
        time.sleep(10)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(3000)
    while True:
        testa_ldap('slave-spo-reg.spo.serpro' if random.random() < 0.9 else 'slave-spo-reg.spo.serpro:672')
        time.sleep(5)
