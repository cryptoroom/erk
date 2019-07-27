#
#  Erk IRC Client
#  Copyright (C) 2019  Daniel Hetrick
#               _   _       _                         
#              | | (_)     | |                        
#   _ __  _   _| |_ _  ___ | |__                      
#  | '_ \| | | | __| |/ _ \| '_ \                     
#  | | | | |_| | |_| | (_) | |_) |                    
#  |_| |_|\__,_|\__| |\___/|_.__/ _                   
#  | |     | |    _/ |           | |                  
#  | | __ _| |__ |__/_  _ __ __ _| |_ ___  _ __ _   _ 
#  | |/ _` | '_ \ / _ \| '__/ _` | __/ _ \| '__| | | |
#  | | (_| | |_) | (_) | | | (_| | || (_) | |  | |_| |
#  |_|\__,_|_.__/ \___/|_|  \__,_|\__\___/|_|   \__, |
#                                                __/ |
#                                               |___/ 
#  https://github.com/nutjob-laboratories
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os
import json
import re
from datetime import datetime
from itertools import combinations
from zipfile import ZipFile
import glob
import importlib.util
import platform
import string
import random

(SYSTEM_BITS,LINKAGE)=platform.architecture()
if "Windows" in platform.system():
	RUNNING_ON_WINDOWS = True
else:
	RUNNING_ON_WINDOWS = False
	if sys.maxsize > 2**32:
		SYSTEM_BITS = "64bit"
	else:
		SYSTEM_BITS = "32bit"

SYSTEM_PLATFORM = platform.platform()
PYTHON_EXECUTABLE = sys.executable
PYTHON_IMPLEMENTATION = platform.python_implementation()
PYTHON_VERSION = platform.python_version()

# Globally load in Erk's essential resource file
globals()["erk.erkimg"] = __import__("erk.erkimg")

APPLICATION_NAME = "Ərk"
APPLICATION_VERSION = "0.410"
OFFICIAL_REPOSITORY = "https://github.com/nutjob-laboratories/erk"
PROGRAM_FILENAME = "erk.py"
EDITOR_NAME = "Kōd"
EDITOR_VERSION = "0.54"
NORMAL_APPLICATION_NAME = "Erk"


GPL_NOTIFICATION = """Ərk IRC Client
Copyright (C) 2019  Dan Hetrick

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

# Directories
INSTALL_DIRECTORY = sys.path[0]
ERK_MODULE_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "erk")
LOG_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "logs")
SETTINGS_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "settings")
PLUGIN_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "plugins")
AUTOJOIN_DIRECTORY = os.path.join(SETTINGS_DIRECTORY, "autojoin")
THEMES_DIRECTORY = os.path.join(INSTALL_DIRECTORY, "themes")

# Files
DISPLAY_CONFIGURATION = os.path.join(SETTINGS_DIRECTORY, "text.json")
IRC_NETWORK_LIST = os.path.join(ERK_MODULE_DIRECTORY, "servers.txt")
LAST_SERVER_INFORMATION_FILE = os.path.join(SETTINGS_DIRECTORY, "lastserver.json")
USER_FILE = os.path.join(SETTINGS_DIRECTORY, "user.json")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "erk.json")
EDITOR_SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "kod.json")
IGNORE_FILE = os.path.join(SETTINGS_DIRECTORY, "ignore.json")

PROFANITY_LIST = os.path.join(ERK_MODULE_DIRECTORY, "profanity.txt")

f = open(PROFANITY_LIST,"r")
cursewords = f.read()
f.close()

PROFANITY = cursewords.split("\n")
PROFANITY_SYMBOLS = ["#","!","@","&","%","$","?","+","*"]

THEME_RESOURCE_FILE_NAME = "resources.py"
THEME_ICON_FILE_NAME = "icon.png"
THEME_QSS_FILE_NAME = "widgets.qss"
THEME_JSON_FILE_NAME = "text.json"

# Globals
DEFAULT_NICKNAME = "erk"
DEFAULT_USERNAME = "erk"
DEFAULT_IRCNAME = f"{APPLICATION_NAME} {APPLICATION_VERSION}"
DEFAULT_ALTERNATIVE = DEFAULT_NICKNAME + "_"

TOOLBAR_BUTTON_HEIGHT = 25

SYSTEM_COLOR = "?_!SYS!_?"
SELF_COLOR = "?_!SLF!_?"
USER_COLOR = "?_!USR!_?"
ACTION_COLOR = "?_!ACT!_?"
NOTICE_COLOR = "?_!NOT!_?"
ERROR_COLOR = "?_!ERR!_?"
HIGHLIGHT_COLOR = "?_!HLT!_?"
LINK_COLOR = "?_!LNK!_?"

NEW_CHAT_DIVIDER_TEXT_COLOR = "?_!TXT!_?"
NEW_CHAT_DIVIDER_BACKGROUND_COLOR = "?_!BAK!_?"

# Templates

NEW_CHAT_DIVIDER = f"""<table style="width: 100%; height: 5px;" border="0"><tbody><tr><td style="background-color: {NEW_CHAT_DIVIDER_BACKGROUND_COLOR}; font-size:small;"><i>&nbsp; <font color="{NEW_CHAT_DIVIDER_TEXT_COLOR}"> New chat </font> &nbsp;</i></td></tr></tbody></table>"""

TIMESTAMP_TEMPLATE = """<td style="vertical-align:top; font-size:small; text-align:center;"><i>!TIME!</i></td><td style="font-size:small;">&nbsp;</td>"""

SYSTEM_MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><font color="!COLOR!"><b>!USER!</b></font></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		<td style="text-align: left; vertical-align: top;"><font color="!COLOR!">!MESSAGE!</font></td>
	</tr>
	</tbody>
</table>
"""

CHAT_MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><font color="!COLOR!"><b>!USER!</b></font></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		<td style="text-align: left; vertical-align: top;">!MESSAGE!</td>
	</tr>
	</tbody>
</table>
"""

LOG_MESSAGE_TEMPLATE = f"""
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: right; vertical-align: top;"><font color="!COLOR!">!USER!</font></td>
		<td style="text-align: left; vertical-align: top;">&nbsp;</td>
		<td style="text-align: left; vertical-align: top;">!MESSAGE!</td>
	</tr>
	</tbody>
</table>
"""

ACTION_MESSAGE_TEMPLATE = """
<table style="width: 100%;" border="0">
	<tbody>
	<tr>!TIMESTAMP!
		<td style="text-align: left; vertical-align: top;"><font color="!COLOR!"><b>!USER!</b> <i>!MESSAGE!</i></font></td>
	</tr>
	</tbody>
