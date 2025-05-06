import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from config import BOT_TOKEN as TOKEN
import os
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Reminder class to handle reminders
class Reminder:
    def __init__(self, duration: int, message: str):
        self.duration = duration  # Duration in seconds
        self.message = message
        self.end_time = datetime.now() + timedelta(seconds=duration)

    def is_active(self):
        return datetime.now() < self.end_time

    def update(self, duration: int, message: str):
        self.duration = duration
        self.message = message
        self.end_time = datetime.now() + timedelta(seconds=duration)

# Project class to manage tasks
class Project:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_name: str):
        self.tasks[task_name] = False  # False indicates the task is not completed

    def complete_task(self, task_name: str):
        if task_name in self.tasks:
            self.tasks[task_name] = True

    def list_tasks(self):
        return {task: completed for task, completed in self.tasks.items()}

# Global variables to hold reminders and projects
reminders = {}
projects = {}

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Productivity Bot! Use /set_reminder, /add_task, /complete_task, and /list_tasks.")

# Command to set a reminder
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        duration = int(context.args[0])
        message = ' '.join(context.args[1:])
        reminder = Reminder(duration, message)
        reminders[update.effective_chat.id] = reminder
        await update.message.reply_text(f"Reminder set for {duration} seconds: {message}")
        await asyncio.sleep(duration)
        await update.message.reply_text(f"Reminder: {message}")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /set_reminder <duration_in_seconds> <message>")

# Command to update an existing reminder
async def update_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in reminders:
        try:
            duration = int(context.args[0])
            message = ' '.join(context.args[1:])
            reminders[update.effective_chat.id].update(duration, message)
            await update.message.reply_text(f"Reminder updated to {duration} seconds: {message}")
        except (IndexError, ValueError):
            await update.message.reply_text("Usage: /update_reminder <duration_in_seconds> <message>")
    else:
        await update.message.reply_text("No active reminder to update.")

# Command to add a task to a project
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_name = ' '.join(context.args)
    if task_name:
        if update.effective_chat.id not in projects:
            projects[update.effective_chat.id] = Project()
        projects[update.effective_chat.id].add_task(task_name)
        await update.message.reply_text(f"Task '{task_name}' added.")
    else:
        await update.message.reply_text("Usage: /add_task <task_name>")

# Command to complete a task
async def complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_name = ' '.join(context.args)
    if update.effective_chat.id in projects:
        projects[update.effective_chat.id].complete_task(task_name)
        await update.message.reply_text(f"Task '{task_name}' marked as completed.")
    else:
        await update.message.reply_text("No tasks found. Please add a task first.")

# Command to list all tasks
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in projects:
        tasks = projects[update.effective_chat.id].list_tasks()
        if tasks:
            task_list = "\n".join([f"{task}: {'✔️' if completed else '❌'}" for task, completed in tasks.items()])
            await update.message.reply_text(f"Tasks:\n{task_list}")
        else:
            await update.message.reply_text("No tasks available.")
    else:
        await update.message.reply_text("No tasks found. Please add a task first.")

# Main function to run the bot
if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_reminder', set_reminder))
    application.add_handler(CommandHandler('update_reminder', update_reminder))
    application.add_handler(CommandHandler('add_task', add_task))
    application.add_handler(CommandHandler('complete_task', complete_task))
    application.add_handler(CommandHandler('list_tasks', list_tasks))

    # Start the bot
    application.run_polling()
