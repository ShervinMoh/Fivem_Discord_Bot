# FiveM Discord Management Bot

![Discord Bot](https://img.shields.io/badge/Discord-Python%20Bot-blue)
![FiveM Integration](https://img.shields.io/badge/FiveM-Integration-orange)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Discord bot for managing FiveM gaming communities with role management, moderation tools, and server monitoring.

## Features

### 🛠️ Administration Tools
- **Role Management**: Add/remove roles from members
- **User Moderation**: Kick/ban members with reason logging
- **Channel Controls**: Manage member access and rename channels
- **Announcements**: Post styled announcements to any channel

### 📊 Server Monitoring
- Real-time FiveM player count in bot status
- Automatic updates every 30 seconds
- Server status detection (online/offline)

### 📝 Audit Logging
- All actions logged to dedicated channel
- Detailed records of:
  - Command used
  - Executing admin
  - Target user/channel
  - Timestamp

## Command Reference

### 👥 Role Commands
| Command | Usage | Description |
|---------|-------|-------------|
| `!addrole` | `!addrole @role @user` | Adds role to user |
| `!removerole` | `!removerole @role @user` | Removes role from user |

### ⚖️ Moderation
| Command | Usage | Description |
|---------|-------|-------------|
| `!kick` | `!kick @user [reason]` | Kicks user with optional reason |
| `!ban` | `!ban @user [reason]` | Bans user with optional reason |

### 📌 Channel Management
| Command | Usage | Description |
|---------|-------|-------------|
| `!addmember` | `!addmember #channel @user` | Grants channel access |
| `!removemember` | `!removemember #channel @user` | Revokes channel access |
| `!renamechannel` | `!renamechannel #channel new_name` | Renames channel |
| `!sendmessage` | `!sendmessage #channel message` | Posts announcement |

## 🚀 Installation

### Requirements
- Python 3.6+
- discord.py (`pip install discord.py`)
- requests (`pip install requests`)

### Configuration
1. Replace placeholders in config:
   ```python
   # Replace these values:
   'YOUR CHANNEL ID'    # Command channel ID
   'YOUR CATEGORY ID'   # Ticket category ID
   'YOUR_TOKEN'         # Discord bot token
   'YOUR FIVEM SERVER IP' # FiveM server API endpoint

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
