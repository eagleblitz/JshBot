import asyncio
import random
import socket
import time
import logging
import inspect
import traceback

from jshbot import data, utilities, commands, plugins, configurations
from jshbot.commands import Command, SubCommands, Shortcuts
from jshbot.exceptions import BotException

__version__ = '0.1.9'
EXCEPTION = 'Base'
uses_configuration = False
global_dictionary = {}


def get_commands():
    """Sets up new commands and shortcuts in the proper syntax.

    See dummy.py for a complete sample reference.
    """
    new_commands = []

    new_commands.append(Command(
        'ping', SubCommands(
            ('&', '(<message>)', 'The bot will respond with "Pong!" and the '
             'given message if it is included.')),
        description='Pings the bot for a response.'))

    new_commands.append(Command(
        'base', SubCommands(
            ('version', 'version', 'Gets the version of the bot.'),
            ('source', 'source', 'Gets the source of the bot.'),
            ('uptime', 'uptime', 'Gets the uptime of the bot.'),
            ('announcement', 'announcement', 'Gets the current announcement '
             'set by the bot owners.'),
            ('join', 'join', 'Joins the voice channel you are in.'),
            ('leave', 'leave', 'Leaves the voice channel you are in.')),
        shortcuts=Shortcuts(
            ('announcement', 'announcement', '', 'announcement', ''),
            ('join', 'join', '', 'join', ''),
            ('leave', 'leave', '', 'leave', ''),
            ('stfu', 'leave', '', 'leave', '')),
        description='Essential bot commands that anybody can use.'))

    new_commands.append(Command(
        'mod', SubCommands(
            ('info', 'info', 'Gets server information.'),
            ('toggle ^', 'toggle <command>', 'Enables or disables a command. '
             'NOTE: bot moderators can still use disabled commands.'),
            ('block ^', 'block <user>', 'Blocks the user from interacting '
             'with the bot.'),
            ('unblock ^', 'unblock <user>', 'Unblocks the user from '
             'interacting with the bot.'),
            ('clear', 'clear', 'Pushes chat upwards.'),
            ('mute &', 'mute (<channel>)', 'Mutes the given channel. If no '
             'channel is specified, this mutes the bot for the server.'),
            ('unmute &', 'unmute (<channel>)', 'Unmutes the given channel. If '
             'no channel is specified, this unmutes the bot for the server.'),
            ('invoker &', 'invoker (<custom invoker>)', 'Sets the custom '
             'invoker for the server. If no invoker is specified, this clears '
             'the custom invoker.'),
            ('mention', 'mention', 'Toggles mention mode. If enabled, the '
             'bot will only respond to its name or mention as an invoker.')),
        shortcuts=Shortcuts(('clear', 'clear', '', 'clear', '')),
        description='Commands for server bot moderators.',
        elevated_level=1, no_selfbot=True))

    new_commands.append(Command(
        'owner', SubCommands(
            ('addmod ^', 'addmod <user>', 'Adds the user to the bot '
             'moderators list. Use responsibly.'),
            ('removemod ^', 'removemod <user>', 'Removes the user from the '
             'bot moderators list.'),
            ('feedback ^', 'feedback <message>', 'Sends a message to the bot '
             'owners. NOTE: Your user ID will be sent as well. Please use '
             'reasonably.'),
            ('notifications', 'notifications', 'Toggles notifications from '
             'the bot regarding moderation events (such as muting channels '
             'and blocking users from bot interaction).')),
        description='Commands for server owners.',
        elevated_level=2, no_selfbot=True))

    new_commands.append(Command(
        'botowner', SubCommands(
            ('halt', 'halt', 'Shuts down the bot.'),
            ('restart', 'restart', 'Restarts the bot.'),
            ('reload', 'reload', 'Reloads all external plugins.'),
            ('ip', 'ip', 'Gets the local IP address of the bot.'),
            ('backup', 'backup', 'Gets the data folder as a zip file.'),
            ('blacklist &', 'blacklist (<user id>)', 'Blacklist or '
             'unblacklist a user from sending feedback. If no user ID is '
             'specified, this lists all blacklisted entries.'),
            ('togglefeedback', 'togglefeedback', 'Enables or disables the '
             'feedback command. Useful if pepole are trolling.'),
            ('announcement &', 'announcement (<text>)', 'Sets or clears the '
             'announcement text.')),
        shortcuts=Shortcuts(('reload', 'reload', '', 'reload', '')),
        description='Commands for the bot owner.',
        elevated_level=3))

    new_commands.append(Command(
        'debug', SubCommands(
            ('plugin list', 'plugin list', 'Lists added plugins.'),
            ('plugin:', 'plugin <plugin name>', 'Gets some basic information '
             'about the given plugin.'),
            ('latency', 'latency', 'Calculates the ping time.'),
            ('resetlocals', 'resetlocals', 'Resets the debug locals.'),
            ('^', '<python>', 'Evaluates or executes the given code.')),
        description='Commands to help the bot owner debug stuff.',
        other='Be careful with these commands! They can break the bot.',
        elevated_level=3))

    new_commands.append(Command(
        'help', SubCommands(
            ('manual ?here ^', 'manual (here) <entry number>', 'Gets the '
             'given manual entry. It is recommended to read through some of '
             'the first few pages if you do not understand how the bot '
             'works.'),
            ('manual ?here', 'manual (here)', 'Lists the available manual '
             'entries.'),
            ('all ?here', 'all (here)', 'Shows all of the commands and '
             'related help.'),
            ('?here :&', 'help (here) <base> (<topic>)', 'Gets the '
             'help of the given command. If a topic index is provided, it '
             'will get specific help regarding that command.'),
            ('?here', '(here)', 'Gets the general help text. This '
             'will list all available commands to you.')),
        shortcuts=Shortcuts(
            ('manual', 'manual {}', '&', 'manual (<arguments>)',
             '(<arguments>)')),
        description='Command help and usage manuals.',
        other=('For all of these commands, if the \'here\' option is '
               'specified, a direct message will not be sent.')))

    return new_commands