</table>
"""

SYSTEM_MESSAGE_DISPLAY_SYMBOL = "\u2666"	# UTF-8 "diamond" symbol

LOG_TIMESTAMP = 0
LOG_TEXT = 1

AUTOJOIN_DELIMITER = "/"

MAX_DEFAULT_NICKNAME_SIZE = 16
MAX_SERVER_NICKNAME_SIZE = 20

MAX_LOG_SIZE_DEFAULT = 300

INITIAL_WINDOW_WIDTH = 500
INITIAL_WINDOW_HEIGHT = 350

ADDITIONAL_POINT_SIZE_FOR_USER_DISPLAY = 1

DEFAULT_USERMODE_DISPLAY = "<i>None</i>"

USE_NO_THEME_SETTING = "none"

TIMESTAMP_SETTING = "display_timestamp"
UPTIME_SETTING = "display_uptime"
KEEPALIVE_SETTING = "keep_connection_alive"
INVITE_SETTING = "join_on_channel_invite"
PRIVATEWINDOW_SETTING = "open_window_on_private_message"
INITIALWIDTH_SETTING = "initial_window_width"
INITIALHEIGHT_SETTING = "initial_window_height"
PRETTYUSER_SETTING = "pretty_user_lists"
DOLINKS_SETTING = "urls_to_links_in_chat"
TITLE_ACTIVE_WINDOW_SETTING = "set_title_to_active_window"
SAVE_LOGS_BY_NETWORK = "use_network_for_chat_log_filenames"
DISPLAY_PLUGIN_ERRORS_SETTING = "display_plugin_load_errors"
LOAD_THEME_ICONS_SETTING = "use_theme_icons"
PROFANITY_FILTER_SETTING = "filter_profanity"
STRIP_IRC_COLORS_SETTING = "strip_irc_colors"
SYSTEM_TRAY_SETTING = "system_tray_icon"
SYSTEM_TRAY_FLASH_SETTING = "system_tray_flash"
PLUGINS_ENABLED_SETTING = "execute_plugin_events"
ENABLE_LIST_SETTING = "enable_channel_list_button"
ENABLE_SPELL_CHECK = "enable_spell_checking"
SPELL_CHECK_LANGUAGE = "spell_check_language"
AUTO_SAVE_CHAT_LOGS = "save_chat_logs_on_exit"
AUTOCOMPLETE_COMMANDS = "enable_command_autocomplete"
AUTOCOMPLETE_ENTITIES = "enable_nick_channel_autocomplete"
HIGHLIGHT_NICK_MESSAGE = "enable_nick_message_highlight"
STATUS_BAR_SETTING = "enable_status_bar"
TOPIC_TITLE_SETTING = "display_channel_topic_in_title"
THEME_SETTING = "theme"

LOAD_LOG_SETTING = "automatically_load_log"
LOAD_LOG_SIZE = "log_display_size"

EDITOR_FONT_SETTING = "font"
EDITOR_WORD_WRAP_SETTING = "word_wrap"
EDITOR_SPACES_TAB_SETTING = "use_spaces_instead_of_tab_for_indent"
EDITOR_NUMBER_OF_SPACES = "number_of_spaces_to_indent"
EDITOR_FIND_ON_TOP = "find_window_always_on_top"

DEFAULT_WINDOW_TITLE = f" {APPLICATION_NAME}"
FIND_WINDOW_TITLE = "Find"
FIND_REPLACE_WINDOW_TITLE = "Find and replace"

IRC_00 = "#FFFFFF"
IRC_01 = "#000000"
IRC_02 = "#0000FF"
IRC_03 = "#008000"
IRC_04 = "#FF0000"
IRC_05 = "#A52A2A"
IRC_06 = "#800080"
IRC_07 = "#FFA500"
IRC_08 = "#FFFF00"
IRC_09 = "#90EE90"
IRC_10 = "#008080"
IRC_11 = "#00FFFF"
IRC_12 = "#ADD8E6"
IRC_13 = "#FFC0CB"
IRC_14 = "#808080"
IRC_15 = "#D3D3D3"

# Graphics

MDI_BACKGROUND = ":/background.png"
ERK_LOG_WATERMARK = ":/logbg.png"
ERK_BANNER_LOGO = ":/logo.png"
ERK_LOG_BANNER = ":/banner.png"
QT_IMAGE = ":/qt.png"
PYTHON_IMAGE = ":/python.png"
TWISTED_IMAGE = ":/twisted.png"
ICONS8_IMAGE = ":/icons8.png"

KOD_LOGO_IMAGE = ":/kodlogo.png"

# Icons

ERK_ICON = ":/erk.png"
SERVER_ICON = ":/server.png"
NETWORK_ICON = ":/network.png"
USER_WINDOW_ICON = ":/userwindow.png"
CHANNEL_WINDOW_ICON = ":/channelwindow.png"
LOCKED_ICON = ":/locked.png"
CASCADE_ICON = ":/cascade.png"
TILE_ICON = ":/tile.png"
EXIT_ICON = ":/exit.png"
DISCONNECT_ICON = ":/disconnect.png"
USER_ICON = ":/user.png"
TOOLBAR_DISCONNECT_ICON = ":/toolbardisconnect.png"
BAN_ICON = ":/ban.png"
MODERATED_ICON = ":/moderated.png"
UNKNOWN_ICON = ":/unknown.png"
SAVE_ICON = ":/save.png"
CLIPBOARD_ICON = ":/clipboard.png"
FONT_ICON = ":/font.png"
PLUS_ICON = ":/plus.png"
MINUS_ICON = ":/minus.png"
NEW_WINDOW_ICON = ":/newwindow.png"
WHOIS_ICON = ":/whois.png"
LOG_ICON = ":/log.png"
KICK_ICON = ":/kick.png"
PLUGIN_ICON = ":/plugin.png"
EDIT_ICON = ":/edit.png"
SAVEAS_ICON = ":/saveas.png"
OPEN_ICON = ":/open.png"
SELECTALL_ICON = ":/selectall.png"
CUT_ICON = ":/cut.png"
COPY_ICON = ":/copy.png"
UNDO_ICON = ":/undo.png"
REDO_ICON = ":/redo.png"
INDENT_ICON = ":/indent.png"
WRAP_ICON = ":/wrap.png"
COMMAND_ICON = ":/command.png"
RESTART_ICON = ":/restart.png"
NEWFILE_ICON = ":/newfile.png"
LOAD_ICON = ":/load.png"
PACKAGE_ICON = ":/package.png"
PUBLIC_ICON = ":/public.png"
PRIVATE_ICON = ":/private.png"
OPERATOR_ICON = ":/operator.png"
VOICED_ICON = ":/voiced.png"
NORMAL_ICON = ":/normal.png"
ABOUT_ICON = ":/about.png"
IGNORE_ICON = ":/ignore.png"
UNIGNORE_ICON = ":/unignore.png"
EDIT_FILE_ICON = ":/editfile.png"
INDIVIDUAL_PACKAGE_ICON = ":/ipackage.png"
KICKBAN_ICON = ":/kickban.png"
USERS_ICON = ":/users.png"
WINDOW_ICON = ":/window.png"
ENABLE_ICON = ":/enable.png"
DISABLE_ICON = ":/disable.png"
LIST_ICON = ":/list.png"
DISPLAY_ICON = ":/display.png"
SPELL_ICON = ":/spell.png"
CONNECTED_ICON = ":/connected.png"
THEME_ICON = ":/theme.png"
LINK_ICON = ":/link.png"
CONSOLE_ICON = ":/console.png"
NOCONSOLE_ICON = ":/hide.png"
COLOR_ICON = ":/colors.png"
FILE_ICON = ":/file.png"
GEARS_ICON = ":/gears.png"
PYICON_ICON = ":/pyicon.png"
QTICON_ICON = ":/qticon.png"
PYQT_ICON = ":/pyqt.png"
OPEN_SOURCE_ICON = ":/opensource.png"
AUTOCOMPLETE_ICON = ":/autocomplete.png"
SETTINGS_ICON = ":/settings.png"
FLASH_ICON = ":/flash.png"
TRAY_ICON = ":/tray.png"

MINIMIZE_ICON = ":/minimize.png"
MAXIMIZE_ICON = ":/maximize.png"

OPERATOR_MENU_TITLE = f"""
<table style="width: 100%;" border="0"><tbody><tr>
  <td style="text-align: left; vertical-align: middle;"><img src=\"{OPERATOR_ICON}\" width=\"22\" height=\"22\">&nbsp;</td>
  <td style="text-align: left; vertical-align: middle;"><b>!USER!!SPACER!</b></td>
