from clickhouse_connect import get_client

class ClickHouseConnector:
    def __init__(self, host, port, database=None, user=None, password=None, jwt_token=None):
        self.client = get_client(
            host=host,
            port=int(port),
            username=user,
            password=password or jwt_token,
            database=database,
            secure=False
        )
    
    def get_tables(self):
        return self.client.query("SHOW TABLES").result_rows
        
def get_clickhouse_client(host, port, username=None, password=None, database=None):
    try:
        client = get_client(
            host=host,
            port=int(port),
            username=username or 'default',
            password=password or '',
            database=database or 'default',
            # Add these critical settings:
            connect_timeout=10,
            send_receive_timeout=30,
            verify=False if host == 'localhost' else True
        )
        # Test connection immediately
        client.query('SELECT 1')
        return client
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        raise