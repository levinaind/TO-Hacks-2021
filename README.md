# 🏙 TO-Hacks-2021: TraceNext 
## 💡 Inspiration
The pandemic taught us one thing: We’re not ready for another one. We aim to prepare us if and when the next comes by harnessing the full potential of contact tracing.

Most countries elected for lockdowns whenever COVID-19 cases surge. While effective, lockdowns are also unsustainable in the long-run. Some countries, like South Korea and Singapore, have implemented a rigorous contact-tracing software at the expense of their citizens’ privacy. **We believe this tradeoff is not a necessary one 😲**



## 🧐 What it does
Our web application can help alert people if they have been in contact with someone who has tested positive for COVID-19. The users can do this by logging places they’ve been in for the last 30 days, as well as declaring whether they have tested positive for COVID-19 🦠 and whether they’ve been vaccinated 💉 

In case a user declared a positive result in a location, all users who were visiting on the same day will be notified 📩. This will help in curbing transmission rates, while making life as normal as possible. Since users log the places they’ve been in themselves, it also guarantees privacy 🔒 for users who are conscious of it.



## ⚙️ How we built it
We built our web application with _Flask_. We used basic _HTML_, _CSS_, and _JavaScript_ in order to make a responsive web app. In addition, we integrated _Google Maps API_ in order to allow users to add the locations they have visited in the past 30 days.

We stored, manipulate, and access our users' data with _PostgreSQL_. We also implemented Courier in order to notify any users that have been in contact with those that are positive.


## 💩 Challenges we ran into
Most of us are new to the coding world, in fact half of our team are joining a hackathon for the first time 🐣! One of our challenges was to develop an idea appropriate to our coding abilities.

We were also experimenting using new frameworks and tools, which we spent the majority of our time trying to figure out 😫 Implementing records to databases, figuring out how to integrate Google Maps API, and connecting our static pages with Flask were some of the struggles we faced the past 24 hour.


## 🏆 Accomplishments that we're proud of
We were proud to be able to design a UI, integrate the database as well as the Maps API, and made a responsive web app! This is a huge milestone for us as we were able to create an interactive web application from scratch despite being beginner programmers.

## 📚 What we learned
We learned that you can actually get a lot of things done in just 24 hours! Other than that, we were also able to hone our existing knowledge, as well as integrate cool, new APIs 😎 with the help of mentors and sponsors!

## 🔮 What's next for TraceNext
The possibilities are endless! While we do hope that the next pandemic never happens, it almost certainly will. When that time comes, we believe an effective contact-tracing program can help minimize the spread of the pathogen, without long-term lockdowns and sacrificing privacy 🥳.

Future developments may include:
 - **A mobile app that uses QR codes to be scanned by businesses** 📱
   - Allows users to log their movements automatically, while still having full knowledge of when and where they are tracked
   - Allows businesses to protect their employees and comply with governmental regulations, without the hassle of making a guest book or Google forms to log patrons’ data
- **More privacy features** 🕵🏾‍♀️
  - An option for users and businesses to encrypt or store their data locally on their device, only using them to notify patrons in case of a confirmed outbreak
- **Extra features** 🐶
  - Uses the data acquired to identify clusters and focus lockdowns on areas who really need them
  - Allows vaccinated users to use the mobile app as a vaccine passport by collaborating with healthcare providers for verification





