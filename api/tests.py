from django.test import TestCase
from .models import Category, Task, TaskAssigned, Log
from authentication.models import CustomUsers
from django.utils import timezone


class CategoryModelTestCase(TestCase):
    print("Running CategoryModelTestCase")
    def test_category_creation(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")


class TaskModelTestCase(TestCase):
    print("Running TaskModelTestCase")
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.task = Task.objects.create(
            title="Test Task",
            priority="Medium",
            category=self.category,
            progress="Open",
            endDate=timezone.now(),
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.priority, "Medium")
        self.assertEqual(self.task.category, self.category)
        self.assertEqual(self.task.progress, "Open")


class TaskAssignedModelTestCase(TestCase):
    print("Running TaskAssignedModelTestCase")
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user = CustomUsers.objects.create_user(
            email="test@example.com", password="test123"
        )
        self.task = Task.objects.create(
            title="Test Task",
            priority="Medium",
            category=self.category,
            progress="Open",
            endDate=timezone.now(),
        )
        self.task_assigned = TaskAssigned.objects.create(
            task=self.task,
            user=self.user,
            isOwner=False,
        )

    def test_task_assigned_creation(self):
        self.assertEqual(self.task_assigned.task, self.task)
        self.assertEqual(self.task_assigned.user, self.user)
        self.assertFalse(self.task_assigned.isOwner)


class LogModelTestCase(TestCase):
    print("Running LogModelTestCase")
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user = CustomUsers.objects.create_user(
            email="test@example.com", password="test123"
        )
        self.task = Task.objects.create(
            title="Test Task",
            priority="Medium",
            category=self.category,
            progress="Open",
            endDate=timezone.now(),
        )
        self.log = Log.objects.create(
            type="Test",
            task=self.task,
            user=self.user,
        )

    def test_log_creation(self):
        self.assertEqual(self.log.type, "Test")
        self.assertEqual(self.log.task, self.task)
        self.assertEqual(self.log.user, self.user)
