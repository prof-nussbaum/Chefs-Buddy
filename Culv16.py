# Folders on this computer
# models folder
models = "C:/Users/EET/Desktop/Culinary Slideshow/models/"

#DISPLAY FUNCTIONS FOR SLIDESHOW
import time
import pygame
# Need 16:9 Aspect Ratio
X = 1600 # was 960
Y = 900 # was  540
pygame.init()

demo_screen = '.\AI_Graphic.png'
demo_text = " --- Autonomous AI Agent Demonstration --- "

# Add 72 pixels up top to hold text
screen = pygame.display.set_mode((X,Y+72))#, pygame.FULLSCREEN)
font = pygame.font.Font(None, 36)

screen.fill((0,0,0))
image = pygame.image.load(demo_screen).convert()
screen.blit(image, (0,72))
pygame.display.set_caption(demo_text)
text_surface = font.render(demo_text, True, (255,255,255))
screen.blit(text_surface, (10, 10))
pygame.display.flip()
time.sleep(3)

# ALL DONE WITH SLIDESHOW
#pygame.display.quit()
#pygame.quit()
#exit()


# The 50 states
fifty_states = [ "Alabama", 
			"Montana",
			"Alaska",
			"Nebraska",
			"Arizona",
			"Nevada",
			"Arkansas",
			"New Hampshire",
			"California",
			"New Jersey",
			"Colorado",
			"New Mexico",
			"Connecticut",
			"New York",
			"Delaware",
			"North Carolina",
			"Florida",
			"North Dakota",
			"Georgia",
			"Ohio",
			"Hawaii",
			"Oklahoma",
			"Idaho",
			"Oregon",
			"Illinois",
			"Pennsylvania",
			"Indiana",
			"Rhode Island",
			"Iowa",
			"South Carolina",
			"Kansas",
			"South Dakota",
			"Kentucky",
			"Tennessee",
			"Louisiana",
			"Texas",
			"Maine",
			"Utah",
			"Maryland",
			"Vermont",
			"Massachusetts",
			"Virginia",
			"Michigan",
			"Washington",
			"Minnesota",
			"West Virginia",
			"Mississippi",
			"Wisconsin",
			"Missouri",
			"Wyoming" ]


# AUTO111SDK
from auto1111sdk import StableDiffusionPipeline
model_loc = models + "v1-5-pruned-emaonly.safetensors"
pipe = StableDiffusionPipeline(model_loc)
    # was v2-1_768-ema-pruned.safetensors", default_command_args = " --no-half")

# AUTO1111SDK UPSCALER
from auto1111sdk import EsrganPipeline
upscaler = EsrganPipeline(models + "4x_UniversalUpscalerV2-Sharp_101000_G.pth")

# OLLAMA
import ollama
start_prompt = 'I want you to write a short and simple prompt for a text to image generator. I only want the prompt as your reply. Do not include any escape characters, additional introductions, or other informational messages. Just the prompt. The prompt should ask the text to image generator to produce an image.'
topic_prompt = 'The image is of a famous culinary specialty from a specific region I will provide. The prompt should ask to create an image of a plate of this delicious dish drawn with great detail. The appetizing image should be of a recipe from the United States, specifically from the state of '

i = 0
while(True) :
   i += 1
   if (i >= 50): i = 0

   # Exery 10 images, show the demo information for 10 seconds
   if (i % 10 == 0) :
      # Allow some time for the prior picture to be shown
      time.sleep(10)
      # Perpare the screen
      screen = pygame.display.set_mode((X,Y+72))#, pygame.FULLSCREEN)
      screen.fill((0,0,0))
      # Display the image
      image = pygame.image.load(demo_screen).convert()
      screen.blit(image, (0,72))
      # Display the text
      font = pygame.font.Font(None, 36)
      # Make the window top caption the name of the recipe
      pygame.display.set_caption(demo_text)
      # draw at the top in a large font
      text_surface = font.render(demo_text, True, (255,255,255))
      screen.blit(text_surface, (10, 10))
      pygame.display.flip()
      # wait a few more seconds - as this will stay on the screen while the next image is being processed
      time.sleep(3)

   # OLLAMA
   usa_state = fifty_states[i]
   my_prompt = start_prompt + topic_prompt + usa_state
   ollama_response = ollama.chat(model="llama3", messages =[{'role':'user','content':my_prompt}])
   txt2img_prompt = ollama_response['message']['content']
   print(txt2img_prompt)

   # GET THE SIMPLE NAME FOR THIS DISH   
   ollama_response = ollama.chat(model="llama3", messages =[
                                    {'role':'user','content':my_prompt},
                                    {'role':'assistant','content':txt2img_prompt},
                                    {'role':'user','content':'just provide me the name of that recipe'}
                                 ])
   recipe_name = ollama_response['message']['content']
   print('\n',recipe_name)

   # GET THE INGREDIENTS FOR THE RECIPE
   ollama_response = ollama.chat(model="llama3", messages =[
                                    {'role':'user','content':my_prompt},
                                    {'role':'assistant','content':txt2img_prompt},
                                    {'role':'user','content':'provide the top three ingredients ranked by cost, in one line, separated by  commas, followed by the two words Total Cost followed by the your best estimate of the total cost to create this recipe per plate in dollars. Do not include any other words in the response.'}
                                 ])
   ingredients = "Top ingredients by cost are: " + ollama_response['message']['content']
   print('\n', ingredients)
  
   
   # AUTOSDK1111
   output = pipe.generate_txt2img(prompt = txt2img_prompt, height = Y/2, width = X/2, steps = 50)
   file_name = usa_state + "_image.png"
   output [0].save(file_name)

   #DISPLAY HALF-SIZE VERSION
