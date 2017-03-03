# CA Alerts, made with Very Little Gravitas for CDT RFI # CDT-ADPQ-0117

[CA Alerts](https://vlg-ctdadpq.herokuapp.com) ([https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com)), submitted by Very Little Gravitas LLC for the California Department of Technology [Digital Services Agile Development Prequalified Vendor Pool Refresh](https://github.com/CDTProcurement/adpq) for CDT RFI # CDT-ADPQ-0117.

## 1. CA Alerts

[CA Alerts](https://vlg-ctdadpq.herokuapp.com) is a faster, clearer, simpler way for California residents and visitors to find out about emergencies that may affect them and for State emergency workers to assess and inform the public about emergencies.

This prototype has been developed based on our experience in delivering digital services that meet user needs and that are simple and intuitive enough that users succeed first time.

Where appropriate, we have [applied the plays from the US Digital Services Playbook](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/US-Digital-Services-Playbook).

### For California residents and visitors, CA Alerts:

* lets users receive up-to-date emergency and non-emergency alerts so that they can keep themselves, their loved ones and the people they're responsible for safe
* lets users choose a location (a zipcode) for which they will receive emergency and non-emergency alerts
* lets users choose whether to receive alerts by SMS or email (with forthcoming push notification functionality)
* lets users sign up quickly and easily, by only requiring a phone number and a zipcode

### For authorized State emergency workers, CA Alerts:

* publishes automatic fire alert emergency notifications based on up-to-date data to registered users whose location is within a 50 mile geofence of a fire, so that the public are automatically notified about fire emergencies
* lets users visualize up-to-date data on fire, river gauge, weather hazard, earthquake, tsunami and other natural hazards from the U.S. Geological Survey, National Oceanic and Atmospheric Administration and the U.S. Department of Interior that is in California or may affect California, so that users can assess and make decisions about publishing emergency or non-emergency notifications
* lets users publish manual emergency notifications to all users, so that the public can be informed about emergencies
* lets users publish manual non-emergency notifications to all users, so that the public can be informed about non-emergency situations
* lets users track data about published notifications
* lets users track data about registered users

## 2. Our team

The Product Manager, Dan Hon, also served as Product Owner in the agile delivery process. We assigned him the leader of the project with full responsibility and authority to build the prototype, and he therefore has full accountability for the quality of the prototype.

We put together the following multidisciplinary team to build California Alerts, based on our experience and the [GSA 18F Agile Labor Categories](https://pages.18f.gov/agile-labor-categories/):

* **Product Manager**: Dan Hon, [@danhon](https://github.com/danhon) and [LinkedIn](https://www.linkedin.com/in/danhon/)
* **Technical Architect**: Michal Migurski, [@migurski](https://github.com/migurski) and [LinkedIn](https://www.linkedin.com/in/michalmigurski/)
* **Interaction Designer / User Researcher / Usability Tester**: Frances Berriman, [@phae](https://github.com/phae) and [LinkedIn](https://www.linkedin.com/in/fberriman/)
* **Backend Web Developer**: Erica Kwan, [@pui](https://github.com/pui) and [LinkedIn](https://www.linkedin.com/in/ericakwan/)
* **Delivery Manager**: Kay Chung, [@kerrching](https://github.com/kerrching) and [LinkedIn](https://www.linkedin.com/in/kerrching/)

## 3. Agile Delivery Process

The agile delivery process used at Very Little Gravitas is based on the open standards Scrum framework, with input and iterative feedback from user-centered design techniques.

Please see our documentation for our [full agile delivery process](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Agile-Delivery-Process).

For this RFI, we implemented a simplified process, appropriate to the scope and available time. The following describes the work delivered in each of the four 1 week sprints completed in building the prototype.

#### Sprint 1
* Defined usecases & personas
* Discussed and clarified requirements
* [User research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)
* [Design exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Design-exploration)
* [Technical exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Technical-exploration)
* Set up a Slack group for team communication
* Set up a [kanban board](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1) in the team’s Github repo for use as a lightweight product backlog and sprint task board

#### Sprint 2

* User interface and user flow visualizations
* Set up page templates
* User profile creation and management
* Emergency notification send and receive - test

#### Sprint 3

* Set up step-through templates for admin view
* Notification signup
* Edit geo-location criteria for notifications
* Selection of delivery format - sms and email
* Implemented Google Analytics

#### Sprint 4

* Finalized prototype documentation
* Finalized copy for the prototype application
* Customer support contact and issue reporting for user
[TODO - add more]


## 4. User-Centered Design
We used a number of different user-centered design techniques in developing the prototype:

* [User survey](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal), to better understand the expectations of a wide number of potential users of our system (quantitative research)
* [Personas](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Personas), to create representative archetypes of our users
* [Interviews](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#interview-diary), to ask in more detail focussed questions about user expectations (qualitative research)
* [Interactive user testing](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#user-testing-remote-week-3), to see if our users are able to successfully use our service

## 5. Technical description and narrative of code flow

CA Alerts is a Python 3 web application built using the Flask micro web framework. The web application front-end is implemented using the U.S. Web Design Standards pattern library with no alterations or custom CSS.  

When the user opens the CA Alerts home page, they can:

* register for alerts
* sign in
* sign in as an administrator

The application's web [__init__.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/web/__init__.py) file defines the addresses/routes and HTTP methods through which the application delivers functionality. Application routes are rendered in HTML for users using the Jinja templating engine built into the Flask framework. The application uses the Python module [Psycop](http://initd.org/psycopg/) to connect to the application Postgres database for data storage and retrieval.

Following the modern software engineering practice of separation of concerns, application functionality relating to the following areas is imported through Python modules stored in the application's data directory:

* [users.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/users.py) for functions such as returning user information from the application database, verifying user SMS identity via Twilio APIs, verifying user email address via Mailgun APIs, managing user profile information and so on
* [zipcodes.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/zipcodes.py) for functions such as returning a zipcode for a given latitude and longitude
* [wildfires.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/wildfires.py) for functions such as wildfire data parsing, storing wildfire information in the application database, returning a list of current fires, returning data about an individual fire
* [notify.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/notify.py) for notification functions, setting up third party API credentials, returning a list of geofenced users to notify, sending notifications via supported third party APIs, logging

Public users register to receive emergency alerts by submitting a phone number and a zipcode. The zipcode can be entered manually or is retrieved from a supported browser by the HTML geolocation API. Entering a phone number and zipcode results in an HTTP POST to the application web server, which creates an (unregistered) user in the application database, generates a PIN confirmation code and uses the Twilio SMS API to send the PIN confirmation code to the user's phone number. The user must then enter a code on a confirmation screen to verify their phone number.

Verified public users (who have entered the correct PIN code) may edit their profile and add an email address. If they choose to receive notifications by email, the Mailgun API is used to deliver email notifications.

We use the same confirmation system to perform public user login. There is no "password", just simple authentication. For an existing user to log in, they identify themselves with their phone number and we send a PIN code confirmation in the same flow as above. This acts as user verification for login.

[Leaflet.js](http://leafletjs.com) is used to display emergency data through a map interface on the CA Alerts homepage and in the Admin interface. Internally, the application uses a Python object that represents emergency data, retrieved from the emergency data stored in the application database. The Python object is serialized to JSON and delivered inline in the HTML response by the application server when a browser requests a page containing the map template.  

On the backend, the prototype data sources are all ESRI feature servers. We use a scheduled task provided by our PaaS (Heroku) to run a collection script ([collect.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/collect.py)) every hour to GET the data at the provided URLs and store it in our application database (our application database is a PostgreSQL database with the PostGIS extension to support location data).  


## 6. Deployment Instructions

* [Install and run the prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype)
* [Use the Docker image](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Use-the-Docker-image)


## 7. Additional Material
* [Project wiki](https://github.com/VeryLittleGravitas/CDTADPQ/wiki)
* [Design exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Design-exploration)
* [Research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)
* [US Digital Services Playbook approach](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/US-Digital-Services-Playbook)
* [Product Backlog and Sprint Taskboard](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1)

____

## Procurement Requirements

The RFI explicitly identifies 20 requirements (a-t) for the prototype submission. Without duplicating the headings, we provide evidence below of how we have met each criteria:

a. We appointed Dan Hon as both Product Manager and leader of the project. He helped the team understand the requirements, was responsible for prioritizing work, and is ultimately accountable for the quality of the submitted prototype

b. [Section 2](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/readme.md#2-our-team) (above) identifies each member of our multidisciplinary team and their labor category.

c. We surveyed over 30 potential users of the service, and conducted detailed interviews with a number of individuals. Insights gathered from these user research exercises were fed directly into the design exploration and are reflected in the implementation of requirements. See our [research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal).

d. We used the user-centered design techniques in [Section 4](https://github.com/VeryLittleGravitas/CDTADPQ#4-user-centered-design) (above).

e. The project [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master) is in Github.

f. We have used Swagger to document the 1 API for this product that [returns a zipcode for a given latitude and longitude](https://vlg-ctdadpq.herokuapp.com/api/)

g. See our code repository for the specifics of how the user-facing templates were implemented [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master). They are written with standards complient, acessible, semantic HTML using [Progressive Enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement), directly using the U.S. Web Design Standards which are fully complient with ADA and WCAG 2.0. See [Pattern Library Accessibility Notes](https://standards.usa.gov/getting-started/designers/#notes-on-accessibility).

h. This project uses the [Draft U.S. Web Design Standards](https://standards.usa.gov/) as style guide and/or pattern library. See [Pull Request 13](https://github.com/VeryLittleGravitas/CDTADPQ/pull/13) for the initial implementation of the pattern library.

i. See [Research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) for evidence of usability testing videos, as well as notes from interviews.

j. The lightweight scrum process we used provided a review point at the end of each sprint, enabling us to reflect users' feedback into the grooming and planning session of the subsequent sprint. This has allowed us to iteratively produce features that reflect real users' requirements. See [Section 3](https://github.com/VeryLittleGravitas/CDTADPQ#3-agile-delivery-process) (above) for further detail.

k. We chose the Draft U.S. Web Design Standards with no custom HTML or CSS to ensure a responsive design that works on multiple devices.

l. We are using the following modern, open-source technologies:

1. Our prototype is written in [Python 3](https://www.python.org/download/releases/3.0/).
2. [Flask](http://flask.pocoo.org), a micro web framework for Python based on [Werkzeug](http://werkzeug.pocoo.org/docs/0.11/), the WSGI toolkit, and [Jinja 2](http://jinja.pocoo.org/docs/2.9/), a templating language based on Django's templating approach. The Flask framework also features integrated support for unit testing and RESTful request dispatching.
3. [PIP](https://pip.pypa.io/en/stable/) for ensuring the correct Python packages are installed to support the application
4. [PostgreSQL 9](https://www.postgresql.org), an enterprise-grade database used by government agencies in the U.S. such as The National Weather Service, the Centers for Disease Control and Prevention and State Department.
5. [psycopg](http://initd.org/psycopg/) as the PostgreSQL adapter for Python.
6. [Swagger](http://swagger.io) to document APIs
7. [PostGIS](http://www.postgis.net), a spatial database extender for the Postgres database. PostGIS adds support for geographic objects, allowing for location queries to be run in SQL.
8. [Leaflet.js](http://leafletjs.com), an open-source JavaScript library for interactive maps
9. The [U.S. Web Design Standards](https://standards.usa.gov), which provides design guidelines and code to quickly create trustworthy, accessible and consistent digital government services that meet Web Content Accessibility Guidelines.
10. [Heroku](https://www.heroku.com/home) as our prototype's platform-as-a-service.
11. [Travis CI](https://travis-ci.org), for continuous integration and testing.
12. [Twilio](https://www.twilio.com) for sending SMS notifications to users.
13. [Mailgun](https://www.mailgun.com) for sending email notifications to users.
14. [Slack](https://slack.com) for team collaboration and chat.

To be added:

13. [Pingdom](https://www.pingdom.com) for continuous monitoring of the prototype website.
14. Amazon Web Services
15. [Skyliner](https://www.skyliner.io), to automate self-contained Production and QA environments on Amazon Web Services.
16. Docker

m. We use [Heroku](https://www.heroku.com) as PaaS provider, see the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for the inital setup of the Heroku deployment pipeline.

The master branch is automatically deployed to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com).

n. Our repository includes a master list of unit tests at https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/test.py

Automated tests are run by Travis CI, the results are available at https://travis-ci.org/VeryLittleGravitas/CDTADPQ/builds

o. We use [Travis CI](https://travis-ci.org) for continuous integration, automatically and continuously deploying the master branch to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com). See the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for initial setup.

p. **Setup or used configuration management;**

[TODO: dependent upon [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95).]

q. **Setup or used continuous monitoring;**

[TODO: see [Issue 96](https://github.com/VeryLittleGravitas/CDTADPQ/issues/96).]

r. CA Alerts has been built with Docker: a single Docker image includes PostgreSQL, the CA Alerts web application and required dependencies. The production application is deployed on the Heroku PaaS. Learn how to [use the Docker image](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Use-the-Docker-image).

s. Learn how to [install and run the prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype).

t. Our work and code for this prototype is licensed under the [MIT License](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/LICENSE).
