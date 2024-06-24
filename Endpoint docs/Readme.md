# Endpoints
- The root blueprint in the __init__.py folder in views stets the '/care' as the primary route for the endpoint request followed by the '/path-to-request' for the specific endpoints listed below under the api resources eg

localhost(url)/care/addusers - this is a post request to add a new user 

## Users (userviews.py)

### users sign up  (/addusers)
- This is a POST request that takes in the json below to add a new user 
{
    "fullname"
    "email"
    "password"
    "role" - on signup outomaticlly set to normal user
}

### users login (/login)
- This is a POST request that allows a registerd user to login takes in :
{
    "email"
    "password"
} 

on succesfull login it gives back:
{
    "access-token"
    "refresh-toke"
    "fullname"
    "role"
}

### Single user resource (/users/userID)
- These are  GET,PATCH,DELETE request 
Allows users to update details all expect their role(which is handled by (superAdmin.py)),Delete their account and get their account details

## Providers (providerviews.py)

## Add new provider (/newprovider)
- This is a POST requets 
Allows only registerd users to add a new provider which will be linked to their user account
takes in :

{
    "providerName"
    "email"
    "phoneNumber"
    "location"
    "services"
    "website"
    "providerType" : Only "Facility" or "Doctor"
    "bio"
    "workingHours"
    "profileImage"
    "user_id": outomatically picked from the current logged in user
    "status" : outomatically set to false can be updated to True
}

# view All provider (/provider)
-This is a GET request .
Shows all providers whose status is set to True (published to view for public)