#   screen = pygame.display.set_mode((X,Y))#, pygame.FULLSCREEN)
#   font = pygame.font.Font(None, 36)
#   screen.fill((0,0,0))
#   image = pygame.image.load(file_name).convert()
#   screen.blit(image, (0,0))
#   text = usa_state + "--->" + recipe_name
#   pygame.display.set_caption(text)
#   text_surface = font.render(text, True, (255,255,255))
#   screen.blit(text_surface, (10, 10))
#   pygame.display.flip()

   # LET'S SEE if UPSCALING improves the image...
   # AUTOSDK1111
   output2 = upscaler.upscale(img = output[0], scale = 2)
   file_name2 = usa_state + "_image2.png"
   output2.save(file_name2)

   #DISPLAY
   # Perpare the screen
   screen = pygame.display.set_mode((X,Y+72))#, pygame.FULLSCREEN)
   screen.fill((0,0,0))

   # Display the image
   image = pygame.image.load(file_name2).convert()
   screen.blit(image, (0,72))


   # Display the name of the recipe
   font = pygame.font.Font(None, 36)
   text = usa_state + "--->" + recipe_name
   # Make the window top caption the name of the recipe
   pygame.display.set_caption(text)
   # draw the name of the recipe at the top in a large font
   text_surface = font.render(text, True, (255,255,255))
   screen.blit(text_surface, (10, 10))
   pygame.display.flip()
   # draw the ingredients of the recipe at the in a small font
   font = pygame.font.Font(None, 36)
   text_surface = font.render(ingredients, True, (255,255,255))
   screen.blit(text_surface, (40, 40))
   pygame.display.flip()

   if pygame.event.get() == pygame.K_ESCAPE: break


screen.fill((0,0,0))
image = pygame.image.load('.\intro.png').convert()
screen.blit(image, (0,0))
text = "Goodbye!"
pygame.display.set_caption(text)
text_surface = font.render(text, True, (255,255,255))
screen.blit(text_surface, (10, 10))
pygame.display.flip()
time.sleep(3)

# ALL DONE WITH SLIDESHOW
pygame.display.quit()
pygame.quit()
exit()

# ---===---===---===---===---===---===---===---===
#     INSTRUCTIONS ON HOW TO INSTALL AUTO1111SDK FOR WINDOWS WITH GPU:
# Install the Python version (3.10.6) from here: https://www.python.org/downloads/windows/
# Install pip as follows: py -m pip install pip --upgrade
# Install CUDA as follows: py -m pip install --verbose nvidia-cuda-runtime-cu11
# Install PyTorch (torch) that uses CUDA as follows: python -m pip install --verbose torch==2.1.0 torchvision --index-url https://download.pytorch.org/whl/cu118
# Make sure the python scripts are in the path
# Press the Start key and search for “Edit the system environment variables”.
# Go to the “Advanced” tab and click the “Environment variables” button.
# Select the “Path” variable under “User variables” or “System variables”.
# Click the “Edit” button and press “New” to add the desired path.
# C:\Users\EET\AppData\Local\Programs\Python\Python310\Scripts
# ---===---===---===---===---===---===---===---===
# Then confirm that Torch was indeed installed and it is set up to use CUDA, buy doing the following within python:
# python
# >>> import torch
# 
# >>> print("Torch version:",torch.__version__)
# Torch version: 2.1.0+cu118
# 
# >>> print("Is CUDA enabled?",torch.cuda.is_available())
# Is CUDA enabled? True
# ---===---===---===---===---===---===---===---===# 
#     GOOGLE MODELS TO DOWNLOAD FROM HUGGINGFACE
#    THESE GO IN "Models" FOLDER
# v1-5-pruned-emaonly.safetensors
# v2-1_768-ema-pruned.safetensors
#    THIS GOES IN A NEW "Upscaler" FOLDER (or you can stick in the models folder if you're not using AUTOMATIC1111 GUI)
# 4x_UniversalUpscalerV2-Sharp_101000_G.pth
#
# Then change the file locations here at the top of this python script:
# models = "C:/Users/EET/Desktop/Culinary Slideshow/models"
# ---===---===---===---===---===---===---===---===
# More details are here:
# https://github.com/Auto1111SDK/Auto1111SDK/blob/main/automatic1111sdk_on_windows_w_gpu.md
#    then install auto1111sdk using pip "pip install auto1111sdk" with additional instructions here:
# https://pypi.org/project/auto1111sdk/
# ---===---===---===---===---===---===---===---===
# ---===---===---===---===---===---===---===---===
#     INSTRUCTIONS ON HOW TO INSTALL PYGAME TO SHOW THINGS ON THE SCREEN
# install pygame using pip "pip install pygame"
# ---===---===---===---===---===---===---===---===
#     INSTRUCTIONS ON HOW TO INSTALL OLLAMA and LLAMA3 8B FOR WINDOWS WITH GPU:
# Install for Windows from here: https://ollama.com/download/windows
# Run the installer
# Pull the desired model. We will use the 8B parameter llama3 using the command line
# ollama pull llama3
# You can test it from the command line using "ollama run llama3"
# install ollama using pip "pip install ollama"
# ---===---===---===---===---===---===---===---===
# ---===---===---===---===---===---===---===---===
# Installing automatic1111
# https://github.com/AUTOMATIC1111/stable-diffusion-webui
# Installation on Windows 10/11 with NVidia-GPUs using release package
# Download sd.webui.zip from v1.0.0-pre (https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.0.0-pre) and extract its contents.
# Run update.bat.
# Run run.bat.
# For more details see Install-and-Run-on-NVidia-GPUs here: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-NVidia-GPUs