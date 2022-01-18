# madcamp_pj3_backend
Submodule for [madcamp_pj3](https://github.com/woojinnn/retravel). Responsible for backend stuffs.

---
## Development Envrionment
- `Django`
    - `DRF` (Django-Rest-Framework package)
    - `django-rest-knox` for authentication
- Database
    - SQLite
- Insomnia for testing HTTP request
- Testing server spec:
    - Ubuntu 18.04.2 LTS
    - Kernel version:  
        Linux camp-20 4.15.0-166-generic #174-Ubuntu SMP Wed Dec 8 19:07:44 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
---
</br>

## Databse Schema
Used Relational databse, sqlite3 for this project.
- User
    - Inherits django user model, `AbstractUser`
    - For more information, refer to `users/models.py`, and `users/serializers.py`

    |Key|Type|Details|
    |------|---|---|
    |id||Obejct id|
    |username|TextField|user Id|
    |nickname|TextField|user name|
    |password|TextField|user password|
    |detail|TextField|user detail information (not used)|
     </br> 

- Post
    - For more information, refer to `posts/models.py`, and `posts/serializers.py`

    |Key|Type|Details|
    |------|---|---|
    |id||Obejct id|
    |author|Foreign Key|User|
    |contents|TextField|descrption of post|
    |publish_date|DateField|day when the post was published|
    |travel_date|TextField|Travel date<br>Was originally DateField|
    |city|CharField|City name of travel place|
    |expense|PositiveIntegerField|expense of travel|
    |like_users|ManyToManyField|List of users that liked post|
    |place|TextField|exact place where you traveled|
    |latitude|FloatField|latitude|
    |longitude|FloatField|longitude|
    |image|ImageField|Image|
     </br> 

---
</br>

## API Specification
- For login-required api, you should specify token of user
- I implemented more apis for this project, but in this README file, I'll just write down APIs that I actually used for this project.
- User
    |HTTP|URI|Body Contents|Login-Required|Explanation|
    |----|---|-------------|--------------|-----------|
    |POST|/api/auth/register|username<br>nickname<br>password|X|Sign in|
    |POST|/api/auth/login|username<br>password|X|Login|
    |POST|/api/auth/logout||O|Logout|
- Post
    |HTTP|URI|Body Contents|Login-Required|Explanation|
    |----|---|-------------|--------------|-----------|
    |GET|/api/auth/all-posts||X|Get all posts|
    |POST|/api/posts/create-post|contents<br>travel_date<br>city<br>expense<br>place<br>latitude<br>longitude<br>image|O|create new post|
    |GET|/api/posts/get-user-post||O|get posts that user wrote|
    |GET|/api/posts/get-user-post/:city||O|get posts that user wrote<br>(filtered with city)|
    |GET|/api/posts/get-traveld-cities||O|get cities that users have traveled|
    |GET|/api/posts/top-liked-posts||X|get the list of posts that is sorted with likes|
    |GET|/api/posts/top-liked-cities||X|get the list of cities that is sorted with cities|
    |POST|/api/posts/like/:post_id||O|like post of post_id|
    |POST|/api/posts/unlike/:post_id||O|unlike post of post_id|
    |POST|/api/posts/get-city-posts/:city||X|get posts realted to city|
- For more information, refer `retravel/urls.py`, `users/urls.py`, `posts/urls.py`