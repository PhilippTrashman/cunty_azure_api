# Documentation

## General Calls

### GET fortnite

`/api/fortnite`

Returns a funny woohoo message

### GET hello

`/api/hello`

Returns hello world, used for checking the server availability

### GET health

`/api/health`

Same as Hello but without returning a hello world

### POST login

`/api/login`

Body needs either the username or email of the user

``` json
{
    "username": "john.doe225",
    "password": "good-password"
}
```

Response includes user data

``` json
{
    "id": "some-uuid4",
    "name": "John",
    "last_name": "Doe",
    "birthday": "None",
    "username": "john.doe225",
    "email": "j.doe@example.com",
    "contacts": {
        "1": "05361-12345678"
    },
    "student": "student info or none",
    "teacher": "teacher info or none",
    "su": "su info or none",
    "absences": {
        "2": {"abscence": "object"}
    }
}
```

## User Calls

### GET Users

`/api/users`

Returns every user in the database

### POST Users

`/api/users`

Creates a new user, body needs to follow the following structure

``` json
{
    "username": "jane.doe",
    "password": "good-password-2",
    "email": "jane.d@example.com",
    "name": "Jane",
    "last_name": "Doe",
    "birthday": "2001-1-24"
}
```

### GET User

`/api/users/{username}`

Returns User with the given username, can also be email

### PUT User

`/api/users/{username}`

Update a users account, needs the username as identifier, body needs to follow the same as creating a user

Only elements that needs to be update need to be put into the body

### DELETE User

`/api/users/{username}`

Deletes the user, is **not reversible**, so use with caution

### GET User Contact

`/api/users/{username}/contact`  
Get the contact information of a User

### POST User Contact

`/api/users/{username}/contact`  
Post contact info for an account  
Body needs to look as follows:  

``` json
{
    "account_id": "users_uuid4",
    "contact_type": "optionally name contact type like email",
    "contact": "1234-5678901",
}
```

### GET User Student Information

`/api/users/{username}/student`  
Get a users student info

### POST User Student Information

`/api/users/{username}/student`
Create User info  
Body needs to look as follows  

``` json
{
    "account_id": "users_uuid4",
    "school_class_id": 23 // id of the school class
}
```

returned Object will look like this  

``` json
{
    "id": 1,
    "school_class_id": 23,
    "parents": "{}",
    "school_subjects": 
}
```

### PUT User Student Information

`/api/users/{username}/student`
Update a users student info  
Body needs to include the wanted changes, meaning the classes

``` json
{
    "school_class_id": 3
}
```

### DELETE User Student Information

`/api/users/{username}/student`
Deletes a users Student Information  
**not reversible** so use with caution

## Student Calls

### GET Students

`/api/students`
Get every student

### Get Student

`/api/students/{student_id}`
id is an Integer  
Returns the Student information associated with the id

## Parent Calls

### GET Parents

`/api/parents`
Returns every parent object in a summarized version

``` json
[
    {
        "id": 1,
        "account": {
            "id": "e259f12f-0cf1-4cb8-ae9e-4af45f784254",
            "name": "Mark",
            "last_name": "Bush",
            "birthday": "1910-07-02",
            "username": "Mark.Bush"
        }
    },
    {
        "...": "..."
    }
]

```

### GET Parent

`/api/parents/{parent_id}`
Returns an in depth parent object

``` json
{
    "id": 1,
    "children": {
       "1": {
           "id": 1,
           "student": {
               "id": 1,
               "school_class_id": 1,
               "account": {
                   "id": "11111111-1111-1111-1111-111111111111",
                   "name": "Test",
                   "last_name": "Student1",
                   "birthday": "2000-01-01",
                   "username": "testStudent1"
               }
           }
       },
       "2": {
           "id": 2,
           "student": {
               "id": 2,
               "school_class_id": 1,
               "account": {
               "id": "22222222-2222-2222-2222-222222222222",
                   "name": "Test",
                    "last_name": "Student2",
                   "birthday": "2000-01-01",
                   "username": "testStudent2"
               }
           }
       }
    },
    "account": {
       "id": "e259f12f-0cf1-4cb8-ae9e-4af45f784254",
       "name": "Mark",
       "last_name": "Bush",
       "birthday": "1910-07-02",
       "username": "Mark.Bush"
    }
}
```

## Teacher Calls

### GET Teachers

`/api/teachers`  
Returns every teacher in a summarized Object

``` json
[
    {
       "id": 1,
       "account": {
           "id": "7dfefc15-3625-4b95-ba1a-8f048a62a683",
           "name": "Nicholas",
           "last_name": "Clark",
           "birthday": "1948-04-06",
           "username": "Nicholas.Clark"
       }
    },
    {"..."}
]
```

### GET Teacher

`/api/teachers/{teacher_id}`  
Returns the full Teacher object  
Note that the object is rather large because of the include timetable, also called **school_subjects**
please try it out for yourself, because i wont include how the object looks as it take up way too many lines

## SU Calls

### GET SUs

### GET SU

## School Classes Calls

### GET School Classes

### GET School Class

### POST School Class

### PUT School Class

### DELETE School Class

## School Grade Calls

### GET School Grades

### GET School Grade

### PUT School Grade

### DELETE School Grade

## School Subject Calls

### GET School Subjects

`/api/school_subjects`  

### POST School Subject

`/api/school_subjects`  

### GET School Subject

`/api/school_subjects/{school_subject_id}`  
school_subject_id is an Int  

### PUT School Subject

### DELETE School Subject

## School Subject Entry Calls