</tr></tbody></table>
"""

VOICED_MENU_TITLE = f"""
<table style="width: 100%;" border="0"><tbody><tr>
  <td style="text-align: left; vertical-align: middle;"><img src=\"{VOICED_ICON}\" width=\"22\" height=\"22\">&nbsp;</td>
  <td style="text-align: left; vertical-align: middle;"><b>!USER!!SPACER!</b></td>
</tr></tbody></table>
"""

USER_MENU_TITLE = f"""
<table style="width: 100%;" border="0"><tbody><tr>
  <td style="text-align: left; vertical-align: middle;"><img src=\"{USER_ICON}\" width=\"22\" height=\"22\">&nbsp;</td>
  <td style="text-align: left; vertical-align: middle;"><b>!USER!!SPACER!</b></td>
</tr></tbody></table>
"""

# Plugins

# Event names
EVENT_LOAD        = "load"
EVENT_UNLOAD      = "unload"
EVENT_CONNECTED     = "server_connected"
EVENT_DISCONNECTED    = "server_disconnected"
EVENT_REGISTERED    = "server_registered"
EVENT_PUBLIC      = "message_public"
EVENT_PRIVATE     = "message_private"
EVENT_NOTICE      = "message_notice"
EVENT_ACTION      = "message_action"
EVENT_JOIN        = "channel_join"
EVENT_PART        = "channel_part"
EVENT_MODE        = "server_mode"
EVENT_QUIT        = "server_quit"
EVENT_TOPIC       = "channel_topic"
EVENT_INVITE      = "channel_invite"
EVENT_MOTD        = "server_motd"
EVENT_MENU        = "menu"
EVENT_TICK        = "tick"
EVENT_INPUT       = "input"
EVENT_RAW       = "server_raw"
EVENT_KICK        = "channel_kick"

PLUGIN_CLASS = '%CLASS%'
PLUGIN_NAME = '%NAME%'
PLUGIN_VERSION = '%VERSION%'
PLUGIN_DESCRIPTION = '%DESCRIPTION%'
PLUGIN_TRIGGER = '%COMMAND%'
PLUGIN_OPTIONS = '%OPTIONS%'

PLUGIN_ARGCOUNT = '%ARGCOUNT%'

TEMPLATE_MODULE_LOAD = "from erk import Plugin,Shared"

INDENT_SYMBOL = "%_I_%"

PRIVATE_COMMAND_SKELETON = f"""
class %CLASS%(Plugin):

%_I_%def __init__(self):
%_I_%%_I_%self.name = "%NAME%"
%_I_%%_I_%self.version = "%VERSION%"
%_I_%%_I_%self.description = "%DESCRIPTION%"
%_I_%%_I_%%OPTIONS%

%_I_%%_I_%self.command = "%COMMAND%"
%_I_%%_I_%self.arguments = %ARGCOUNT%

%_I_%# Executed when a public message is received
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The user who sent the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PRIVATE}(self,serverID,user,message):
%_I_%%_I_%tokens = shlex.split(message)
%_I_%%_I_%if len(tokens)>0 and tokens[0].lower()==self.command.lower():
%_I_%%_I_%%_I_%tokens.pop(0)

%_I_%%_I_%%_I_%# tokens = a list of arguments passed to the command

%_I_%%_I_%%_I_%if len(tokens)!=self.arguments:
%_I_%%_I_%%_I_%%_I_%# Too many/too few arguments
%_I_%%_I_%%_I_%%_I_%return

%_I_%%_I_%%_I_%# Command functionality goes here

"""

PUBLIC_COMMAND_SKELETON = f"""
class %CLASS%(Plugin):

%_I_%def __init__(self):
%_I_%%_I_%self.name = "%NAME%"
%_I_%%_I_%self.version = "%VERSION%"
%_I_%%_I_%self.description = "%DESCRIPTION%"
%_I_%%_I_%%OPTIONS%

%_I_%%_I_%self.command = "%COMMAND%"
%_I_%%_I_%self.arguments = %ARGCOUNT%

%_I_%# Executed when a public message is received
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               user (str) - The user who sent the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PUBLIC}(self,serverID,channel,user,message):
%_I_%%_I_%tokens = shlex.split(message)
%_I_%%_I_%if len(tokens)>0 and tokens[0].lower()==self.command.lower():
%_I_%%_I_%%_I_%tokens.pop(0)

%_I_%%_I_%%_I_%# tokens = a list of arguments passed to the command

%_I_%%_I_%%_I_%if len(tokens)!=self.arguments:
%_I_%%_I_%%_I_%%_I_%# Too many/too few arguments
%_I_%%_I_%%_I_%%_I_%return

%_I_%%_I_%%_I_%# Command functionality goes here
"""

COMMAND_SKELETON = f"""
class %CLASS%(Plugin):

%_I_%def __init__(self):
%_I_%%_I_%self.name = "%NAME%"
%_I_%%_I_%self.version = "%VERSION%"
%_I_%%_I_%self.description = "%DESCRIPTION%"
%_I_%%_I_%%OPTIONS%

%_I_%%_I_%self.command = "%COMMAND%"
%_I_%%_I_%self.arguments = %ARGCOUNT%

%_I_%# Executed when the text is inputted into the client
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               source (str) - The window the client input text into
%_I_%#               text (str) - The input text
%_I_%def {EVENT_INPUT}(self,serverID,source,text):
%_I_%%_I_%tokens = shlex.split(text)
%_I_%%_I_%if len(tokens)>0 and tokens[0].lower()==self.command.lower():
%_I_%%_I_%%_I_%tokens.pop(0)

%_I_%%_I_%%_I_%if len(tokens)!=self.arguments:
%_I_%%_I_%%_I_%%_I_%# Too many/too few arguments
%_I_%%_I_%%_I_%%_I_%return

%_I_%%_I_%%_I_%# serverID = the ID of the server
%_I_%%_I_%%_I_%# source = the name of the window the command was input into
%_I_%%_I_%%_I_%# tokens = a list of arguments passed to the command

%_I_%%_I_%%_I_%# Command functionality goes here

%_I_%%_I_%%_I_%# Return a true value so the inputted text isn't
%_I_%%_I_%%_I_%# sent to the IRC server as chat
%_I_%%_I_%%_I_%return True
"""

PLUGIN_SKELETON = f"""
class %CLASS%(Plugin):

%_I_%def __init__(self):
%_I_%%_I_%self.name = "%NAME%"
%_I_%%_I_%self.version = "%VERSION%"
%_I_%%_I_%self.description = "%DESCRIPTION%"
%_I_%%_I_%%OPTIONS%

%_I_%# =================
%_I_%# | CLIENT EVENTS |
%_I_%# =================

%_I_%# Executed as soon as the plugin is loaded
%_I_%def {EVENT_LOAD}(self):
%_I_%%_I_%pass

%_I_%# Executed when the client exits
%_I_%def {EVENT_UNLOAD}(self):
%_I_%%_I_%pass