async def base_wrapper(
        bot, message, direct, blueprint_index, options, arguments):
    response = ''

    if blueprint_index == 0:  # version
        response = '`{}`\n{}'.format(bot.version, bot.date)

    elif blueprint_index == 1:  # source
        response = random.choice([
            "It's shit. I'm sorry.",
            "You want to see what the Matrix is like?",
            "Script kiddie level stuff in here.",
            "Beware the lack of PEP 8 guidelines inside!",
            "Snarky comments inside and out.",
            "Years down the road, this will all just be a really "
            "embarrassing but funny joke.",
            "Made with ~~love~~ pure hatred.",
            "At least he's using version control.",
            "Yes, I know I'm not very good. Sorry...",
            "Take it easy on me, okay?",
            "You're going to groan. A lot.",
            "You might be better off *not* looking inside."])
        response += ("\nhttps://github.com/jkchen2/JshBot\n"
                     "https://github.com/jkchen2/JshBot-plugins")

    elif blueprint_index == 2:  # uptime
        uptime_total_seconds = int(time.time()) - bot.time
        uptime_struct = time.gmtime(uptime_total_seconds)
        days = int(uptime_total_seconds / 86400)
        hours = uptime_struct.tm_hour
        minutes = uptime_struct.tm_min
        seconds = uptime_struct.tm_sec
        response = (
            "The bot has been on since **{0}**\n{1} days, {2} hours, "
            "{3} minutes, and {4} seconds").format(
                bot.readable_time, days, hours, minutes, seconds)

    elif blueprint_index == 3:  # Announcement
        announcement = data.get(bot, 'base', 'announcement')
        if not announcement:
            response = "No announcement right now!"
        else:
            response = announcement

    elif blueprint_index in (4, 5):  # Join/leave voice channel
        if message.channel.is_private:
            raise BotException(
                EXCEPTION, "This command cannot be used in direct messages.")
        voice_channel = message.author.voice_channel
        if not voice_channel:
            raise BotException(EXCEPTION, "You are not in a voice channel.")
        try:
            if blueprint_index == 4:
                await utilities.join_and_ready(
                    bot, voice_channel, is_mod=data.is_mod(
                        bot, message.server, message.author.id))
                response = "Joined {}.".format(voice_channel.name)
            else:
                await utilities.leave_and_stop(
                    bot, message.server, member=message.author, safe=False)
                response = "Left {}.".format(voice_channel.name)
        except BotException as e:
            raise e  # Pass up
        except Exception as e:
            action = 'join' if blueprint_index == 4 else 'leave'
            raise BotException(
                EXCEPTION, "Failed to {} the voice channel.".format(action),
                e=e)

    return response


