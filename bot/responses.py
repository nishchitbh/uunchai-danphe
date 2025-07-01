from random import choice
import discord
import shlex
from sheet.sheet_operations import (
    get_top_k_individual,
    increase_score,
)


def get_help():
    embed = discord.Embed(
        title="Danphe",
        description="Welcome to Danphe Leaderboard! Here are all the available commands:",
        color=discord.Color.blue(),
    )

    # View Leaderboard Commands
    embed.add_field(
        name="📊 View Leaderboards",
        value="**`danphe top <k>`**\n"
        "Shows the top k individual users sorted by their scores.\n"
        "Example: `danphe top 5` shows the top 5 users\n\n",
        inline=False,
    )

    # Admin Commands
    embed.add_field(
        name="🔒 Admin Commands",
        value="**`danphe increase_score '<team name>' <points>`**\n"
        "Increases a registered team's score by the specified points.\n"
        "Example: `danphe increase_score 'Uunchai' 10`",
        inline=False,
    )

    embed.set_footer(
        text='💡 Use \'danphe help\' anytime to see this help message'
    )
    return embed


def get_responses(user_input: str, is_admin: bool) -> str | discord.Embed:
    lowered: str = user_input

    if lowered == "":
        return "Well you're awfully silent..."
    elif lowered.startswith("danphe "):
        # Remove the "danphe " prefix
        command = lowered[7:]

        # Help command
        if command == "help":
            return get_help()

        # Top k users command
        elif command.startswith("top "):
            try:
                k = int(command.split()[1])
                if k <= 0:
                    return "Please provide a positive number for top k users"
                if k>25:
                    return "Unforunately, Discord's API doesn't allow more than 25 embeds in a single message. How sad!" + choice(["🥲","😔","😉","😑","😐","🤨","😶","🫥","🙄","😏","😣","😥","😮","🤐","😯","😪","🥱","😫","😴"])

                top_users = get_top_k_individual(k)
                if not top_users:
                    return "No users found in the leaderboard"

                embed = discord.Embed(
                    title=f"Top {k} Users",
                    description="Here are the top performers!",
                    color=discord.Color.gold(),
                )

                for i, user in enumerate(top_users, 1):
                    try:
                        team = user.get("Team", "Unknown")
                        danphe_points = user.get("Danphe Points", "NaN")

                        embed.add_field(
                            name=f"{i}. {team}",
                            value=f"Danphe Points: {danphe_points}",
                            inline=False,
                        )
                    except Exception as e:
                        print(f"Error processing user {i}: {e}")
                        continue

                return embed
            except (IndexError, ValueError) as e:
                print(f"Error in top command: {e}")
                return "Please use the correct format: danphe top <number>"
        elif command.startswith("increase_score "):
            if not is_admin:
                return "❌ You need admin permissions to use this command!"
            try:
                # split respects single-quoted strings
                tokens = shlex.split(command)
                # tokens == ["increase_score", "Some User Name", "10"]
                if len(tokens) != 3:
                    return "Please use the correct format: danphe increase_score '<username>' <points>"

                _, username, points_str = tokens
                points = int(points_str)
                increase_score(username, points)
                return f"✅ Successfully increased {username!r}'s score by {points} points!"
            except ValueError:
                return "Please use the correct format: danphe increase_score '<username>' <points>"

        else:
            return "Unknown command. Use 'danphe help' to see available commands."

    elif "hello" in lowered:
        return "hello there!"
    else:
        return choice(
            [
                "I do not understand.",
                "What are you talking about?",
                "Do you mind rephrasing?",
            ]
        )