%_I_%# Executed when the plugin's name is clicked in
%_I_%# the "Plugins" menu
%_I_%def {EVENT_MENU}(self):
%_I_%%_I_%pass

%_I_%# Executes roughly once per second
%_I_%# {EVENT_TICK} is executed once for each connected server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               uptime (int) - The uptime of the client, in seconds 
%_I_%def {EVENT_TICK}(self,serverID,uptime):
%_I_%%_I_%pass

%_I_%# Executed when the text is inputted into the client
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               source (str) - The window the client input text into
%_I_%#               text (str) - The input text
%_I_%def {EVENT_INPUT}(self,serverID,source,text):
%_I_%%_I_%pass

%_I_%# ==============
%_I_%# | IRC EVENTS |
%_I_%# ==============

%_I_%# Executed when the client connects to an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server connected to
%_I_%def {EVENT_CONNECTED}(self,serverID):
%_I_%%_I_%pass

%_I_%# Executed when the client disconnected from an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server disconnected from
%_I_%#               reason (str) - The reason for the disconnection
%_I_%def {EVENT_DISCONNECTED}(self,serverID,reason):
%_I_%%_I_%pass

%_I_%# Executed when the client registers with an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server registered with
%_I_%def {EVENT_REGISTERED}(self,serverID):
%_I_%%_I_%pass

%_I_%# Executed when the client receives the MOTD from a server
%_I_%# Arguments:    serverID (str) - The ID of the server the part occurred on
%_I_%#               motd (list) - A list of strings containing the MOTD
%_I_%def {EVENT_MOTD}(self,serverID,motd):
%_I_%%_I_%pass

%_I_%# Executed when the client receives a public message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PUBLIC}(self,serverID,channel,user,message):
%_I_%%_I_%pass

%_I_%# Executed when the client receives a private message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PRIVATE}(self,serverID,user,message):
%_I_%%_I_%pass

%_I_%# Executed when the client receives a notice
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_NOTICE}(self,serverID,channel,user,message):
%_I_%%_I_%pass

%_I_%# Executed when the client receives CTCP action message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_ACTION}(self,serverID,channel,user,message):
%_I_%%_I_%pass

%_I_%# Executed when a user joins a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server the join occurred on
%_I_%#               channel (str) - The channel joined
%_I_%#               user (str) - The user joining
%_I_%def {EVENT_JOIN}(self,serverID,channel,user):
%_I_%%_I_%pass

%_I_%# Executed when a user leaves a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server the part occurred on
%_I_%#               channel (str) - The channel left
%_I_%#               user (str) - The user leaving
%_I_%def {EVENT_PART}(self,serverID,channel,user):
%_I_%%_I_%pass

%_I_%# Executed when the client receives a channel invite
%_I_%# Arguments:    serverID (str) - The ID of the server the invite occurred on
%_I_%#               channel (str) - The channel invited to
%_I_%#               user (str) - The user who sent the invite
%_I_%def {EVENT_INVITE}(self,serverID,channel,user):
%_I_%%_I_%pass

%_I_%# Executed when the topic is changed in a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               channel (str) - The channel that had its topic changed
%_I_%#               user (str) - The user who changed the topic
%_I_%#               topic (str) - The new topic
%_I_%def {EVENT_TOPIC}(self,serverID,channel,user,topic):
%_I_%%_I_%pass

%_I_%# Executed when a user disconnects from the IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               user (str) - The user disconnecting
%_I_%#               message (str) - An optional parting message
%_I_%def {EVENT_QUIT}(self,serverID,user,message):
%_I_%%_I_%pass

%_I_%# Executed when the client receives a mode message
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               mset (bool) - True for setting a mode, False for unsetting
%_I_%#               user (str) - The user who set the mode
%_I_%#               target (str) - The channel or user the mode was set or unset on
%_I_%#               modes (str) - The modes set
%_I_%#               args (list) - Any mode arguments
%_I_%def {EVENT_MODE}(self,serverID,mset,user,target,modes,args):
%_I_%%_I_%pass

%_I_%# Executed when the client receives ANY data from the server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               data (str) - The data sent
%_I_%#
%_I_%def {EVENT_RAW}(self,serverID,data):
%_I_%%_I_%pass

%_I_%# Executed when a user is kicked from a channel
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               channel (str) - The channel the user was kicked from
%_I_%#               user (str) - The user kicked
%_I_%#               kicker (string) - The user who did the kicking
%_I_%#               reason (string) - The optional reason for the kick
%_I_%def {EVENT_KICK}(self,serverID,channel,user,kicker,reason):
%_I_%%_I_%pass
"""

# Objects

class ErkWindow(object):

	def __init__(self,name,server,window,subwindow):
		self.name = name
		self.server = server
		self.window = window
		self.subwindow = subwindow

class ircConnection(object):

	def __init__(self):
		self.irc = None   # IRC connection object
		self.server = None
		self.port = 0

class Whowas(object):

	def __init__(self):

		self.name = ''
		self.username = ''
		self.host = ''
		self.realname = ''

class Whois(object):

	def __init__(self):

		self.name = ''
		self.channels = []
		self.username = ''
		self.host = ''
		self.realname = ''
		self.idle = 0
		self.signedon = ''
		self.server = ''

# Functions

def censorWord(word,punc=True):
	result = ''
	last = '+'
	for letter in word:
		if punc:
			random.shuffle(PROFANITY_SYMBOLS)		
			nl = random.choice(PROFANITY_SYMBOLS)
			while nl == last:
				nl = random.choice(PROFANITY_SYMBOLS)
			last = nl
			result = result + nl
		else:
			result = result + "*"
	return result

def filterProfanityFromText(text,punc=True):
	clean = []
	for word in text.split(' '):
		nopunc = word.translate(str.maketrans("","", string.punctuation))
		if nopunc in PROFANITY:
			word = censorWord(word,punc)
		clean.append(word)
	return ' '.join(clean)

def importThemeResources(theme):
	if theme==USE_NO_THEME_SETTING:
		globals()["erk.resources"] = __import__("erk.resources")
		return

	f = os.path.join(THEMES_DIRECTORY, theme)
	f = os.path.join(f, THEME_RESOURCE_FILE_NAME)
	if not os.path.isfile(f):
			globals()["erk.resources"] = __import__("erk.resources")
			return

	spec = importlib.util.spec_from_file_location("erk.resources", f)
	foo = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(foo)
	globals()["erk.resources"] = foo

def getThemeList():
	themes = []
	for theme in os.listdir(THEMES_DIRECTORY):
			theme = os.path.basename(theme)
			if '.' in theme: continue
			themes.append(theme)
	return themes

def getThemeIcon(theme):
	f = os.path.join(THEMES_DIRECTORY, theme)
	f = os.path.join(f, THEME_ICON_FILE_NAME)
	if not os.path.isfile(f):
			return None
	return f

def getThemeQSS(tfile):
	f = os.path.join(THEMES_DIRECTORY, tfile)
	f = os.path.join(f, THEME_QSS_FILE_NAME)
	if not os.path.isfile(f):
			return None

	tf = open(f,"r")
	return tf.read()

def getThemeJSON(tfile):
	f = os.path.join(THEMES_DIRECTORY, tfile)
	f = os.path.join(f, THEME_JSON_FILE_NAME)
	if not os.path.isfile(f):
			return []

	with open(f, "r") as read_json:
		data = json.load(read_json)
		return [data,f]

def installThemeFromZip(filename,password=None):
	if os.path.isfile(filename):
		 THEMEZIP = filename
	else:
		THEMEZIP = os.path.join(INSTALL_DIRECTORY, filename)
		if not os.path.isfile(THEMEZIP):
			# zip file not found
			return False
	
	with ZipFile(THEMEZIP,"r") as zip:
		zip.extractall(path=THEMES_DIRECTORY,pwd=password)
	return True

def installPluginFromZip(filename,password=None):
	if os.path.isfile(filename):
		 PLUGZIP = filename
	else:
		PLUGZIP = os.path.join(INSTALL_DIRECTORY, filename)
		if not os.path.isfile(PLUGZIP):
			# zip file not found
			return False
	
	with ZipFile(PLUGZIP,"r") as zip:
		zip.extractall(path=PLUGIN_DIRECTORY,pwd=password)
	return True

def get_ignore():
	if os.path.isfile(IGNORE_FILE):
		with open(IGNORE_FILE, "r") as read_ignore:
			data = json.load(read_ignore)
			return data
	else:
		return []

def save_ignore(data):
	with open(IGNORE_FILE, "w") as write_data:
		json.dump(data, write_data, indent=4, sort_keys=True)

def restart_program():
	python = sys.executable
	os.execl(python, python, * sys.argv)

def restart_program_no_arg():
	python = sys.executable
	sys.argv.pop()
	os.execl(python, python, * sys.argv)


def get_editor_settings():
	if os.path.isfile(EDITOR_SETTINGS_FILE):
		with open(EDITOR_SETTINGS_FILE, "r") as read_settings:
			data = json.load(read_settings)
			return data
	else:
		si = {
			EDITOR_FONT_SETTING: "Consolas,10,-1,5,50,0,0,0,0,0,Regular",
			EDITOR_WORD_WRAP_SETTING: False,
			EDITOR_SPACES_TAB_SETTING: True,
			EDITOR_NUMBER_OF_SPACES: 2,
			EDITOR_FIND_ON_TOP: True,

		}
		return si

def save_editor_settings(data):
	with open(EDITOR_SETTINGS_FILE, "w") as write_data:
		json.dump(data, write_data, indent=4, sort_keys=True)

def timestamp_to_date(ts):
	dt_object = datetime.fromtimestamp(int(ts))
	return dt_object.strftime("%m/%d/%Y, %H:%M:%S")

def makeWhoisPretty(w):
	sot = timestamp_to_date(w.signedon)
	t = f"""<b>Nickname:</b> {w.name}<br>