async def mod_wrapper(bot, message, blueprint_index, options, arguments):
    response = ''
    mod_action = ''

    if blueprint_index == 0:  # info
        server_data = data.get(
            bot, 'base', None, server_id=message.server.id, default={})
        response = (
            '```\n'
            'Information for server {0}\n'
            'ID: {0.id}\n'
            'Owner: {0.owner.id}\n'
            'Moderators: {1}\n'
            'Blocked users: {2}\n'
            'Muted: {3}\n'
            'Muted channels: {4}\n'
            'Command invoker: {5}\n'
            'Mention mode: {6}\n'
            'Disabled commands: {7}```').format(
                message.server,
                server_data.get('moderators', []),
                server_data.get('blocked', []),
                server_data.get('muted', []),
                server_data.get('muted_channels', []),
                server_data.get('command_invoker', None),
                server_data.get('mention_mode', False),
                server_data.get('disabled', []))

    elif blueprint_index == 1:  # toggle command
        to_toggle = arguments[0].lower()
        try:
            command = bot.commands[to_toggle]
        except KeyError:
            raise BotException(EXCEPTION, "Invalid base.")

        to_toggle = command.base
        if command.plugin.__name__ == 'jshbot.base':
            raise BotException(
                EXCEPTION, "The base commands cannot be disabled.")
        pass_in = (bot, 'base', 'disabled', to_toggle)
        pass_in_keywords = {'server_id': message.server.id}
        disabled_commands = data.get(
            *pass_in[:-1], **pass_in_keywords, default=[])
        if to_toggle in disabled_commands:
            data.list_data_remove(*pass_in, **pass_in_keywords)
            response = "Enabled"
        else:
            data.list_data_append(*pass_in, **pass_in_keywords)
            response = "Disabled"
        response += " the `{}` command and all associated subcommands.".format(
            to_toggle)
        mod_action = response

    elif blueprint_index in (2, 3):  # block or unblock
        user = data.get_member(bot, arguments[0], message.server)
        block = blueprint_index == 2
        mod_action = 'Blocked {}' if block else 'Unblocked {}'
        mod_action = mod_action.format('{0} ({0.id})'.format(user))
        blocked = data.is_blocked(
            bot, message.server, user.id, strict=True)
        mod = data.is_mod(bot, message.server, user.id)
        if mod:
            raise BotException(
                EXCEPTION, "Cannot block or unblock a moderator.")
        elif block:
            if blocked:
                raise BotException(EXCEPTION, "User is already blocked.")
            else:
                data.list_data_append(
                    bot, 'base', 'blocked', user.id,
                    server_id=message.server.id)
                response = "User is now blocked."
        else:
            if not blocked:
                raise BotException(EXCEPTION, "User is already unblocked.")
            else:
                data.list_data_remove(
                    bot, 'base', 'blocked', user.id,
                    server_id=message.server.id)
                response = "User is now unblocked."

    elif blueprint_index == 4:  # clear
        response = '\n'*80 + "The chat was pushed up by a bot moderator."

    elif blueprint_index in (5, 6):  # mute or unmute
        server_id = message.server.id
        mute = blueprint_index == 5
        mod_action = 'Muted {}' if mute else 'Unmuted {}'

        if arguments[0]:
            channel = data.get_channel(bot, arguments[0], message.server)
            muted = channel.id in data.get(
                bot, 'base', 'muted_channels', server_id=server_id, default=[])
            mod_action = mod_action.format(channel.name)
            if mute:
                if muted:
                    raise BotException(
                        EXCEPTION, "Channel is already muted.")
                else:
                    data.list_data_append(
                        bot, 'base', 'muted_channels',
                        channel.id, server_id=server_id)
                    if str(channel.type) == 'voice':  # Disconnect
                        await utilities.leave_and_stop(bot, message.server)
                    response = "Channel muted."
            else:  # unmute
                if not muted:
                    raise BotException(
                        EXCEPTION, "Channel is already unmuted.")
                else:
                    data.list_data_remove(
                        bot, 'base', 'muted_channels',
                        channel.id, server_id=server_id)
                    response = "Channel unmuted."

        else:  # server
            mod_action = mod_action.format('the server')
            muted = data.get(
                bot, 'base', 'muted',
                server_id=server_id, default=False)
            if not (muted ^ mute):
                response = "Server is already {}muted.".format(
                    '' if muted else 'un')
                raise BotException(EXCEPTION, response)
            else:
                data.add(bot, 'base', 'muted', mute, server_id=server_id)
                response = "Server {}muted.".format('' if mute else 'un')

    elif blueprint_index == 7:  # invoker
        if len(arguments[0]) > 10:
            raise BotException(
                EXCEPTION,
                "The invoker can be a maximum of 10 characters long.")
        data.add(
            bot, 'base', 'command_invoker',
            arguments[0] if arguments[0] else None,
            server_id=message.server.id)
        response = "Custom command invoker {}.".format(
                'set' if arguments[0] else 'cleared')
        if arguments[0]:
            response = "Custom command invoker set."
            mod_action = "Set the server command invoker to '{}'.".format(
                arguments[0])
        else:
            response = "Custom command invoker cleared."
            mod_action = "Removed the custom command invoker."

    elif blueprint_index == 8:  # mention
        current_mode = data.get(
            bot, 'base', 'mention_mode',
            server_id=message.server.id, default=False)
        data.add(
            bot, 'base', 'mention_mode', not current_mode,
            server_id=message.server.id)
        response = "Mention mode {}activated.".format(
            'de' if current_mode else '')
        mod_action = "{}activated mention mode.".format(
            'de' if current_mode else '').capitalize()

    # Send notification if configured
    send_notifications = data.get(
        bot, 'base', 'notifications',
        server_id=message.server.id, default=True)
    if mod_action and send_notifications:
        if message.edited_timestamp:
            timestamp = message.edited_timestamp
        else:
            timestamp = message.timestamp
        notification = ('Moderator {0} ({0.id}) from {0.server} on {1}:\n\t'
                        '{2}').format(message.author, timestamp, mod_action)
        logs = await utilities.get_log_text(
            bot, message.channel, limit=20, before=message)
        logs += '\n{}'.format(utilities.get_formatted_message(message))
        await bot.send_message(message.server.owner, notification)
        await utilities.send_text_as_file(
            bot, message.server.owner, logs, 'context')

    return response


