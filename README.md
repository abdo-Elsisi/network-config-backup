# ⚙️ Network Switch Configuration Backup Script

This Python script automates the backup of running configurations from network switches to a TFTP server over an SSH connection.

## ✨ Features

* **Automated IP Retrieval:** Dynamically determines the host machine's Wi-Fi IP address for use as the TFTP server address.
* **Also support other interfaces Like ssl vpn interface or physical interface
* **SSH Connectivity:** Uses `paramiko` to establish a secure SSH connection to the switches.
* **Privileged Execution:** Handles password-based privilege escalation (`enable` mode).
* **Dynamic Naming:** Creates a unique backup filename using the site name, switch hostname, and current date (`<SITE_NAME>_<HOSTNAME>_<YYYY-MM-DD>`).
* **Error Handling:** Includes checks for common SSH failures (authentication, connection, and general errors).

## 🛠️ Prerequisites

Before running the script, ensure you have the following installed:

1.  **Python 3**
2.  **TFTP Server:** A running TFTP server on the machine executing the script (or at the IP retrieved by `get_int_ip`).
3.  **Required Python Libraries:**
    ```bash
    pip install psutil paramiko
    ```

## 🚀 Usage

### 1. Configuration

Open `ScriptBKUP.py` and modify the following variables in the `connect_ssh` and `backup_running_config` functions to match your network credentials:

* `ssh_username` (in `connect_ssh`)
* `ssh_password` (in `connect_ssh`)
* `enable_password` (in `backup_running_config`)

In the `if __name__ == "__main__":` block, update the switch array for your site:

```python
    # Update this with your site's switches
    VirtualComp_switches = ["192.168.20.1", "192.168.20.2", "...", "...."]
    # Pass your site name and the array to the backup function
    backup_site_switches("VirtualComp", VirtualComp_switches, tftp_server)
