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