async def owner_wrapper(bot, message, blueprint_index, options, arguments):
    response = ''
    mod_action = ''
    send_notifications = data.get(
        bot, 'base', 'notifications',
        server_id=message.server.id, default=True)

    if blueprint_index in (0, 1):  # add or remove moderator
        user = data.get_member(bot, arguments[0], server=message.server)
        user_is_mod = data.is_mod(
            bot, message.server, user.id, strict=True)
        user_is_elevated = data.is_mod(bot, message.server, user.id)
        blocked = data.is_blocked(
            bot, message.server, user.id, strict=True)
        mod_action = 'Added {}' if blueprint_index == 0 else 'Removed {}'
        mod_action = mod_action.format(
            '{0} ({0.id}) as a moderator'.format(user))
        if blocked:
            raise BotException(EXCEPTION, "User is blocked.")
        elif blueprint_index == 0:  # add
            if user_is_mod or user_is_elevated:
                raise BotException(EXCEPTION, "User is already a moderator.")
            else:
                data.list_data_append(
                    bot, 'base', 'moderators',
                    user.id, server_id=message.server.id)
                response = "User is now a moderator."
        else:  # remove
            if not user_is_mod:
                raise BotException(
                    EXCEPTION, "User is not in the moderators list.")
            else:
                data.list_data_remove(
                    bot, 'base', 'moderators',
                    user.id, server_id=message.server.id)
                response = "User is no longer a moderator."

    elif blueprint_index == 2:  # send feedback
        if data.get(bot, 'base', 'feedbackdisabled', default=False):
            response = ("Feedback has been temporarily disabled, probably "
                        "due to some troll spammers.")
        else:
            text = arguments[0]
            if len(text) > 1500:
                raise BotException(
                    EXCEPTION, "Whoa! That's a lot of feedback. "
                    "1500 characters or fewer, please.")
            text = ('{0} ({0.id}) on {1.timestamp}:'
                    '\n\t{2}').format(message.author, message, text)
            await utilities.notify_owners(bot, text, user_id=message.author.id)
            response = "Message sent to bot owners."

    elif blueprint_index == 3:  # toggle notifications
        response = ("Bot moderator activity notifications are now turned "
                    "{}").format("OFF." if send_notifications else "ON.")
        data.add(
            bot, 'base', 'notifications', not send_notifications,
            server_id=message.server.id)

    # Send notification if configured
    if mod_action and send_notifications:
        if message.edited_timestamp:
            timestamp = message.edited_timestamp
        else:
            timestamp = message.timestamp
        notification = 'From {0.server} on {1}, you:\n\t{2}'.format(
            message.author, timestamp, mod_action)
        logs = await utilities.get_log_text(
            bot, message.channel, limit=20, before=message)
        logs += '\n{}'.format(utilities.get_formatted_message(message))
        await bot.send_message(message.server.owner, notification)
        await utilities.send_text_as_file(
            bot, message.server.owner, logs, 'context')

    return response


