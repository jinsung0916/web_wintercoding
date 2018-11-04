# 설치/빌드 방법

1. git clone https://github.com/jinsung0916/web_wintercoding.git
2. virtualenv -python=python3 [파일이름]
3. source [파일이름]/bin/activate
4. pip install -r requirements.txt
5. python manage.py migrate & python manage.py makemigrations
6. python manage.py runserver
7. 웹브라우저나 Curl 등을 통해 http://localhost:8000으로 접속한다.  
8. python manage.py test 명령어로 테스트를 수행한다. (optional) 
   -  {프로젝트}/todo/test.py



# TODO API

HTTP로 통신한다.

- Server URL :  http://jinsung0916.pythonanywhere.com/

(Browsable API 사용 가능합니다.)

## Show Todo list API

모든 Todo 목록을 반환한다.

dueDate 와 priority 를 기준으로 정렬되어 반환한다.

### Request

```http
GET /todo
```

### Response

|        Status Code        | Description |
| :-----------------------: | :---------: |
|          200 OK           |   success   |
| 500 Interner Server Error |  sorry ^_^  |

성공일 때 response body는 JSON 형식이며 아래와 같다.

```
[{
	"id": 0,
	"title": "",
	"content": "",
	"priority": 3,
	"dueDate": null, 
	"isFulfilled": false
},...]
```



## Create Todo API

새로운 Todo를 생성한다.

### Request

~~~HTTP
POST /todo
Content-Type: application/json
~~~

~~~json
{
  "title": "",
  "content": "",
  "priority": 1,
  "dueDate": "YYYY-MM-DDThh:mm:ss"
}
~~~

|        Name         |          Type          |      Description      |
| :-----------------: | :--------------------: | :-------------------: |
|        title        |         string         |      Todo title       |
|       content       |         string         |     Todo content      |
| priority (optional) |        integer         |     Todo priority     |
| dueDate (optional)  | datetime format string | iso8601 format string |

### Response

|        Status Code        |    Description     |
| :-----------------------: | :----------------: |
|        201 Created        |      success       |
|      400 Bad Request      | invalid parameters |
| 500 Interner Server Error |     sorry ^_^      |

성공일 때 response body는 JSON 형식이며 아래와 같다.

```
{
    "id": 0,
    "title": "",
    "content": "",
    "priority": 1,
    "dueDate": "YYYY-MM-DDThh:mm:ss",
    "isFulfilled": false
}
```



## Show Todo Detail API

Todo 의 상세정보를 반환한다.

### Request

~~~HTTP
GET /todo/{Todo_id}
~~~

### Response

|        Status Code        |    Description     |
| :-----------------------: | :----------------: |
|          200 OK           |      success       |
|      400 Bad Request      | invalid parameters |
|       404 Not Found       |  invalid todo ID   |
| 500 Interner Server Error |     sorry ^_^      |

성공일 때 response body는 JSON 형식이며 아래와 같다.

```
{
    "id": {Todo_id},
    "title": "",
    "content": "",
    "priority": 3,
    "dueDate": "YYYY-MM-DDThh:mm:ss",
    "isFulfilled": false
}
```



## Update Todo API

Todo의 정보를 수정한다.

### Request

```HTTP
PUT /todo/{Todo_id}
Content-Type: application/json
```

```json
{
  "title": "",
  "content": "",
  "priority": 1,
  "dueDate": "YYYY-MM-DDThh:mm:ss",
  "isFulfilled": true
}
```

|          Name          |          Type          |      Description      |
| :--------------------: | :--------------------: | :-------------------: |
|    title (optinal)     |         string         |      Todo title       |
|   content (optinal)    |         string         |     Todo content      |
|  priority (optional)   |        integer         |     Todo priority     |
|   dueDate (optional)   | datetime format string | iso8601 format string |
| isFulfilled (optional) |        boolean         |  Todo fulfill status  |

### Response

|        Status Code        |    Description     |
| :-----------------------: | :----------------: |
|          200 OK           |      success       |
|      400 Bad Request      | invalid parameters |
|       404 Not Found       |  invalid todo ID   |
| 500 Interner Server Error |     sorry ^_^      |

성공일 때 response body는 JSON 형식이며 아래와 같다.

```
{
    "id": {Todo_id},
    "title": "",
    "content": "",
    "priority": 3,
    "dueDate": "YYYY-MM-DDThh:mm:ss",
    "isFulfilled": false
}
```



## Delete Todo API

Todo 를 삭제한다.

### Request

```HTTP
DELETE /todo/{Todo_id}
```

### Response

|        Status Code        |   Description   |
| :-----------------------: | :-------------: |
|      204 No Content       |     success     |
|       404 Not Found       | invalid todo ID |
| 500 Interner Server Error |    sorry ^_^    |



## Show expired Todo list API

마감기한이 지난 TODO에 대해 알림을 노출하기 위해 만료된 Todo 목록을 반환한다.



### Request

```http
GET /todo/expired
```

### Response

|        Status Code        | Description |
| :-----------------------: | :---------: |
|          200 OK           |   success   |
| 500 Interner Server Error |  sorry ^_^  |

성공일 때 response body는 JSON 형식이며 아래와 같다.

```
[{
	"id": 0,
	"dueDate": "YYYY-MM-DDThh:mm:ss"
},...]
```