<b>Username:</b> {w.username}<br>
<b>Real Name:</b> {w.realname}<br>
<b>Host:</b> {w.host}<br>
<b>Connected to:</b> {w.server}<br>
<b>Signed on:</b> {sot}<br>
<b>Idle:</b> {w.idle} seconds<br>
<b>Channels:</b> {', '.join(w.channels)}"""
	return t

def makeWhowasPretty(w):
	t = f"""<b>{w.name}</b><br>
<b>Username:</b> {w.username}<br>
<b>Real Name:</b> {w.realname}<br>
<b>Host:</b> {w.host}"""
	return t

def cmdHelp():
	h = [
		f"<u>{APPLICATION_NAME} {APPLICATION_VERSION} Command Help</u>",
		"/help - <i>Displays command help</i>",
		"/msg TARGET MESSAGE - <i>Sends MESSAGE to TARGET</i>",
		"/notice TARGET MESSAGE - <i>Sends a notice to TARGET</i>",
		"/me MESSAGE - <i>Sends a CTCP action message</i>",
		"/join CHANNEL [KEY] - <i>Joins a channel</i>",
		"/part [CHANNEL] - <i>Leaves a channel</i>",
		"/away [MESSAGE] - <i>Sets you as \"away\"</i>",
		"/back - <i>Sets you as \"back\"</i>",
		"/invite USER [CHANNEL] - <i>Sends a channel invitation</i>",
		"/kick [CHANNEL] USER [REASON] - <i>Kicks a user from a channel</i>",
		"/topic [CHANNEL] NEW_TOPIC - <i>Attempts to set a channel's topic</i>",
		"/oper USERNAME PASSWORD - <i>Attempts to log into an IRCop account</i>",
		"/whowas USER - <i>Attempts to retrieve information about a user</i>",
		"/quit [MESSAGE] - <i>Disconnects from an IRC server</i>",
		"/nick NEW_NICKNAME - <i>Changes to a new nickname</i>",
		"/color FOREGROUND [BACKGROUND] TEXT - <i>Formats a message with mIRC color codes",
	]
	return h

INPUT_COMMANDS = {
	"/help": "/help",
	"/msg": "/msg ",
	"/notice": "/notice ",
	"/me": "/me ",
	"/join": "/join ",
	"/part": "/part ",
	"/away": "/away ",
	"/back": "/back",
	"/invite": "/invite ",
	"/kick": "/kick ",
	"/topic": "/topic ",
	"/oper": "/oper ",
	"/whowas": "/whowas ",
	"/quit": "/quit ",
	"/nick": "/nick ",
	"/color": "/color ",
}

def convertSeconds(seconds):
	h = seconds//(60*60)
	m = (seconds-h*60*60)//60
	s = seconds-(h*60*60)-(m*60)
	return [h, m, s]

def is_integer(n):
	try:
		int(n)
	except ValueError:
		return False
	return True

def save_autojoin_channels(server,chans):
	AUTOJOIN_FILE = os.path.join(AUTOJOIN_DIRECTORY, f"{server}.json")
	with open(AUTOJOIN_FILE, "w") as write_data:
		json.dump(chans, write_data, indent=4, sort_keys=True)

def get_autojoins(server):
	AUTOJOIN_FILE = os.path.join(AUTOJOIN_DIRECTORY, f"{server}.json")
	if os.path.isfile(AUTOJOIN_FILE):
		with open(AUTOJOIN_FILE, "r") as read_server:
			data = json.load(read_server)
			return data
	else:
		return []

def save_last_server(host,port,password,ssl):
	sinfo = {
			"host": host,
			"port": port,
			"password": password,
			"ssl": ssl
		}
	with open(LAST_SERVER_INFORMATION_FILE, "w") as write_data:
		json.dump(sinfo, write_data, indent=4, sort_keys=True)

def get_last_server():
	if os.path.isfile(LAST_SERVER_INFORMATION_FILE):
		with open(LAST_SERVER_INFORMATION_FILE, "r") as read_server:
			data = json.load(read_server)
			return data
	else:
		si = {
			"host": '',
			"port": '',
			"password": '',
			"ssl": False
		}
		return si

def get_user(filename=USER_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_user:
			data = json.load(read_user)
			return data
	else:
		si = {
			"nick": DEFAULT_NICKNAME,
			"username": DEFAULT_USERNAME,
			"realname": DEFAULT_IRCNAME,
			"alternate": DEFAULT_ALTERNATIVE,
		}
		return si

def save_user(user,filename=USER_FILE):
	with open(filename, "w") as write_data:
		json.dump(user, write_data, indent=4, sort_keys=True)

# SETTINGS_FILE

def saveSettings(settings,filename=SETTINGS_FILE):
	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def loadSettings(filename=SETTINGS_FILE):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)
			return data
	else:
		s = {
			TIMESTAMP_SETTING: True,
			UPTIME_SETTING: True,
			KEEPALIVE_SETTING: True,
			INVITE_SETTING: False,
			PRIVATEWINDOW_SETTING: True,
			INITIALWIDTH_SETTING: INITIAL_WINDOW_WIDTH,
			INITIALHEIGHT_SETTING: INITIAL_WINDOW_HEIGHT,
			PRETTYUSER_SETTING: True,
			DOLINKS_SETTING: True,
			TITLE_ACTIVE_WINDOW_SETTING: True,
			SAVE_LOGS_BY_NETWORK: True,
			DISPLAY_PLUGIN_ERRORS_SETTING: True,
			PLUGINS_ENABLED_SETTING: True,
			ENABLE_LIST_SETTING: False,
			AUTO_SAVE_CHAT_LOGS: True,
			ENABLE_SPELL_CHECK: True,
			SPELL_CHECK_LANGUAGE: "en",
			AUTOCOMPLETE_COMMANDS: True,
			AUTOCOMPLETE_ENTITIES: True,
			HIGHLIGHT_NICK_MESSAGE: True,
			STATUS_BAR_SETTING: False,
			THEME_SETTING: USE_NO_THEME_SETTING,
			LOAD_THEME_ICONS_SETTING: True,
			PROFANITY_FILTER_SETTING: False,
			TOPIC_TITLE_SETTING: True,
			STRIP_IRC_COLORS_SETTING: False,
			SYSTEM_TRAY_SETTING: False,
			SYSTEM_TRAY_FLASH_SETTING: True,
			LOAD_LOG_SETTING: True,
			LOAD_LOG_SIZE: MAX_LOG_SIZE_DEFAULT,
		}
		return s

def saveDisplay(settings,filename=DISPLAY_CONFIGURATION):
	with open(filename, "w") as write_data:
		json.dump(settings, write_data, indent=4, sort_keys=True)

def loadDisplay(filename=DISPLAY_CONFIGURATION):
	if os.path.isfile(filename):
		with open(filename, "r") as read_settings:
			data = json.load(read_settings)
			return data
	else:
		s = {
			"font": "Consolas,10,-1,5,50,0,0,0,0,0,Regular",
			"system": "#FF9C00",
			"self": "#FF0000",
			"user": "#00007F",
			"action": "#009300",
			"notice": "#9C009C",
			"error": "#FF0000",
			"highlight": "#76448A",
			"link": "#0000FF",
			"new-chat-divider-text": "#000000",
			"new-chat-divider": "#FFFFFF",
			"banner-text": "",
		}
		return s

def encodeLogName(serverid,name):
	serverid = serverid.replace(":","-")
	return f"{serverid}-{name}.json"

def saveLog(serverid,name,logs):
	f = encodeLogName(serverid,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	with open(logfile, "w") as writelog:
		json.dump(logs, writelog, indent=4, sort_keys=True)

def appendLog(serverid,name,logs):
	f = encodeLogName(serverid,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	slog = loadLog(serverid,name)
	for e in logs:
		slog.append(e)

	with open(logfile, "a") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

def loadLog(serverid,name):
	f = encodeLogName(serverid,name)
	logfile = os.path.join(LOG_DIRECTORY,f)

	if os.path.isfile(logfile):
		with open(logfile, "r") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

def encodeWindowLink(serverid,user):
	l = f"{serverid}___{user}"
	l = l.replace(":","&")
	return f"{l}"

def decodeWindowLink(link):
	l = link.replace("&",":")
	return l.split("___")

def systemTextDisplay(text,max,foreground):
	user = SYSTEM_MESSAGE_DISPLAY_SYMBOL
	msg = SYSTEM_MESSAGE_TEMPLATE
	msg = msg.replace('!COLOR!',foreground)
	msg = msg.replace('!USER!',user)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def pad_nick(nick,size):
	x = size - len(nick)
	if x<0 : x = 0
	y = '&nbsp;'*x
	return f"{y}{nick}"

def remove_html_markup(s):
	tag = False
	quote = False
	out = ""

	for c in s:
			if c == '<' and not quote:
				tag = True
			elif c == '>' and not quote:
				tag = False
			elif (c == '"' or c == "'") and tag:
				quote = not quote
			elif not tag:
				out = out + c

	return out

def inject_www_links(txt):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
	for u in urls:
		u = re.sub('<[^<]+?>', '', u)
		link = f"<a href=\"{u}\"><span style=\"text-decoration: underline; font-weight: bold; color: {LINK_COLOR}\">{u}</span></a>"
		txt = txt.replace(u,link)
	return txt

def chat_display_highlight(user,text,max,dolink,namecolor,foreground):
	text = remove_html_markup(text)
	text = convert_irc_color_to_html(text)
	user = pad_nick(user,max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',"<font color=\"" + foreground + "\">" + text + "</font>")

	return msg

def chat_display(user,text,max,dolink,namecolor,dobold=False):
	text = remove_html_markup(text)
	if dobold: text = "<b>"+text+"</b>"
	text = convert_irc_color_to_html(text)
	user = pad_nick(user,max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def chat_display_no_strip(user,text,max,dolink,namecolor):
	#text = remove_html_markup(text)
	user = pad_nick(user,max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def whois_display(text,max,namecolor):
	user = pad_nick("WHOIS",max)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def whowas_display(text,max,namecolor):
	user = pad_nick("WHOWAS",max)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def motd_display(text,max,dolink,namecolor):
	user = pad_nick("MOTD",max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def log_chat_display(user,text,max,dolink,namecolor):
	text = remove_html_markup(text)
	#user = pad_nick(user,max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def action_display(user,text,dolink,namecolor,highlight,highlightcolor,nick):
	text = remove_html_markup(text)
	text = convert_irc_color_to_html(text)
	if dolink: text = inject_www_links(text)
	if highlight:
		text = text.replace(nick,f"</i><font color=\"{highlightcolor}\"><b>{nick}</b></font><i>")

	msg = ACTION_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def notice_display(user,text,max,dolink,namecolor):
	text = remove_html_markup(text)
	text = convert_irc_color_to_html(text)
	user = pad_nick(user,max)
	if dolink: text = inject_www_links(text)
	msg = CHAT_MESSAGE_TEMPLATE.replace('!USER!',user)
	msg = msg.replace('!COLOR!',namecolor)
	msg = msg.replace('!MESSAGE!',text)

	return msg

def convertLogToPlaintext(log):
	d = []
	for l in log:
		time = l[LOG_TIMESTAMP]
		text = l[LOG_TEXT]

		text = text.replace("!TIMESTAMP!","")
		text = remove_html_markup(text)
		text = text.replace("\n","")
		text = text.replace("&nbsp;","")
		text = text.strip()
		text = re.sub("[\t ]{2,}", "\t", text)
		text = text.replace("\t",":")
		d.append(f"{time} {text}")
	return "\n".join(d)

def convertLogToHtml(log):
	d = []
	for l in log:
		time = l[LOG_TIMESTAMP]
		text = l[LOG_TEXT]

		text = text.replace("!TIMESTAMP!","")
		d.append(f"{time} {text}")
	return "\n".join(d)

def plugin_color(text,fore,back=None):
	if fore<0: return text
	if fore>15: return text
	if back!=None:
		if back<0: return text
		if back>15: return text

	if back!=None:
		fc = str(fore)
		bc = str(back)
		if len(fc)==1: fc = "0"+fc
		if len(bc)==1: bc = "0"+bc
		return chr(3)+fc+","+bc+text+chr(3)
	else:
		fc = str(fore)
		if len(fc)==1: fc = "0"+fc
		return chr(3)+fore+text+chr(3)

def irc_color_full(fore,back,text):

	if fore==0: fore=IRC_00
	if fore==1: fore=IRC_01
	if fore==2: fore=IRC_02
	if fore==3: fore=IRC_03
	if fore==4: fore=IRC_04
	if fore==5: fore=IRC_05
	if fore==6: fore=IRC_06
	if fore==7: fore=IRC_07
	if fore==8: fore=IRC_08
	if fore==9: fore=IRC_09
	if fore==10: fore=IRC_10
	if fore==11: fore=IRC_11
	if fore==12: fore=IRC_12
	if fore==13: fore=IRC_13
	if fore==14: fore=IRC_14
	if fore==15: fore=IRC_15

	if back==0: back=IRC_00
	if back==1: back=IRC_01
	if back==2: back=IRC_02
	if back==3: back=IRC_03
	if back==4: back=IRC_04
	if back==5: back=IRC_05
	if back==6: back=IRC_06
	if back==7: back=IRC_07
	if back==8: back=IRC_08
	if back==9: back=IRC_09
	if back==10: back=IRC_10
	if back==11: back=IRC_11
	if back==12: back=IRC_12
	if back==13: back=IRC_13
	if back==14: back=IRC_14
	if back==15: back=IRC_15

	return f"<div style=\"color: {fore}; background-color: {back}\">" + text + "</div>"

def irc_color(fore,text):

	if fore==0: fore=IRC_00
	if fore==1: fore=IRC_01
	if fore==2: fore=IRC_02
	if fore==3: fore=IRC_03
	if fore==4: fore=IRC_04
	if fore==5: fore=IRC_05
	if fore==6: fore=IRC_06
	if fore==7: fore=IRC_07
	if fore==8: fore=IRC_08
	if fore==9: fore=IRC_09
	if fore==10: fore=IRC_10
	if fore==11: fore=IRC_11
	if fore==12: fore=IRC_12
	if fore==13: fore=IRC_13
	if fore==14: fore=IRC_14
	if fore==15: fore=IRC_15

	return f"<div style=\"color: {fore};\">" + text + "</div>"

def convert_irc_color_to_html(text):

	html_tag = "font"

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		if int(fore)==0: foreground = str(IRC_00)
		if int(fore)==1: foreground = str(IRC_01)
		if int(fore)==2: foreground = str(IRC_02)
		if int(fore)==3: foreground = str(IRC_03)
		if int(fore)==4: foreground = str(IRC_04)
		if int(fore)==5: foreground = str(IRC_05)
		if int(fore)==6: foreground = str(IRC_06)
		if int(fore)==7: foreground = str(IRC_07)
		if int(fore)==8: foreground = str(IRC_08)
		if int(fore)==9: foreground = str(IRC_09)
		if int(fore)==10: foreground = str(IRC_10)
		if int(fore)==11: foreground = str(IRC_11)
		if int(fore)==12: foreground = str(IRC_12)
		if int(fore)==13: foreground = str(IRC_13)
		if int(fore)==14: foreground = str(IRC_14)
		if int(fore)==15: foreground = str(IRC_15)

		if int(back)==0: background = str(IRC_00)
		if int(back)==1: background = str(IRC_01)
		if int(back)==2: background = str(IRC_02)
		if int(back)==3: background = str(IRC_03)
		if int(back)==4: background = str(IRC_04)
		if int(back)==5: background = str(IRC_05)
		if int(back)==6: background = str(IRC_06)
		if int(back)==7: background = str(IRC_07)
		if int(back)==8: background = str(IRC_08)
		if int(back)==9: background = str(IRC_09)
		if int(back)==10: background = str(IRC_10)
		if int(back)==11: background = str(IRC_11)
		if int(back)==12: background = str(IRC_12)
		if int(back)==13: background = str(IRC_13)
		if int(back)==14: background = str(IRC_14)
		if int(back)==15: background = str(IRC_15)

		t = f"\x03{fore},{back}"
		r = f"<{html_tag} style=\"color: {foreground}; background-color: {background}\">"
		text = text.replace(t,r)

	text = text.replace("\x0310",f"<{html_tag} style=\"color: {IRC_10};\">")
	text = text.replace("\x0311",f"<{html_tag} style=\"color: {IRC_11};\">")
	text = text.replace("\x0312",f"<{html_tag} style=\"color: {IRC_12};\">")
	text = text.replace("\x0313",f"<{html_tag} style=\"color: {IRC_13};\">")
	text = text.replace("\x0314",f"<{html_tag} style=\"color: {IRC_14};\">")
	text = text.replace("\x0315",f"<{html_tag} style=\"color: {IRC_15};\">")

	text = text.replace("\x0300",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x0301",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x0302",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x0303",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x0304",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x0305",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x0306",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x0307",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x0308",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x0309",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x030",f"<{html_tag} style=\"color: {IRC_00};\">")
	text = text.replace("\x031",f"<{html_tag} style=\"color: {IRC_01};\">")
	text = text.replace("\x032",f"<{html_tag} style=\"color: {IRC_02};\">")
	text = text.replace("\x033",f"<{html_tag} style=\"color: {IRC_03};\">")
	text = text.replace("\x034",f"<{html_tag} style=\"color: {IRC_04};\">")
	text = text.replace("\x035",f"<{html_tag} style=\"color: {IRC_05};\">")
	text = text.replace("\x036",f"<{html_tag} style=\"color: {IRC_06};\">")
	text = text.replace("\x037",f"<{html_tag} style=\"color: {IRC_07};\">")
	text = text.replace("\x038",f"<{html_tag} style=\"color: {IRC_08};\">")
	text = text.replace("\x039",f"<{html_tag} style=\"color: {IRC_09};\">")

	text = text.replace("\x03",f"</{html_tag}>")

	# close font tags
	if f"<{html_tag} style=" in text:
		if not f"</{html_tag}>" in text: text = text + f"</{html_tag}>"

	out = []
	indiv = False
	for w in text.split(' '):

		if indiv:
			if w==f"<{html_tag}":
				out.append(f"</{html_tag}>")

		if w==f"<{html_tag}": indiv = True
		if w==f"</{html_tag}>": indiv = False

		out.append(w)

	text = ' '.join(out)

	# other format tags
	fout = ''
	inbold = False
	initalic = False
	inunderline = False
	for l in text:
		if l=="\x02":
			inbold = True
			fout = fout + "<b>"
			continue
		if l=="\x1D":
			initalic = True
			fout = fout + "<i>"
			continue
		if l=="\x1F":
			inunderline = True
			fout = fout + "<u>"
			continue

		if l=="\x0F":
			if inbold:
				fout = fout + "</b>"
				inbold = False
			if initalic:
				fout = fout + "</i>"
				initalic = False
			if inunderline:
				fout = fout + "</u>"
				inunderline = False
			continue

		fout = fout + l

	if inbold: fout = fout + "</b>"
	if initalic: fout = fout + "</i>"
	if inunderline: fout = fout + "</u>"

	text = fout

	return text



LOAD_EVENT_TEMPLATE = f"""%_I_%# Executed as soon as the plugin is loaded
%_I_%def {EVENT_LOAD}(self):
%_I_%%_I_%pass"""

UNLOAD_EVENT_TEMPLATE = f"""%_I_%# Executed when the client exits
%_I_%def {EVENT_UNLOAD}(self):
%_I_%%_I_%pass"""

MENU_EVENT_TEMPLATE = f"""%_I_%# Executed when the plugin's name is clicked in
%_I_%# the "Plugins" menu
%_I_%def {EVENT_MENU}(self):
%_I_%%_I_%pass"""

TICK_EVENT_TEMPLATE = f"""%_I_%# Executes roughly once per second
%_I_%# {EVENT_TICK} is executed once for each connected server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               uptime (int) - The uptime of the client, in seconds 
%_I_%def {EVENT_TICK}(self,serverID,uptime):
%_I_%%_I_%pass"""

INPUT_EVENT_TEMPLATE = f"""%_I_%# Executed when the text is inputted into the client
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               source (str) - The window the client input text into
%_I_%#               text (str) - The input text
%_I_%def {EVENT_INPUT}(self,serverID,source,text):
%_I_%%_I_%pass"""

CONNECTED_EVENT_TEMPLATE = f"""%_I_%# Executed when the client connects to an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server connected to
%_I_%def {EVENT_CONNECTED}(self,serverID):
%_I_%%_I_%pass"""

DISCONNECTED_EVENT_TEMPLATE = f"""%_I_%# Executed when the client disconnected from an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server disconnected from
%_I_%#               reason (str) - The reason for the disconnection
%_I_%def {EVENT_DISCONNECTED}(self,serverID,reason):
%_I_%%_I_%pass"""

REGISTERED_EVENT_TEMPLATE = f"""%_I_%# Executed when the client registers with an IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server registered with
%_I_%def {EVENT_REGISTERED}(self,serverID):
%_I_%%_I_%pass"""

MOTD_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives the MOTD from a server
%_I_%# Arguments:    serverID (str) - The ID of the server the part occurred on
%_I_%#               motd (list) - A list of strings containing the MOTD
%_I_%def {EVENT_MOTD}(self,serverID,motd):
%_I_%%_I_%pass"""

