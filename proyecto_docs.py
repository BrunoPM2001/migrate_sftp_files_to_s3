# Libs
import paramiko
import mysql.connector
import os
from dotenv import load_dotenv

# Env vars
load_dotenv()
success_count = 0
error_count = 0

# Download a file using SFTP
def download_file(remote_path):
  global success_count
  global error_count

  # Create client
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

  try:
    # Conection
    client.connect(hostname = os.getenv('SFTP_HOST'), username = os.getenv('SFTP_USER'), password = os.getenv('SFTP_PASS'))
    sftp = client.open_sftp()

    # Create dir and get file
    i = remote_path.rfind('/')
    folder = remote_path[:i]
    if not os.path.exists(os.getenv('LOC_DIR') + folder):
      os.makedirs(os.getenv('LOC_DIR') + folder)
    sftp.get(remotepath = os.getenv('SFTP_DIR') + remote_path, localpath = os.getenv('LOC_DIR') + remote_path)

    success_count += 1
  except Exception as e:
    error_count += 1
    print(f"Error downloading {remote_path}: {e}")
  finally:
    # Close connection
    sftp.close()
    client.close()

def getList():
  try:
    # Connection to mysql
    conn = mysql.connector.connect(
      host = os.getenv('MYSQL_HOSTNAME'),
      user = os.getenv('MYSQL_USERNAME'),
      password = os.getenv('MYSQL_PASSWORD'),
      database = os.getenv('MYSQL_DATABASE'),
      port = os.getenv('MYSQL_PORT')
    )

    # Query
    cursor = conn.cursor()
    cursor.execute(os.getenv('MYSQL_QUERY'))
    res = cursor.fetchall()

    print("Query executed!")
    return res
  except Exception as e:
    print(f"Error connectiong: {e}")
  finally:
    # Close connection
    conn.close()

# Using both functions
myList = getList()
for item in myList:
  download_file(item[0])

print("Results:")
print(f"Success: {success_count}")
print(f"Error: {error_count}")