# IS213-G9T7

## Local Testing Guide
1. ensure all dependencies installed (require npm, vue-cli, firebase-admin, vue-router, bootstrap-icons)
2. cd into /microservices
3. go into the docker-compose.yml file and change the dockerid parts in the image names
    - eg (if your docker id is bob, change "image: rafeang/attraction_details:esd" to "image: bob/attraction_details:esd")
3. run ```docker-compose up```
4. cd into /frontend
5. run ```npm run serve```
6. admin accounts:
    - email: admin@dbtt.com | password: dbttleggo36969
    - email: admin@esd.com | password: esdleggo36969
7. test customer accounts:
    - email: rafe.ang@gmail.com | password: rafeang
    - email: hello@world.com | password: helloworld
    - email: test@test.com | password: testytest
    - feel free to create your own test accounts. view all accounts in firebase console

## Microservices
1. Refer to <a href='https://docs.google.com/document/d/1MTwUEjCK1cy_RJsjDjIc4_K0mHl2sd4ZuBxzTuGbDP4/edit?usp=sharing' target='_blank'>this</a> documentation for endpoints, return values and port info of all the microservices
2. Refer to <a href='https://lucid.app/lucidchart/invitations/accept/78e2006a-6154-4140-96c9-586eb50cd397' target='_blank'>this</a> for a visual reference of all the scenarios
3. Atomic Microservices (only they can access their respective Firestore Collections)
    - Attractions (Who's currently queueing for which ride)
    - Customers (Customer data and queue status)
    - Attraction Details (Ride info. Currently it's only name and whether the ride is indoors / outdoors)
    - Queue Logs (Store all the logs of who joins / leaves / gets removed from which queue and at what time) **AMQP
4. Complex Services
    - Join Queue (Check if customer is in queue, if not, add him to the queue and change his queue status) **AMQP
    - Update Queue (For customer to leave queue / admin to remove one or more people from the queue and change their queue status) **AMQP
    - View Status (Returns either the number of people in queue or number of people in front of the customer if he's in the queue)
    - Weather Check (Call Weather API to see if forecast of thunder: lightning risk, outdoor rides must cease)
    - Dashboard (Aggregates Queue Log Data and returns necessary info for frontend chart rendering with ChartJS)

## Frontend
1. Frontend uses firebase for authentication, vue router for page routing, and const store for state management
2. App.vue and main.js are the main vue and javascript files
3. Views: The different pages. 
    - Welcome.vue: Login page (/)
    - Gallery.vue: Attractions Gallery for Customers (/gallery)
    - Panel.vue: Admin Control Panel (/panel)
4. Components: Nested within views. 
    - AdminLogin.vue: Admin Login Form (used in '/')
    - LoginForm.vue: Customer Login Form (used in '/')
    - RegisterForm.vue: Registration Form (used in '/')
    - AttractionCard.vue: Card showing the wait time, queue length, availability (weather), join queue button and leave queue button. (used in '/gallery')
    - QueueCard.vue: Similar to AttractionCard.vue, except you can see who is in which queue and remove them. (used in '/panel')
5. Router
    - index.js need to register views here when u want to add a new endpoint page to the site 

## To-do / Ideas for extending project
1. Scheduler Microservice for scheduled rides and fine-grained, realtime tracking of customers on rides
2. Websocket to replace polling (expensive)
3. Notifications Microservice for when your turn is about to arrive (currently, we're simulating notifications with a simple JS alert)
