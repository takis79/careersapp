# Recruiting CRM

This project is the result of a personal project to understand Django framework. As an experiment, I worked with real recruiters that specialize in the tech industry to understand their needs. The result is a simple and efficient CRM tailored for recruitment processes. 

Sections:
- Companies: current or potential clients with hiring needs. 
- Jobs: hiring needs of companies (i.e., job openings)
- Contacts: people that work in companies, responsible for job openings 
- Skills: set of programming languages, frameworks or technologies related to a job oppening
- To-do list: actions that recruiters must complete in a specified date
 
![Django CRM](https://github.com/RodrigoVillatoro/recruiting_crm/blob/master/screenshot.png)

In all the sections, users can add, edit, delete entries. Users can also assign companies and tasks to other users.

There are many features that would still have to be implemented in order for this CRM to be a fully working one. To mention just a few of them:
- Search: recruiters can't search now for companies, jobs, etc. 
- Email integration: recruiters can't receive task reminders and can't email customers directly
- Calendar integrations: to schedule appointments or set up reminders
- Frontend improvements: right now the design is very basic, and definitely needs improvements

The code is written in Python 3.5, and uses the following libraries:
- Django
- django-crispy-forms
- mysqlclient 
