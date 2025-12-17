import psutil
import socket
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, NoValidConnectionsError
import time
from datetime import datetime

def get_int_ip():
    # Get all network interfaces
    interfaces = psutil.net_if_addrs()
    # interfaces now includes all your different interface: Wifi, SSL VPN, Physical,..
    for interface_name, interface_info in interfaces.items():
        # Get Wi-Fi interface IP address you can replace 'Wi-Fi' with 'FortiClient' for example for ssl vpn interface
        if 'Wi-Fi' in interface_name:
            for address in interface_info:
                # Check if the address is IPv4
                if address.family == socket.AF_INET:
                    return f"{address.address}"

    return "Wi-Fi interface not found or no IP assigned."

#connect over SSH
def connect_ssh(sw_ip):
    # SSH connection details
    ssh_username = "ssh_username"
    ssh_password = "ssh_pass"

    # Establish SSH connection
    try:
        # Establish SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(sw_ip, username=ssh_username, password=ssh_password)
        print(f"Successfully connected to {sw_ip}")
        return ssh_client  # You can return the client object if needed for further operations

    except AuthenticationException:
        print(f"Authentication failed for {sw_ip}. Please check your credentials.")
    except NoValidConnectionsError:
        print(f"Unable to establish a connection to {sw_ip}. The device might be unreachable.")
    except SSHException as ssh_error:
        print(f"Error occurred while connecting to {sw_ip}: {str(ssh_error)}")
    except Exception as e:
        print(f"An unexpected error occurred while connecting to {sw_ip}: {str(e)}")
    return None

#backup the config
def backup_running_config(sw_ip, tftp_ip, site_name):
    # get ssh_client
    ssh_client = connect_ssh(sw_ip)
    if ssh_client is None:
        return
    # Create a shell object
    ssh_shell = ssh_client.invoke_shell()

    # Wait for the shell to be ready
    time.sleep(1)

    # Read the hostname
    hostname = ssh_shell.recv(65535).decode()[2:-1]

    #current date as str
    date_string = datetime.now().date().strftime("%Y-%m-%d")

    # create file name: site_name + sw_hostname + current_date
    file_name = site_name + "_" + hostname + "_" + date_string
    print(f"backup file name: {file_name}")
    #print file name for debuggind:
    
    # Send command to enter privileged EXEC mode
    ssh_shell.send("enable\n")
    time.sleep(1)
    
    # Send the enable password
    enable_password = "enable password"
    ssh_shell.send(enable_password + "\n")
    time.sleep(1)

    # Send command to copy running config to TFTP server
    ssh_shell.send(f"copy running-config tftp:\n")
    ssh_shell.send(f"{tftp_ip}\n")
    ssh_shell.send(f"{file_name}\n")
    time.sleep(2)
    
    # Close SSH shell
    ssh_shell.close()
    
    # Close SSH connection
    ssh_client.close()
    print(f"Switch {sw_ip} Back UP Done!\n")
    return hostname


#Loop over array of switches, Back-up one by one and print progress
def backup_site_switches(site_name,switches_arr,tftp):
    #start this site backup
    print(f"##### {site_name} Backup Start #####")
    for sw in switches_arr:
        backup_running_config(sw, tftp,site_name)
    print(f"##### {site_name} Backup Done! #####")

if __name__ == "__main__":
    #get the tftp server IP
    tftp_server = get_int_ip()
    #create an array for VirtualComp site switches
    VirtualComp_switches = ["192.168.20.1","192.168.20.2","192.168.20.4","192.168.20.5","192.168.20.6"]
    #backup VirtualComp site switches
    backup_site_switches("VirtualComp",VirtualComp_switches,tftp_server)