PUBLIC_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives a public message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PUBLIC}(self,serverID,channel,user,message):
%_I_%%_I_%pass"""

PRIVATE_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives a private message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_PRIVATE}(self,serverID,user,message):
%_I_%%_I_%pass"""

NOTICE_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives a notice
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_NOTICE}(self,serverID,channel,user,message):
%_I_%%_I_%pass"""

ACTION_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives CTCP action message
%_I_%# Arguments:    serverID (str) - The ID of the server that sent the message
%_I_%#               channel (str) - The channel the message was sent to
%_I_%#               user (str) - The sender of the message
%_I_%#               message (str) - The message
%_I_%def {EVENT_ACTION}(self,serverID,channel,user,message):
%_I_%%_I_%pass"""

JOIN_EVENT_TEMPLATE = f"""%_I_%# Executed when a user joins a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server the join occurred on
%_I_%#               channel (str) - The channel joined
%_I_%#               user (str) - The user joining
%_I_%def {EVENT_JOIN}(self,serverID,channel,user):
%_I_%%_I_%pass"""

PART_EVENT_TEMPLATE = f"""_I_%# Executed when a user leaves a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server the part occurred on
%_I_%#               channel (str) - The channel left
%_I_%#               user (str) - The user leaving
%_I_%def {EVENT_PART}(self,serverID,channel,user):
%_I_%%_I_%pass"""

