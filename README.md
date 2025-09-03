# Waifu full local companion

Example video

[![Mi video](https://img.youtube.com/vi/4LkFELAaSyk/0.jpg)](https://youtu.be/4LkFELAaSyk)

All these steps are maked to run your own full customizable waifu running fully in local
you can make whatever your imagination or ideas tha you can have, because use : 

- n8n ( to create your own workflows )
- LLM models likes gpt-oss ( To handle and generate respones )
- Nvidia 12GB of VRAM ( To handle all the LLM and hard memory space )
- Kokoro TTS ( To get a natural audio response using the CPU/GPU )
- Vtuber studio ( To handle your custom Vtuber/Waifu/Companion Model )

I hope this give to you a lot ideas to make your own waifus/companion that can help you
doing whatever you want, all is handled with n8n so you just need to be creative connecting
the n8n nodes :)


You wanna know how it works and run it ?

Lets start !

# Tested Requirements

This currently works only in Linux for now, because i dont have much time to finish the Open AI hackthon,
in the future also is gonna works on Windows ( if the community wants :) )

This code runs and tested with this requirements

```
       _,met$$$$$gg.          kypanz@debian 
    ,g$$$$$$$$$$$$$$$P.       ------------- 
  ,g$$P"     """Y$$.".        OS: Debian GNU/Linux 12 (bookworm) x86_64 
 ,$$P'              `$$$.     Host: A320AM4-M3D 1.x/3.x/5.x 
',$$P       ,ggs.     `$$b:   Kernel: 6.1.0-38-amd64 
`d$$'     ,$P"'   .    $$$    Uptime: 10 days, 1 hour, 21 mins 
 $$P      d$'     ,    $$P    Packages: 3393 (dpkg), 23 (flatpak) 
 $$:      $$.   -    ,d$$'    Shell: bash 5.2.15 
 $$;      Y$b._   _,d$P'      Resolution: 1440x900 
 Y$$.    `.`"Y$$$$P"'         DE: GNOME 43.9 
 `$$b      "-.__              WM: Mutter 
  `Y$$                        WM Theme: Adwaita 
   `Y$$.                      Theme: Adwaita [GTK2/3] 
     `$$b.                    Icons: Adwaita [GTK2/3] 
       `Y$$b.                 Terminal: gnome-terminal 
          `"Y$b._             CPU: AMD Athlon 3000G (4) @ 3.500GHz 
              `"""            GPU: NVIDIA GeForce RTX 3060 Lite Hash Rate 
                              Memory: 10642MiB / 32020MiB 

```

# Notes to have in mind

Currently i have an `AMD Athlon 3000g` that is a bottle neck for my `RTX 3060`
if you have a better CPU than me is gonna runs more fastly than me because
gpt-oss runs in hybrid mode ( this means use GPU & CPU to generate responses )

# Setting up the n8n Docker

[ new terminal ] - This runs the n8n workflow automation tool in localhost

```
cd ./n8n
bash install_n8n.sh
bash run-n8n.sh
```

# Setting up the kokoro TTS server

[ new terminal ] - This starts the kokoro TTS server 

note : if you have conda enabled you need to deactivate it first

```
conda deactivate
```

then starts kokoro TTS server

```
cd ./local-tts
source ./venv/bin/activate
python tts_server.py
```

( Optional )

to change the voices you can change it in the `tts_server.py` file the name of the voice model
that you want to use

some available voice models from Kokoro TTS 

```
https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices
```

# Setting up gpt-oss and ollama

First we need to create a custom host to interact between the docker and the ollama

to understand works like this

- Docker ( run isolated )
- Ollama ( runs out docker / not isolated / in your main host )

So you need to enable your ollama serve that can comunicate with all the possible request that gonna join
using this command

```
OLLAMA_HOST=0.0.0.0 ollama serve
```

Then you need to download the gpt-oss model runing in a new terminal

```
ollama run gpt-oss
```

after that you can close the interactive LLM with ollama pressing `CTRL + D` that close the interactive window

then you can close that terminal if you want and keep the `LOCAL_HOST=0.0.0.0 ollama serve` terminal window to handle the requests
from n8n

# Configurating the hosts file

To interact between Docker and your main Host ( outside the n8n Docker ) you need to create this in your `/etc/hosts` file using an IDE 
like neovim/vim/nano or whathever you like, we gonna add this at the end

```
# For n8n Docker communication with ollama that runs outside
127.0.0.1       host.docker.internal
```

Note : Remember to edit `/etc/hosts` you need to use the `sudo` command that means you are running it like `root` ( owner of the system ) 

# Setting up the Vtuber Studio settings

Download the vtuber studio from steam

Direct link

```
https://store.steampowered.com/app/1325860/VTube_Studio/
```

If these link dont work you can just look for `Vtube Studio` in steam website or any searcher engine

After download you just need to run it and select your Waifu/Companion 2d Model

( optional ) [ new terminal ] - This keep the Vtuber studio window on top

```
cd ./local-tts
bash always-on-top.sh
```

### Setting up the Lipsync

For the lipsync we need to install `pavucontrol` to create a Virtual input microphone to send 
the audio generated with kokoro there

```
sudo apt install pavucontrol
```

Then generate the Virtual Microphone

```
pactl load-module module-null-sink sink_name=VirtualMic sink_properties=device.description="MicVirtual"
pactl load-module module-loopback source=VirtualMic.monitor
```

Then you need to set the input for the Vtuber Studio ( you need to have the app started )

execute 

```
pavucontrol
```

then select `Recording` tab, and then `Vtuber Studio.exe` and in the dropdown menu select 
your Virtual Microphone created in this case `Monitor of MicVirtual` / `MicVirtual`

then just close the window and all is set for the Lipsync

Note :
All the files proccesed by Vtube Studio ( Live2D behind ) are needed in .wav format because internally vtuber studio 
and live2d use `RMS` to convert the `.wav` files into waves to produce the lipsync effect, if is not a `.wav` file the 
program gonna crash or the model dont move their mouth, also you need to be sure your model is configurated to associate 
the voice detected with the microphone to move their mouth ( is in Model configuration in the Vtube Studio )

( Optional to read ) How `RMS` / `Root mean square` works
```
https://en.wikipedia.org/wiki/Root_mean_square
https://docs.live2d.com/en/cubism-sdk-tutorials/native-lipsync-from-wav-native/
```

# Dashboard and workflow configuration

- Open the `http://localhost:5678` website to see the `n8n` dashboard
- Import the workflow file


Double click the `Ollama Chat Model` and configure your LLM url with : `http://host.docker.internal:11434` ( this gonna point to your ollama server initiated before )

The api key is not needed in the `Ollama Chat Model` so you can keep that empty and just try to test the connection,
if all goes well is gonna be green, after that you can close these modal/window


Then write something in the input chat to interact with your waifu and your companion is gonna start talk

Enjoy ! :)

After that you can connect and do whatever you want based in your imagination to add or change n8n nodes to do functionalities with
your waifu companion


If you have questions/errors/bugs/ideas feel free to send me a message at `@kypanz` in Discord or open a issue directly in the github

Happy hacking !