async def botowner_wrapper(bot, message, blueprint_index, options, arguments):
    response = ''
    message_type = 0
    extra = None

    if blueprint_index == 0:  # halt
        await bot.send_message(message.channel, "Going down...")
        bot.shutdown()
    elif blueprint_index == 1:  # restart
        await bot.send_message(message.channel, "Restarting...")
        bot.restart()
    elif blueprint_index == 2:  # reload
        response = "Reloading..."
        message_type = 3
        extra = ('reload',)
    elif blueprint_index == 3:  # ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Thanks Google
        ip = s.getsockname()[0]
        s.close()
        response = "Local IP: " + ip
    elif blueprint_index == 4:  # backup
        utilities.make_backup(bot)
        await bot.send_file(
            message.channel, '{}/temp/backup1.zip'.format(bot.path))
    elif blueprint_index == 5:  # blacklist
        blacklist = data.get(bot, 'base', 'blacklist', default=[])
        if not arguments[0]:
            response = "Blacklisted entries: {}".format(blacklist)
        else:
            user_id = arguments[0]
            if user_id in blacklist:
                data.list_data_remove(bot, 'base', 'blacklist', user_id)
                response = "User removed from blacklist."
            else:
                data.list_data_append(bot, 'base', 'blacklist', user_id)
                response = "User added to blacklist."
    elif blueprint_index == 6:  # toggle feedback
        status = data.get(bot, 'base', 'feedbackdisabled', default=False)
        action = "enabled" if status else "disabled"
        data.add(bot, 'base', 'feedbackdisabled', not status)
        response = "Feedback has been {}.".format(action)
    elif blueprint_index == 7:  # Announcement
        if arguments[0]:
            text = '{0}:\n{1}'.format(time.strftime('%c'), arguments[0])
            data.add(bot, 'base', 'announcement', text)
            response = "Announcement set!"
        else:
            data.add(bot, 'base', 'announcement', '')
            response = "Announcement cleared!"

    return (response, message_type, extra)


