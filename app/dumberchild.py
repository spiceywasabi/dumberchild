import sys, os
import re
import nextcord as discord
import aiml
import logging

# Note: Requires this specific version of PyAIML https://github.com/weddige/pyaiml3 

logname="botlog.txt"

if os.getenv("BOTINCONTAINER") is None:
   logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S.%f%z',
                            level=logging.INFO)
else:
   logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#logging.basicConfig(level=logging.INFO)
try:
   logging.getLogger("discord").setLevel(logging.WARNING)
except:
   print("unable to adjust logging level")

class DumberChild(discord.Client):
    brain = None
    brain_file = None
    brain_xml = None
    brainLoaded = False
    brainLobotomy = False
    
    def load_aiml(self):
       self.brain_file=os.getenv("AIML_BRAIN")
       self.brain_xml=os.getenv("AIML_XML")
       print("aiml brain = %s"%self.brain_file)
       print("aiml xml = %s"%self.brain_xml)
       if not os.path.exists(self.brain_file):
           self.reload_brain()
       else:
           self.brain = aiml.Kernel()
           self.brain.bootstrap(brainFile = self.brain_file)   
           self.brainLoaded = True
        
    def reload_brain(self):
      if not os.path.exists(self.brain_xml):
          logging.error("cannot load brain, brain xml is not valid or combiled brain is corrupt");
          print("error, cannot reload brain or load brain xml data to init")
      if os.path.exists(self.brain_file) and self.brainLobotomy:
          os.path.unlink(self.brain_file)
          logging.info("rebuilding brain, existing brain has been removed")
          print("brain existed, and is being removed")
      self.brain = aiml.Kernel()
      self.brain.bootstrap(learnFiles=self.brain_xml, commands="load aiml b") 
      self.brainLoaded = True
      self.brain.saveBrain(self.brain_file)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.mention_everyone:
            return       
        if client.user.mentioned_in(message):
            if self.brainLoaded:
               try:
                  processed_msg = re.sub(r'<@(?:\?|!)[0-9]+> ', r'', str(message.content)[:230],re.MULTILINE)
                  logging.info("user: %s"%processed_msg)
                  reply = self.brain.respond(processed_msg)
                  logging.info("bot: %s"%str(reply))
                  await message.reply(reply)
               except Exception as e:
                  print("error: ",e)
                  logging.error("error and brain could not replly to message")
                  await message.reply("I am attempting to fill a silent moment with non-relevant conversation.")
            else:
               logging.error("brain is not loaded and cannot reply to message")
               await message.reply("... If i only had a brain ... ")
    
        if message.content.startswith('hello moto'):
            await message.reply('hello', mention_author=True)
            
        if message.content.startswith('hello rebuild brain'):
            logging.info("brain has been rebuilt by user interaction")
            await message.reply('hello brain reload in progress', mention_author=True)
            self.reload_brain()
                                                        
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = DumberChild()
client.load_aiml()
client.run(DISCORD_TOKEN)


