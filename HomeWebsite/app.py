from flask import Flask, render_template, request, session, url_for
import random

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "123"

#home page
@app.route('/')
def home():
    return render_template('home.html')


info_dict = {
    "projectTikTok":["https://github.com/Freskoko?tab=repositories","https://youtu.be/5fe88IU6DwI","TikTokBot",
    "This project uses the reddit-api to extract post data from popular reddit posts. Gtts (google-text-to-speech) turns the text into speech","Moviepy creates a video using the text and speech, as well as gameplay footage in the background", "Finally pyautogui, and selenium are used to post the content to Instagram/Tiktok."]
    ,

    "projectOutLouder":["https://github.com/Freskoko/OutLouderBot-2","https://www.youtube.com/watch?v=ScMzIvxBSi4","OutLouder",
    "This project uses selenium to access Outloud which is a music service where users can vote on songs", "This project allows a song to be voted on mulitple times by sending several requests to the website."," This was quite fun to make and use, made in collaboration with Luca Fossen"]
    ,
    "projectSeaGullID":["https://github.com/Freskoko/SeaGullID","https://www.youtube.com/watch?v=ScMzIvxBSi4","SeaGullID",
    "This project used PYQT6 to create an easy to use GUI for identifiying norwegian seagulls","This was before i learned that things are much easier on the net","I am happy with how it turned out, one of my first projects"]
    ,
    "projectinstagramBot":["https://github.com/Freskoko/instagramBotMemeAccount","https://www.youtube.com/watch?v=ScMzIvxBSi4","InstagramBot",
    "This project uses Selenium and pyautogui to upload images to instagram that have been collected from redditdownloader.com", "This is fully automatic, and is pretty fun to watch happen","Exciting!"]
    ,
    "projectPyEvolution":["https://github.com/Freskoko/PyGameDuckEvolution","https://www.youtube.com/watch?v=ScMzIvxBSi4","Evolution using pygame",
    "This project simulates evolution, ducks eat bread, wolves eat ducks. Wolves/Ducks who perform well pass their genes (speed) on","The genetic algorithm used here is quite basic as there is only 1 thing evolving(speed)","A really fun project to learn programming"]
    ,
    "projectThisWebsite":["https://github.com/Freskoko","https://www.youtube.com/watch?v=ScMzIvxBSi4","This website!",
    "This website was built using Flask, HTML and CSS.","There is not much more to say","Have a look around!"]
}

#general renderer 

#@app.route('/project/', methods=['GET'])
@app.route('/project/TikTok', methods=['GET',"POST"])
@app.route('/project/OutLouder', methods=['GET',"POST"])
@app.route('/project/SeaGullID', methods=['GET',"POST"])
@app.route('/project/instagramBot', methods=['GET',"POST"])
@app.route('/project/PyEvolution', methods=['GET',"POST"])
@app.route('/project/ThisWebsite', methods=['GET',"POST"])


def just_render():
    file_name = request.path.replace('/', '')
    template = '{file_name}.html'.format(file_name=file_name)
    infolist = info_dict[file_name]

    return render_template("project.html",
        githublink =    infolist[0],
        youtubeLink =   infolist[1],
        title =         infolist[2],
        maintext=       infolist[3],
        secondtext =    infolist[4],
        lasttext=       infolist[5])

    #<!-- needs: 
    #project name
    #libraries used
    #github link
    #youtube link
    # -->


#page with buttons and such

@app.route('/contact/', methods=['GET',"POST"])
def contact():
    return render_template("contact.html")

@app.route('/about/', methods=['GET',"POST"])
def about():
    return render_template("about.html")

@app.route("/stat101/", methods=['GET',"POST"])

def stat101():
    return render_template("stat101.html")


@app.route("/drikke/", methods=['GET','POST'])

def drikke():  

    def generate_image():

        with open("GameChallenges.txt","r",encoding="utf8") as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            funnytext = random.choice(lines)
            file.close()

        try:
            namelist = session['names']
            person = random.choice(namelist)

            if person == "":
                return(namelist)

        except Exception:
            return("⬇ No names... Add some below ⬇")

        personrandom = random.randint(1,15)
        if personrandom == 10:
            person = "Everyone"
            
        return (f"{person} {funnytext}")

    def clear_names():
     
        session['names'] = []
        return ("All names cleared")

    def addName():

        name = request.form['addplayer']

        if name == "":
            return "Names cannot be empty"

        if name != "":
            if "names" not in session:
                session['names'] = []

            namelist = session['names']
            namelist.append(name)
            session['names'] = namelist  # 

        return f"Welcome {name}"

    
    completedprompt = "🍺 Do the challenge or dice roll = drinks 🍺 When the bar fills up" 
    rolleddice = "?"
    
    if request.method == "POST": 

        
        completedprompt = "🍺 Do the challenge or dice roll = drinks 🍺 When the bar fills up" 
        rolleddice = "?"

        if "progbarvalue" not in session:
            session["progbarvalue"] = 1


        if "new" in request.form:
            completedprompt = generate_image()

        if "dicerollbutton" in request.form:
            multiplier = 1
            rolleddice = f"{random.randint(1,6)}"
            completedprompt = "You chose to drink instead!       Drink the amount the dice says!"

            session["progbarvalue"] += int(rolleddice)

            if session["progbarvalue"] >= 50:
                session["progbarvalue"] = 1
                multiplier = 3
                
            return render_template("drikke.html", 
            result=completedprompt,
            dice = int(rolleddice)*multiplier,
            progBarHtml = session["progbarvalue"])
    
        if "addplayerbutton" in request.form:
            completedprompt = addName()

        if "clear" in request.form:
            completedprompt = clear_names()
            
    return render_template("drikke.html", result=completedprompt,dice = rolleddice,progBarHtml=session["progbarvalue"] )
    


if __name__ == '__main__':
    app.run(debug=True)