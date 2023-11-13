# glance

![glanceLogo](https://github.com/NuMellow/glance/assets/23238520/becd33c1-2b79-454c-b12e-d2fbd7b84b8f)

An e-ink display with fun and helpful information, just a glance away.

<img src="https://github.com/NuMellow/glance/assets/23238520/f29084d3-147c-47a5-8be7-3cf1759f471d" title="Upcoming contests" width="400" />
<img src="https://github.com/NuMellow/glance/assets/23238520/75a07b5a-7152-431e-8965-f9949f957d13" title="Photo album" width="400" />

## Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Contributing and adding your own apps](#contributing-adding-and-suggesting-your-own-apps)
- [Acknowledgements and credits](#acknowledgements-and-credits)

## About
Glance is a picture frame-like e-ink tablet that is designed to display glance-able information thoughout the week.

It is made using a 7.5 inch e-ink display, rasberry pi 3b, pi sugar battery hat and a 3D printed casing.

It currently has 2 apps:
- Current Contests - Displays the current open contests on instrucatables.com
- Photo Album - Displays a random image from shared google photos album 

## Getting Started
### Hardware
Check out the wiki(coming soon) for details on how to make one

### Software
After downloading the repository, navigate into the `glance` directory and run the following commands 

#### Installing packages
- `pip install -r requirements.txt` - Installs necessary packages to run glance

#### Setting up the .conf files
There are several `.conf` files in the src directory. These are configuration files that can configure the way glance behaves

- glance.conf - This file contains the following configuration:
   - page: determines which app (also called pages) to show. If you use the pi sugar battery you can set the custom button to cycle through the pages depending on what content you want to show. See wiki(comimng soon) for details
   - has_pi_sugar: determines whether Glance is using the pi sugar battery and can display battery percentage in the different apps. If you're not using the battery update it to 'False'
   - numofapps - This is the total number apps.
- album.conf - This is used for the Album app. Add a url to a shared google photos album.

#### Running glance
`python glance.py`

The screen remains on even without power, so if you are using a battery you can shutdown you pi and the display will continue to show information. Of course this also means that it will not be able to update the information. If you use the pi sugar, you can have it start up at a specific time every day. See wiki(coming soon) for details.

## Contributing, adding and suggesting your own apps
If you have app requests you could create an issue with the "App request" label and perhaps I might make it. Or if you would like to make your own apps for Glance, you can either fork this repo and create to your heart's content or pull this repo and create a pull request to have it added to this project 😀.

## Acknowledgements and credits
- The instrucatbles contest app makes use of the webscraper created by James Matlock in his repo: https://github.com/jmatlock/ContestScraperFlask

