# Pixel-Pirates

## Delivery 6
## Anora
### In Progress
1. fixing dropdown duplication for profile page
2. fixing creating campaign/news/rewards
   
### Done
1. django-celery-beats for scheduling daily tasks and weekly tasks
2. streaks calendar and calculating streaks
3. celery -A Pixel_Pirates.celery worker --beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler 
    - run this command along with runserver 

## Grace
- working on
    - photo upload to compelte task
    - finish word search and integrate with tasks (not just views) and make interactive with javascript
    - article quiz
- done
    - campaign, news, and rewards items are saved to database and show up on home page
    - fix links for items on home page
    - word search code and css

## Leah (currently tackling these -- mostly logic/buggy parts)
- Leader ranking
    - If user has the same number of points, who is going to be first? DONE
    - Where the user falls on the table sometimes does not match the motivation message (tied to if user has the same number of points, who is going to be first) DONE
- Hamburger menu: when the user is on a mobile interface, the side bar will disappear DONE
- Responsiveness/bootstrap:
    - Rewards page DONE
    - Campaign/rewards/news (should all be relatively simple because they have the same layout) DONE
 - Campaign is not being added to news page on homepage even when checkbox for add to news is true DONE

## Other
- Wordsearch
- Photo upload
- Supervisor Landing Page
- A Django superuser will have access to a webpage where they can define that a register user is a supervisor DONE


## Delivery 5
## anora
### In Progress
1. working on creating tasks on action page using celery beats to create a schedule so that the task refreshes every day (starting with daily tasks first)
2. when using celery, run the command: celery -A Pixel_Pirates.celery worker --beat --loglevel=info, with runserver (not sure if this works yet still figuring it out)
3. opening each task
4. assign points to users when task are completed
5. currently when the user first sign up, when they fill in the required information on the profile page, they have to save twice to access the sidebar, will fix this
6. for the actions, some of them dont show up when signing in: 
   - python manage.py update_tasks
      - manally adds the actions

## leah
### In Progress
2. Make campaigns once listed on landing page editable *works but might change to pop-up for more efficiency* fix CSS for it because wonky
3. User can see where they are on ranking even if not on top 50 -- wonky
4. Logic for if users have the same number of points (also is leaderboard tracking total number of points so points won't be deducted when they exchange for rewards
5. Start mobile interface (home and profile are responsive)
6. Make sidebar disappear when mobile - hmaburger

## meg
### in progress
1. Work with Jason to get the new rewards item to show up in rewards page
2. Points to show up on rewards and subtracting them when rewards redeemed
3. Show completed tasks on rewards page and points gained 
4. Show redeemed rewards and points subtracted

### done
1. create new form to create rewards item

## Delivery 4

## leah
### DONE
1. Landing page: Dynamic leaderboard with test users (used chart.js)
2. Ranking 
3. html for landing page

## grace
### DONE
1. created new page with html and css to allow admin to choose what action item to create
2. created new page with html and css to create news item  
3. added campaign items with news attribute to news section of home page


## anora
### DONE
1. created the basic layout for the campaign page 
2. restricted the campaign page to superusers only
3. found a problem for creating new users (it took them to a signup page instead of directly log in) - working on allowing the users create a profile directly based on google authentication
4. finish the html for campaign page


## meg
### DONE
1. separated html and css
2. made sure graduation year was mandatory
3. showing mandatory fields on the front end of profile page
4. added requirement (djqando-multifieldselect)
5. made sure graduation year was not already selected for a new user (makes them fill it out themselves instead of already selecting 2024)

### NEED TO DO
1. make majors and minors a drop down list
