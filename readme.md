# Hello, world

## 1. Prototype B

The working prototype will be an application that will allow California residents to establish and manage their profile and receive emergency and non-emergency notifications via email, Short Message Service (SMS), and/or push notification based on the location and contact information provided in their profile and/or the geo-location of their cellphone if they have opted in for this service. In addition, the working prototype will provide the authorized administrative users with the ability to publish notifications and track, and analyze and visualize related data. The working prototype does not need to implement any authentication or authorization against an external directory or authentication mechanism.

[TODO: INSERT INTRO, WHAT DOES IT DO & WHAT VALUE DOES IT ADD]

Our approach is consistent with both the [ADPQ RFI] (https://github.com/CDTProcurement/adpq/blob/master/RFI%20CDT-ADPQ-0117%20-%20PQVP%20DS-AD%20-%20Final%20%2002.06.17.pdf) requirements and the [US Digital Services Playbook] (https://playbook.cio.gov).


## 2. The Team

The Product Manager, Dan Hon, also served as Product Owner in the agile delivery process. He was the assigned leader of the project with responsibility and accountability for the quality of the prototype. 

Composition of the multi-disciplinary team (based on GSA 18F Agile Labor Categories): 

**Dan Hon, Product Manager**

@danhon [LinkedIn Profile](https://www.linkedin.com/in/danhon/)

**Michal Migurski, Technical Architect**

@migurski [LinkedIn Profile](https://www.linkedin.com/in/michalmigurski/)

**Frances Berriman, Interaction Designer / User Researcher / Usability Tester**

@phae [LinkedIn Profile](https://www.linkedin.com/in/fberriman/)

**Erica Kwan, Backend Web Developer**

@pui [LinkedIn Profile](https://www.linkedin.com/in/ericakwan/)

**Kay Chung, Delivery Manager**

@kerrching [LinkedIn Profile](https://www.linkedin.com/in/kerrching/)


## 3. Agile Delivery Process

The agile delivery process used at Very Little Gravitas is based on the open standards Scrum framework, with input and iterative feedback from user-centered design techniques. 

Documentation on the [full agile delivery process](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Agile-Delivery-Process)

For the purposes of the ADPQ submission, we implemented a simplified process, appropriate to the scope and available time. 
The following describes the four 1 week sprints that were completed for the design and build of the prototype. 

#### Sprint 1
* Defined usecases & personas
* Discussed and clarified requirements 
* [User research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)
* [Design exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Design-exploration) 
* [Technical exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Technical-exploration)
* Set up a Slack group for team communication
* Set up a [kanban board](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1) in the team’s Github repo for use as a lightweight product backlog and sprint task board 

#### Sprint 2

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]

#### Sprint 3

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]

#### Sprint 4

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]


## 4. User-Centered Design 
We used a number of different user-centered design techniques in developing the prototype:

* [User survey](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal), to better understand the expectations of a wide number of potential users of our system (quantitative research)
* [Personas](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Personas), to create representations of our users
* [Interviews](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#interview-diary), to ask in more detail focussed questions about user expectations (qualitative research)
* [Interactive user testing](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#user-testing-remote-week-3), to see if our users are able to successfully use our service


## 5. Deployment Instructions 

See our documentation to [install and run the prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype)


## 6. Additional Material
* [Product Backlog and Sprint Taskboard](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1)
* [Project wiki](https://github.com/VeryLittleGravitas/CDTADPQ/wiki)

____

## Procurement Requirements

The RFI explicitly identifies 20 requirements (a-t) for the prototype submission. Without duplicating the headings, we provide evidence below of how we have met each criteria:

a. We appointed Dan Hon as both Product Manager and leader of the project. He helped the team understand the requirements, was responsible for prioritizing the work, and is ultimately accountable for the quality of the submitted prototype 

b. Section 2 (above) identifies the members of the multidisciplinary team and their specialisms. 

c. We surveyed over 30 potential users of the service, and conducted detailed interviews with a number of individuals. Insights gathered from these user research exercises were fed directly into the design exploration and reflected in the implementation of requirements.See the [research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) on the project wiki for further evidence.

d. We used the following user-centered design techniques to develop this prototype:

* [User survey](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal), to better understand the expectations of a wide number of potential users of our system (quantitative research)
* [Personas](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Personas), to create representations of our users
* [Interviews](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#interview-diary), to ask in more detail focussed questions about user expectations (qualitative research)
* [Interactive user testing](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal#user-testing-remote-week-3), to see if our users are able to successfully use our service

e. See the project [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master) in Github.

f. **Used Swagger to document the RESTful API, and provided a link to the Swagger API;**

We have created 1 API in this project that returns a zipcode for a given latitude and longitude. 

g. See the code repository for the specifics of how the user-facing templates were implemented [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master). They are written with standards complient, acessible, semantic HTML using [Progressive Enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement), directly using the U.S. Web Design Standards which are fully complient with ADA and WCAG 2.0. See [Pattern Library Accessibility Notes](https://standards.usa.gov/getting-started/designers/#notes-on-accessibility).

h. This project uses the [Draft U.S. Web Design Standards](https://standards.usa.gov/) as style guide and/or pattern library. See [Pull Request 13](https://github.com/VeryLittleGravitas/CDTADPQ/pull/13) for the initial implementation of the pattern library.

i. See [Research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) for evidence of usability testing videos, as well as notes from interviews.

j. The lightweight scrum process we used provided a review point at the end of each sprint, enabling us to reflect users' feedback into the grooming and planning session of the subsequent sprint. This has allowed us to iteratively produce features that reflect real users' requirements.

k. We have chosen to use the Draft U.S. Web Design Standards with no custom HTML. This pattern library was chosen to ensure the delivery of a responsive design that works on multiple devices.

l. We are using the following modern, open-source technologies for this prototype:

* Python 3](https://www.python.org/download/releases/3.0/)
* [Postgres 9](https://www.postgresql.org), an enterprise-grade database used by government agencies in the U.S. such as The National Weather Service, the Centers for Disease Control and Prevention and State Department. 
* [PostGIS](http://www.postgis.net), a spatial database extender for the Postgres database. PostGIS adds support for geographic objects, allowing for location queries to be run in SQL.
* The [U.S. Web Design Standards](https://standards.usa.gov), which provides design guidelines and code to quickly create trustworthy, accessible and consistent digital government services that meet Web Content Accessibility Guidelines.
* [Flask](http://flask.pocoo.org), a microfreamework for Python based on [Werkzeug](http://werkzeug.pocoo.org/docs/0.11/), the WSGI toolkit, and [Jinja 2](http://jinja.pocoo.org/docs/2.9/), a templating language based on Django's templating approach. 
* [Heroku](https://www.heroku.com/home) as our prototype's platform-as-a-service.
* [Travis CI](https://travis-ci.org), for continuous integration and testing. 

	To be added: 
	
	* AWS
	* Skyliner
	* Docker
	
m. This project is using [Heroku](https://www.heroku.com) as PaaS provider, see the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for the inital setup of the Heroku deployment pipeline.

We are currently automatically deploying the master branch to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com).

n. Our Github respository includes a master list of unit tests at https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/test.py

Automated tests are run by Travis CI, and the results are available at https://travis-ci.org/VeryLittleGravitas/CDTADPQ/builds

o. We are using [Travis CI](https://travis-ci.org) for continuous integration, automatically and continuously deploying the master branch to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com). See the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for initial setup.

p. **Setup or used configuration management;**

In-progress, dependent upon [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95).

q. **Setup or used continuous monitoring;**

In-progress, see [Issue 96](https://github.com/VeryLittleGravitas/CDTADPQ/issues/96).

r. **Deployed their software in an open source container, such as Docker (i.e., utilized operating-system-level virtualization);**

In-progress, see [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95).

s. Instructions on installation and running of the prototype can be found here: [https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype).

t. We have chosen the [MIT License](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/LICENSE) for this prototype.