INVITE_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives a channel invite
%_I_%# Arguments:    serverID (str) - The ID of the server the invite occurred on
%_I_%#               channel (str) - The channel invited to
%_I_%#               user (str) - The user who sent the invite
%_I_%def {EVENT_INVITE}(self,serverID,channel,user):
%_I_%%_I_%pass"""

TOPIC_EVENT_TEMPLATE = f"""%_I_%# Executed when the topic is changed in a channel the client is in
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               channel (str) - The channel that had its topic changed
%_I_%#               user (str) - The user who changed the topic
%_I_%#               topic (str) - The new topic
%_I_%def {EVENT_TOPIC}(self,serverID,channel,user,topic):
%_I_%%_I_%pass"""

QUIT_EVENT_TEMPLATE = f"""%_I_%# Executed when a user disconnects from the IRC server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               user (str) - The user disconnecting
%_I_%#               message (str) - An optional parting message
%_I_%def {EVENT_QUIT}(self,serverID,user,message):
%_I_%%_I_%pass"""

MODE_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives a mode message
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               mset (bool) - True for setting a mode, False for unsetting
%_I_%#               user (str) - The user who set the mode
%_I_%#               target (str) - The channel or user the mode was set or unset on
%_I_%#               modes (str) - The modes set
%_I_%#               args (list) - Any mode arguments
%_I_%def {EVENT_MODE}(self,serverID,mset,user,target,modes,args):
%_I_%%_I_%pass"""

