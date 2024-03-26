# Libs
import paramiko
import os
from dotenv import load_dotenv

# Env vars
load_dotenv()

def download_file(remote_path):
  # Create client
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

  try:
    # Conection
    client.connect(hostname = os.getenv('SFTP_HOST'), username = os.getenv('SFTP_USER'), password = os.getenv('SFTP_PASS'))
    sftp = client.open_sftp()

    # Get file
    sftp.get(remotepath = os.getenv('SFTP_DIR') + remote_path, localpath = os.getenv('LOC_DIR') + remote_path)

    print(f"Downloaded! {remote_path}")
  except Exception as e:
    print(f"Error downloading {remote_path}: {e}")
  finally:
    # Close connection
    sftp.close()
    client.close()

download_file('/files/proyectos/4/4-20170331-211323-1187279183.doc')