async def debug_wrapper(
        bot, message, blueprint_index, options, arguments, cleaned_content):
    response = ''
    message_type = 0
    extra = None
    global global_dictionary

    if blueprint_index == 0:  # List plugins
        plugins = list(bot.plugins.keys())
        plugins.sort()
        response = '```\n{}```'.format(plugins)

    elif blueprint_index == 1:  # Plugin information
        if options['plugin'] not in bot.plugins:
            response = options['plugin'] + " not found."
        else:
            plugin = bot.plugins[options['plugin']][0]
            version = getattr(plugin, '__version__', 'Unknown')
            has_flag = getattr(plugin, 'uses_configuration', False)
            response = ("```\nPlugin information for: {0}\n"
                        "Version: {1}\n"
                        "Config: {2}\n"
                        "Dir: {3}\n```").format(
                            options['plugin'],
                            version, has_flag, dir(plugin))

    elif blueprint_index == 2:  # Latency
        message_type = 3
        response = "Testing latency time..."
        extra = ('ping', time.time() * 1000)

    elif blueprint_index == 3:  # Reset local dictionary
        setup_debug_environment(bot)
        response = "Debug environment local dictionary reset."

    elif blueprint_index == 4:  # Exec
        global_dictionary['message'] = message

        # Sanitize input
        arguments = cleaned_content[6:]
        if arguments.startswith('```py\n') and arguments.endswith('```'):
            arguments = arguments[6:-3]
        else:
            arguments = arguments.strip('`')
        pass_in = [arguments, global_dictionary]

        # Check if the previous result should be sent as a file
        if arguments in ('saf', 'file'):
            await utilities.send_text_as_file(
                bot, message.channel,
                str(global_dictionary['result']), 'result')
        else:
            used_exec = False

            try:  # Try to execute arguments
                if '\n' in arguments:
                    exec(*pass_in)
                    used_exec = True
                else:
                    try:
                        if arguments.startswith('await '):
                            pass_in[0] = arguments[6:]
                            global_dictionary['result'] = await eval(*pass_in)
                        else:
                            global_dictionary['result'] = eval(*pass_in)
                    except SyntaxError:  # May need to use exec
                        exec(*pass_in)
                        used_exec = True

            except Exception as e:
                global_dictionary['last_traceback'] = traceback.format_exc()
                response = '`{0}: {1}`'.format(type(e).__name__, e)

            else:  # Get response if it exists
                if used_exec:
                    result = 'Executed.'
                elif global_dictionary['result'] is None:
                    result = 'Evaluated. (returned None)'
                else:
                    result = str(global_dictionary['result'])
                if len(result) >= 1998:
                    raise BotException(
                        EXCEPTION, "Exec result is too long. (try 'file')")
                if '\n' in result:  # Better formatting
                    response = '```python\n{}\n```'.format(result)
                else:  # One line response
                    response = '`{}`'.format(result)

    return (response, message_type, extra)


async def help_wrapper(bot, message, blueprint_index, options, arguments):
    response = ''
    message_type = 0
    extra = None
    direct = message.channel.is_private
    is_owner = data.is_owner(bot, message.author.id)
    server = message.server if 'here' in options else None

    if blueprint_index == 0:  # Detailed manual
        try:
            entry = int(arguments[0])
        except:
            raise BotException(EXCEPTION, "That is not a valid number.")
        response = commands.get_manual(bot, entry, server=server)

    elif blueprint_index == 1:  # General manual
        response = commands.get_general_manual(bot, server=server)

    elif blueprint_index == 2:  # All help
        base_list = []
        for command in bot.commands.values():
            if command.base not in base_list and not command.hidden:
                base_list.append(command.base)
        base_list.sort()
        help_list = ["Here is a list of all commands:\r\n"]
        for base_command in base_list:
            base_usage = commands.usage_reminder(bot, base_command)
            base_usage = base_usage[base_usage.index('\n') + 1:].replace(
                '\n', '\r\n').replace('`', '')
            help_list.append(base_usage[:-2])
        help_list.append("\r\nHere is all of the help:\r\n")
        for base_command in base_list:
            help_list.append('\r\n\r\n# {} #\r\n'.format(base_command))
            base_help = commands.get_help(bot, base_command)
            help_list.append(
                base_help.replace('\n', '\r\n').replace('`', '') + '\r\n')
            current_help_length = len(bot.commands[base_command].help)
            for it in range(1, current_help_length + 1):
                subcommand_help = commands.usage_reminder(
                    bot, base_command, index=it).replace('`', '')
                help_list.append(subcommand_help.replace('\n', '\r\n\t'))

        response = '\r\n'.join(help_list)

    elif blueprint_index == 3:  # Detailed help
        if len(arguments) == 2 and arguments[1]:
            topic = arguments[1]
        else:
            topic = None
        response = commands.get_help(
            bot, arguments[0], topic=topic,
            is_owner=is_owner, server=server)

    elif blueprint_index == 4:  # General help
        response = commands.get_general_help(
            bot, is_owner=is_owner, server=server)

    if not direct and server is None:  # Terminal reminder message
        if len(response) > 1800:
            await utilities.send_text_as_file(
                bot, message.author, response, 'help')
        else:
            await bot.send_message(message.author, response)
        response = "Check your direct messages!"
        message_type = 2
        extra = (10, message)  # Deletes the given message too
    elif len(response) > 1800:
        await utilities.send_text_as_file(
            bot, message.channel, response, 'help')
        response = ''

    return (response, message_type, extra)


