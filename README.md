# Makarakov
Markov chain trained on Homestuck full text.

Data from [readmspa](http://readmspa.org/search/search=6.html), trained using [markovify](https://github.com/jsvine/markovify).

Supports characters: Rose, Dirk, Vriska, Karkat, Roxy, Jade, Kanaya, Jane, Jake, Tavros, Dave, Caliborn, Calliope, Meenah, Terezi, John


## Usage
* Install dependencies (python3, bs4, markovify)
* Run scrape.py. This will take a while the first time while the models are generated. 
* Follow onscreen prompts to select character.


## Examples (try to figure out who's who!)
* But Strider is being obtuse, I can't explain why I go dark on your computer.
* Which is really bad for you. Published papers forthcoming.
* but i don't know what came over me there, i was on fire, and had amazing tales to tell.
* armageddon's gettin waged on us patriarchally like urban watermarks in the blanks myself for a while
* Are you in the daydreams of our reality. For me in particular. But also a bit of cheating, through the steps necessary to launch the session.
* That makes sense, but I'm not ready to get married and have babies!!!
* So we're a8out to start taking some steps all 8y yourself. I think I didn't hear anyone else want to 8e paying attention here, so feel free to look at them. They all seem so excited.
* Okay That Was Romantically Oriented
* BR1NG1NG H3R TO JUST1C3 1S CR1T1C4L TO 4LL DR34M BUBBL3S


(answers: Rose, Rose, John, Dave, Dirk, Jane, Vriska, Kanaya, Terezi)



## Planned Features
- [ ] Command-line tool (e.g makarakov karkat 100 -> 100 lines of karkat)
- [ ] Nice refactoring
- [ ] requirements.txt
