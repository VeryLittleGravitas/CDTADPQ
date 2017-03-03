# CA Alerts, made with Very Little Gravitas for CDT RFI # CDT-ADPQ-0117

[CA Alerts](https://alerts-ca.herokuapp.com) ([https://alerts-ca.herokuapp.com](https://alerts-ca.herokuapp.com)), submitted by Very Little Gravitas LLC for the California Department of Technology [Digital Services Agile Development Prequalified Vendor Pool Refresh](https://github.com/CDTProcurement/adpq) for CDT RFI # CDT-ADPQ-0117.

## 1. CA Alerts

[CA Alerts](https://alerts-ca.herokuapp.com) is a faster, clearer, simpler way for California residents and visitors to be notified of emergencies affecting them and for State emergency workers to assess and inform the public about emergencies.

Ths prototype is based on our experience delivering digital services that meet user needs and are simple and intuitive enough so users succeed first time.

Where appropriate, we've [applied the plays from the US Digital Services Playbook](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/US-Digital-Services-Playbook).

### California residents and visitors can use CA Alerts to:

* sign up quickly and easily, by only requiring a phone number and zipcode
* receive timely emergency and non-emergency alerts to keep themselves, their loved ones and the people they're responsible for safe
* choose a location (a zipcode) to receive emergency and non-emergency alerts for
* receive alerts by SMS or email (with forthcoming push notification functionality)

### Authorized State emergency workers can use CA Alerts to:

* publish automatic fire alert emergency notifications to registered users whose location is within a 50 mile geofence of a fire, so the public are notified about nearby fire emergencies
* visualize up-to-date data on fire, river gauge, weather hazard, earthquake, tsunami and other natural hazards from the U.S. Geological Survey, National Oceanic and Atmospheric Administration and the U.S. Department of Interior in California or may affect California, so they can assess and make decisions about publishing emergency or non-emergency notifications
* publish manual emergency and non-emergency notifications, so the public can be informed about emergency and non-emergency situations
* track and analyze data about published notifications and public users

### Logging in as an Authorized State emergency worker

* Request the prototype Authorized User username and password by sending an email to: <a href="mailto:ca-alerts-support@verylittlegravitas.com?subject=CA Alerts Admin Request">ca-alerts-support@verylittlegravitas.com</a> with the subject "CA Alerts Admin Request".

## 2. Our Team

The Product Manager, Dan Hon, also served as Product Owner in the agile delivery process. We assigned him the leader of the project, with full responsibility and authority to build the prototype. He had full accountability for the quality of the prototype.

We assembled our multidisciplinary team based on our experience and [GSA 18F Agile Labor Categories](https://pages.18f.gov/agile-labor-categories/):

* **Product Manager**: Dan Hon, [@danhon](https://github.com/danhon) and [LinkedIn](https://www.linkedin.com/in/danhon/)
* **Technical Architect**: Michal Migurski, [@migurski](https://github.com/migurski) and [LinkedIn](https://www.linkedin.com/in/michalmigurski/)
* **Interaction Designer / User Researcher / Usability Tester**: Frances Berriman, [@phae](https://github.com/phae) and [LinkedIn](https://www.linkedin.com/in/fberriman/)
* **Backend Web Developer**: Erica Kwan, [@pui](https://github.com/pui) and [LinkedIn](https://www.linkedin.com/in/ericakwan/)
* **Delivery Manager**: Kay Chung, [@kerrching](https://github.com/kerrching) and [LinkedIn](https://www.linkedin.com/in/kerrching/)

## 3. Agile Delivery Process

The agile delivery process used at Very Little Gravitas is based on the open standards Scrum framework, with input and iterative feedback from user-centered design techniques.

Our wiki documents our [full agile delivery process](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Agile-Delivery-Process).

For this RFI, we implemented a simplified process, appropriate to scope and available time. The following describes the work delivered in each of the four 1 week sprints completed in building the prototype.

#### Sprint 1
* Defined usecases & personas
* Discussed and clarified requirements
* [User research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)
* [Design exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Design-exploration)
* [Technical exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Technical-exploration)
* Set up a Slack group for team communication
* Set up a [kanban board](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1) in the team’s repository as a lightweight product backlog and sprint task board

#### Sprint 2

* User interface and user flow visualizations
* Set up page templates
* User profile creation and management
* Emergency notification send and receive - test

#### Sprint 3

* Set up step-through templates for admin view
* Notification signup
* Edit geo-location criteria for notifications
* Selection of delivery format - SMS and email
* Implemented Google Analytics
* Reassess issue priorities and assign [stretch](https://github.com/VeryLittleGravitas/CDTADPQ/issues?q=is%3Aissue+is%3Aopen+label%3AStretch) label to stories out of prototype scope 

#### Sprint 4

* Finalized prototype documentation
* Finalized copy for the prototype application
* Customer support contact and issue reporting for user
* Administrator user research
* Implement email delivery 
* Implement administrator map interface improvements
* Reassess issue priorities and assign [stretch](https://github.com/VeryLittleGravitas/CDTADPQ/issues?q=is%3Aissue+is%3Aopen+label%3AStretch) label to stories out of prototype scope 

[TODO - add more]


## 4. User-Centered Design

We used these user-centered design techniques:

1. [User surveys](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal), to better understand the expectations of a wide number of potential users of our system (quantitative research)
2. [Personas](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Personas), to create representative archetypes of our users
3. [Interviews](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#interview-diary), to ask in more detail focussed questions about user expectations (qualitative research)
4. [Interactive user testing](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#user-testing-remote-week-3), to see if real users could successfully use our service

## 5. Written Technical Approach

CA Alerts is a Python 3 web application built using the Flask micro web framework. Users use the application via a web front-end that uses the U.S. Web Design Standards pattern library.

On the [CA Alerts homepage](https://alerts-ca.herokuapp.com), users can:

* register
* sign in
* sign in as an administrator

The application router [\_\_init\_\_.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/web/__init__.py) defines the addresses/routes and HTTP methods implementing the application's functionality. HTTP methods (GETs, POSTs etc) on routes result in running the appropriate code. Routes are rendered in HTML by the Jinja templating engine. The Python module [Psycopg](http://initd.org/psycopg/) is used to connect to the application database. The application database is a PostgreSQL database with the PostGIS extension for geolocation support.

Following the separation of concerns pattern, certain application functionality imported through Python modules in the application's [data](https://github.com/VeryLittleGravitas/CDTADPQ/tree/master/CDTADPQ/data) directory:

* [users.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/users.py) (create, read, update, delete (CRUD) user methods on the application database, verify user identity via appropriate Twilio and Mailgun APIs, managing user profile information etc.)
* [zipcodes.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/zipcodes.py) (return a zipcode for a given latitude and longitude)
* [wildfires.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/wildfires.py) (wildfire data parsing, storing wildfire information in the application database, returning a list of current fires, returning individual fires)
* [notify.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/notify.py) (notification functions, setting up third party API credentials, returning a list of geofenced users to notify, send notifications via third party APIs, notification logging)

Public users [register](https://alerts-ca.herokuapp.com/register) by entering a phone number and a zipcode in an HTML form. The zipcode is entered manually or retrieved using the HTML geolocation API. 

Submitting the form as an HTTP POST to the application web server calls the appropriate route to 

* create an (unregistered) user in the application database
* generates a PIN confirmation code
* send the PIN confirmation code via the Twilio SMS API to the user phone number
* redirect the user browser to a confirmation URL

The user enters their confirmation code at a unique confirmation URL to verify their phone number.

Verified public users (who have entered the correct PIN code) may edit their profile and add an email address. If they choose to receive notifications by email, the Mailgun API is used to deliver email notifications.

Public user login is two-factor authentication. Users log in by supplying something they know (a confirmation code sent by email or SMS) and something they have (access to a phone number or email address). 

[Admin users](https://alerts-ca.herokuapp.com/admin/) manually publish notifications using an HTML form. An emergency notification HTML form is HTTP POSTed to the appropriate route creating a notification object, calling the required functions to send notifications using the appropriate APIs and logs the notification in the application database.

Emergency and related data is displayed using a [Leaflet.js](http://leafletjs.com) map interface on the CA Alerts homepage and in the Admin interface. The  application uses a Python object representing emergency data, generated from emergency data stored in the application database. The object is serialized to JSON and delivered inline in the HTML response by the application server when a browser requests a page containing the map template.  

On the backend, a scheduled task provided by our PaaS (Heroku) runs a collection script ([collect.py](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/CDTADPQ/data/collect.py)) every hour to

* GET the data at the provided URLs from the prototype data source ESRI feature servers
* store returned data in the application database
* identify users within 50 miles of fire points within California
* send emergency notification to those users
* log sent notifications

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

c. We surveyed over 30 potential users of the service, and conducted detailed interviews with a number of individuals. Insights from these exercises were used directly in design exploration and reflected in the implementation of requirements. See our [research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal).

d. We used 4 user-centered design techniques in [Section 4](https://github.com/VeryLittleGravitas/CDTADPQ#4-user-centered-design) (above).

e. The project [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master) is in Github.

f. We used Swagger to document the 1 API for this product [returning a zipcode for a given latitude and longitude](https://alerts-ca.herokuapp.com/api/).

g. Our [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master) shows how user-facing templates were implemented using standards compliant, accessible, semantic HTML using [Progressive Enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement). The U.S. Web Design Standards were used, which are [fully compliant with ADA and WCAG 2.0](https://standards.usa.gov/getting-started/designers/#notes-on-accessibility)

h. We used the [U.S. Web Design Standards](https://standards.usa.gov/) as style guide and/or pattern library. [Pull Request 13](https://github.com/VeryLittleGravitas/CDTADPQ/pull/13) shows initial implementation.

i. Our [research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) documents usability testing videos and notes from interviews.

j. The lightweight scrum process we used provided a review point at the end of each sprint, enabling us to reflect users' feedback in the planning session of the next sprint. We iteratively produced features reflecting real users' requirements. See [Section 3](https://github.com/VeryLittleGravitas/CDTADPQ#3-agile-delivery-process) (above) for further detail.

k. Using the U.S. Web Design Standards with no custom HTML or CSS ensures a responsive design on multiple devices.

l. We are using the following modern, open-source technologies:

1. Our prototype is written in [Python 3](https://www.python.org/download/releases/3.0/).
2. [Flask](http://flask.pocoo.org), a micro web framework for Python based on [Werkzeug](http://werkzeug.pocoo.org/docs/0.11/), the WSGI toolkit, and [Jinja 2](http://jinja.pocoo.org/docs/2.9/), a templating language based on Django's templating approach. The Flask framework also features integrated support for unit testing and RESTful request dispatching.
3. [PIP](https://pip.pypa.io/en/stable/) for ensuring the correct Python packages are installed to support the application
4. [PostgreSQL 9](https://www.postgresql.org), an enterprise-grade database used by government agencies in the U.S. such as The National Weather Service, the Centers for Disease Control and Prevention and State Department.
5. [psycopg](http://initd.org/psycopg/) as the PostgreSQL adapter for Python.
6. [Swagger](http://swagger.io) to document APIs
7. [PostGIS](http://www.postgis.net), a spatial database extender for the Postgres database. PostGIS adds support for geographic objects, allowing for location queries to be run in SQL.
8. [Leaflet.js](http://leafletjs.com), an open-source JavaScript library for interactive maps
9. The [U.S. Web Design Standards](https://standards.usa.gov), which provides design guidelines and code to quickly create trustworthy, accessible and consistent digital government service, meeting Web Content Accessibility Guidelines.
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

m. We use [Heroku](https://www.heroku.com) as PaaS provider. [Issue 3](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) shows inital setup of the Heroku deployment pipeline. The master branch is automatically deployed to [https://alerts-ca.herokuapp.com](https://alerts-ca.herokuapp.com).

n. We have a [master list of unit tests](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/test.py) and automated tests are run by Travis CI, [build and test results are public](https://travis-ci.org/VeryLittleGravitas/CDTADPQ/builds)

o. [Travis CI](https://travis-ci.org) provides continuous integration, automatically and continuously deploying the master branch to [https://alerts-ca.herokuapp.com](https://alerts-ca.herokuapp.com). [Issue 3](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) documents initial setup.

p. **Setup or used configuration management;**

[TODO: dependent upon [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95).]

q. CA Alerts is continuously monitored using Pingdom with a [public uptime report](http://stats.pingdom.com/qp87mnx745hc/2571878).

r. CA Alerts has been built with Docker: a single Docker image includes PostgreSQL, the CA Alerts web application and required dependencies. The production application is deployed on the Heroku PaaS. Learn how to [use the Docker image](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Use-the-Docker-image).

s. Learn how to [install and run the prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype).

t. Our work and code for this prototype is licensed under the [MIT License](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/LICENSE).