async def get_response(
        bot, message, base, blueprint_index, options, arguments,
        keywords, cleaned_content):
    response, tts, message_type, extra = ('', False, 0, None)

    if base == 'ping':
        if arguments:
            response = 'Pong!\n{}'.format(arguments[0])
        else:
            response = 'Pong!'

    elif base == 'base':
        response = await base_wrapper(
            bot, message, message.channel.is_private,
            blueprint_index, options, arguments)

    elif base == 'mod':
        response = await mod_wrapper(
            bot, message, blueprint_index, options, arguments)

    elif base == 'owner':
        response = await owner_wrapper(
            bot, message, blueprint_index, options, arguments)

    elif base == 'botowner':
        response, message_type, extra = await botowner_wrapper(
            bot, message, blueprint_index, options, arguments)

    elif base == 'debug':
        response, message_type, extra = await debug_wrapper(
            bot, message, blueprint_index, options, arguments, cleaned_content)

    elif base == 'help':
        response, message_type, extra = await help_wrapper(
            bot, message, blueprint_index, options, arguments)

    else:
        response = "This should not be seen. Your command was: " + base

    return (response, tts, message_type, extra)


async def handle_active_message(bot, message_reference, extra):
    """
    This function is called if the given message was marked as active
    (message_type of 3).
    """
    if extra[0] == 'ping':
        latency_time = "Latency time: {:.2f} ms".format(
                (time.time() * 1000) - extra[1])
        await bot.edit_message(message_reference, latency_time)

    elif extra[0] == 'reload':
        logging.debug("Reloading plugins and commands...")
        bot.commands = {}
        bot.plugins = {}
        bot.manuals = []
        plugins.add_plugins(bot)
        commands.add_manuals(bot)
        logging.debug("Reloading configurations...")
        bot.configurations = {}
        configurations.add_configurations(bot)
        bot.volatile_data = {'global_users': {}, 'global_plugins': {}}
        data.check_all(bot)
        plugins.broadcast_event(bot, 0)
        await asyncio.sleep(1)
        await bot.edit_message(message_reference, "Reloaded!")


def setup_debug_environment(bot):
    """Resets the local dictionary for the debug command."""
    global global_dictionary
    global_dictionary = {}
    import pprint

    def say(text):
        calling_locals = inspect.currentframe().f_back.f_locals
        asyncio.ensure_future(bot.send_message(
            calling_locals['message'].channel, str(text)))
    global_dictionary.update({
        'bot': bot,
        'inspect': inspect,
        'traceback': traceback,
        'last_traceback': '',
        'result': '',
        'say': say,
        'pformat': pprint.pformat
    })


# Standard discord.py event functions

async def on_ready(bot):
    setup_debug_environment(bot)

async def on_server_join(bot, server):
    # Add server to the list
    logging.debug("Joining server")
    data.add_server(bot, server)
    invoker = utilities.get_invoker(bot)
    text = (
        "Hello! You are receiving this notification because this bot was "
        "added to one of your servers, specifically '{0.name}' (ID: {0.id}). "
        "If you are aware of this and approve of the addition, feel free to "
        "continue and use the bot. However, if you did not approve of this "
        "addition, it is highly recommended you kick or ban this bot as there "
        "may be potential for users to use the bot to spam. Only users that "
        "have the administrator permission can add bots to servers. "
        "Unfortunately, there is no way to track who added the bot.\n\n"
        "To read more about the functionality and usage of the bot, type "
        "`{1}manual` to see a list of topics, and `{1}help` to see a list of "
        "commands. **As a server owner, it is highly recommended that you "
        "read `{1}manual 5` and `{1}manual 4` for moderating and configuring "
        "the bot.**\n\nThat's all for now. If you have any questions, please "
        "refer to the manual, or send the bot owners a message using "
        "`{1}owner feedback <message>`.").format(server, invoker)
    await bot.send_message(server.owner, text)

async def on_message_edit(bot, before, after):
    """Integrates with the core to handle edited messages."""
    if before.content != after.content and before.id in bot.edit_dictionary:
        message_reference = bot.edit_dictionary.pop(before.id)
        await bot.on_message(after, replacement_message=message_reference)

async def on_error(bot, event, *args, **kwargs):
    """Gets uncaught exceptions."""
    logging.error(
        "An exception was thrown that wasn't handled by the core. \n"
        "Event: {0}\nargs: {1}\nkwargs: {2}".format(event, args, kwargs))
    traceback.print_exc()