RAW_EVENT_TEMPLATE = f"""%_I_%# Executed when the client receives ANY data from the server
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               data (str) - The data sent
%_I_%#
%_I_%def {EVENT_RAW}(self,serverID,data):
%_I_%%_I_%pass"""

KICK_EVENT_TEMPLATE = f"""%_I_%# Executed when a user is kicked from a channel
%_I_%# Arguments:    serverID (str) - The ID of the server
%_I_%#               channel (str) - The channel the user was kicked from
%_I_%#               user (str) - The user kicked
%_I_%#               kicker (string) - The user who did the kicking
%_I_%#               reason (string) - The optional reason for the kick
%_I_%def {EVENT_KICK}(self,serverID,channel,user,kicker,reason):
%_I_%%_I_%pass"""

PLUGIN_START_TEMPLATE = f"""class MyPluginClass(Plugin):
%_I_%def __init__(self):
%_I_%%_I_%self.name = "Plugin"
%_I_%%_I_%self.version = "1.0"
%_I_%%_I_%self.description = "A plugin."
%_I_%%_I_%self.silent = False
%_I_%%_I_%self.nowindows = False
%_I_%%_I_%self.noirc = False
"""

def strip_color(text):

	html_tag = "font"

	combos = list(combinations(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	combos = list(combinations(["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"],2))
	for c in combos:
		fore = c[0]
		back = c[1]

		t = f"\x03{fore},{back}"
		text = text.replace(t,'')

	text = text.replace("\x0310","")
	text = text.replace("\x0311","")
	text = text.replace("\x0312","")
	text = text.replace("\x0313","")
	text = text.replace("\x0314","")
	text = text.replace("\x0315","")

	text = text.replace("\x0300","")
	text = text.replace("\x0301","")
	text = text.replace("\x0302","")
	text = text.replace("\x0303","")
	text = text.replace("\x0304","")
	text = text.replace("\x0305","")
	text = text.replace("\x0306","")
	text = text.replace("\x0307","")
	text = text.replace("\x0308","")
	text = text.replace("\x0309","")

	text = text.replace("\x030","")
	text = text.replace("\x031","")
	text = text.replace("\x032","")
	text = text.replace("\x033","")
	text = text.replace("\x034","")
	text = text.replace("\x035","")
	text = text.replace("\x036","")
	text = text.replace("\x037","")
	text = text.replace("\x038","")
	text = text.replace("\x039","")

	text = text.replace("\x03","")

	text = text.replace("\x02","")
	text = text.replace("\x1D","")
	text = text.replace("\x1F","")
	text = text.replace("\x0F","")

	return text