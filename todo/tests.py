# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todo.models import Todo
import pytz
from faker import Factory
from django.utils import timezone
import dateutil.parser

class TodoCreateTests(APITestCase):
    def setUp(self):
        fake = Factory.create()
        self.title = fake.text()[:100].strip()
        self.content = fake.text()[:500].strip()
        self.dueDate = fake.date()+"T"+fake.time()+"+09:00"

    """
    요구사항 1: 새로운 TODO(제목 + 내용)를 작성한다
    """
    def test_create_todo(self):
        url = reverse('todo-list')
        data = {'title': self.title, 'content': self.content}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, self.title)
        self.assertEqual(Todo.objects.get().content, self.content)

    """
    요구사항 2:사용자의 선택에 의해 TODO에는 마감 기한을 넣을 수 있다.
    """
    def test_create_todo_with_dueDate(self):
        url = reverse('todo-list')
        data = {'title': self.title, 'content': self.content, 'dueDate': self.dueDate}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.get().title, self.title)
        self.assertEqual(Todo.objects.get().content, self.content)
        self.assertEqual(Todo.objects.get().dueDate.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul')).isoformat(), self.dueDate)

    """
    (예외) title과 content가 없으면 Todo를 생성할 수 없다.
    """
    def test_create_todo_without_title_and_content(self):
        url = reverse('todo-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TodoUpdateTests(APITestCase):
    def setUp(self):
        self.fake = Factory.create()
        url = reverse('todo-list')
        data = {'title': self.fake.text()[:100].strip(), 'content': self.fake.text()[:500].strip()}
        self.response = self.client.post(url, data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    """
    요구사항 3: 우선순위를 조절할 수 있다.
    """
    def test_update_todo_priority(self):
        self.assertEqual(Todo.objects.get().priority, 3)

        url = reverse('todo-detail',  kwargs={'pk': self.response.data.get("id")})
        data = {'priority': 1}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get().priority, 1)

    """
    요구사항 4: 완료 처리를 할 수 있다.
    """
    def test_update_todo_isFulfilled(self):
        self.assertEqual(Todo.objects.get().isFulfilled, False)

        url = reverse('todo-detail',  kwargs={'pk': self.response.data.get("id")})
        data = {'isFulfilled': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get().isFulfilled, True)


    """
    요구사항 6: Todo 내용을 수정할 수 있다.
    """
    def test_update_todo(self):
        title = self.fake.text()[:100].strip()
        content = self.fake.text()[:500].strip()

        url = reverse('todo-detail',  kwargs={'pk': self.response.data.get("id")})
        data = {'title': title, 'content': content}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get().title, title)
        self.assertEqual(Todo.objects.get().content, content)

    """
    요구사항 7: Todo 항목을 삭제할 수 있다.
    """
    def test_delete_todo(self):
        url = reverse('todo-detail',  kwargs={'pk': self.response.data.get("id")})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)


class TodoExpiredTest(APITestCase):
    def setUp(self):
        fake = Factory.create()

        for i in range(100):
            title = fake.text()[:100].strip()
            content = fake.text()[:500].strip()
            dueDate = fake.date()+"T"+fake.time()+"+09:00"
            isFulfilled = fake.boolean()

            url = reverse('todo-list')
            data = {'title': title, 'content': content, 'dueDate': dueDate, 'isFulfilled': isFulfilled}
            self.response = self.client.post(url, data, format='json')

    """
    요구사항 5: 마감기한이 지난 Todo에 대해 알림을 노출한다.
    """
    def test_get_todo_expired(self):
        url = reverse('todo-expired')
        response = self.client.get(url)
        for data in response.data:
            self.assertTrue(dateutil.parser.parse(data.get("dueDate")) < timezone.now(), True)
