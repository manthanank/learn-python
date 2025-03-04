# Learn Python

Python is a versatile and powerful programming language that is widely used in various fields, including web development, data analysis, artificial intelligence, scientific computing, and more. This guide provides an overview of Python's syntax, features, and best practices to help you get started with programming in Python.

## Basic Syntax

### Variables and Data Types

Python's dynamic typing system makes it flexible and beginner-friendly. Variables are created when you assign a value and can change types during runtime.

Key concepts:

- Variables don't need explicit declaration
- Names are case-sensitive
- Must start with letter or underscore
- Can contain letters, numbers, underscores
- PEP 8 recommends snake_case for variable names

```python
# Variable naming and type demonstration
user_name = "John"     # snake_case naming convention
firstName = "Jane"     # camelCase (not recommended in Python)
_hidden = "secret"     # starts with underscore
MAX_VALUE = 100       # constants typically use UPPER_CASE

# Type checking and conversion examples
x = 42
print(isinstance(x, int))    # True
print(isinstance(x, (int, float)))  # True - multiple types

# Advanced type conversion
binary_str = bin(x)[2:]      # "101010"
hex_str = hex(x)[2:]         # "2a"
oct_str = oct(x)[2:]         # "52"
```

### Strings

Understanding string manipulation is crucial in Python. Strings are immutable sequences of characters with powerful built-in methods.

Best practices:

- Use f-strings for modern string formatting
- Consider performance when concatenating large strings
- Be aware of string immutability
- Use appropriate string methods instead of manual manipulation

```python
# Advanced string manipulation examples
text = "Python Programming"

# Slicing with step
print(text[::2])       # "Pto rgamn"
print(text[::-1])      # "gnimmargorP nohtyP" (reverse)

# String alignment
print(text.ljust(25, '*'))   # "Python Programming*******"
print(text.center(25, '-'))  # "---Python Programming---"

# String validation
print("abc123".isalnum())    # True
print("  \t\n".isspace())    # True
print("Title".istitle())     # True

# Advanced replacement
text = "The quick brown fox"
mapping = str.maketrans('aeiou', '12345')
print(text.translate(mapping))  # "Th2 q54ck br3wn f3x"
```

### Numbers

Python provides comprehensive support for different numeric types and mathematical operations. Understanding number handling is essential for calculations and data processing.

Important concepts:

- Integer precision is unlimited
- Float precision is system-dependent
- Complex numbers are built-in
- Decimal type for precise decimal arithmetic
- Fraction type for rational numbers

```python
# Advanced numeric operations
import math
import numpy as np
from decimal import Decimal, getcontext

# Precision control with Decimal
getcontext().prec = 6
d = Decimal('1') / Decimal('7')
print(d)  # 0.142857

# Advanced mathematical functions
print(math.isclose(0.1 + 0.2, 0.3))  # True
print(math.copysign(1.0, -0.0))      # -1.0
print(math.isfinite(float('inf')))    # False

# Statistics with built-in functions
numbers = [1, 2, 3, 4, 5, 6, 7]
print(sum(numbers))          # 28
print(min(numbers))          # 1
print(max(numbers))          # 7
print(sum(numbers)/len(numbers))  # 4.0 (mean)

# Using NumPy for advanced calculations
arr = np.array(numbers)
print(np.median(arr))        # 4.0
print(np.std(arr))          # Standard deviation
print(np.percentile(arr, 75))  # 75th percentile
```

### Boolean Operations

```python
# Comparison operators
x = 5
y = 10
print(x == y)   # False
print(x != y)   # True
print(x < y)    # True
print(x > y)    # False
print(x <= y)   # True
print(x >= y)   # False

# Logical operators
a = True
b = False
print(a and b)  # False
print(a or b)   # True
print(not a)    # False

# Identity operators
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1
print(list1 is list3)      # True (same object)
print(list1 is list2)      # False (different objects)
print(list1 is not list2)  # True
```

## Control Flow

### Conditional Statements

```python
# if-elif-else
x = 10
if x > 15:
    print("x is greater than 15")
elif x > 5:
    print("x is greater than 5 but not greater than 15")
else:
    print("x is 5 or less")

# Ternary conditional expression
age = 20
status = "adult" if age >= 18 else "minor"
```

### Loops

```python
# For loop with range
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

# For loop with list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
for i in range(10):
    if i == 3:
        continue    # Skip this iteration
    if i == 8:
        break       # Exit the loop
    print(i)

# Loop with enumerate (for index and value)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

## Data Structures

### Lists

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]

# Accessing elements
print(fruits[0])       # "apple"
print(fruits[-1])      # "cherry" (last element)
print(fruits[1:3])     # ["banana", "cherry"] (slicing)

# Modifying lists
fruits.append("orange")        # Add to end
fruits.insert(1, "blueberry")  # Insert at index
fruits.remove("banana")        # Remove by value
popped = fruits.pop()          # Remove and return last item
popped_idx = fruits.pop(0)     # Remove and return item at index
fruits.sort()                  # Sort in place
fruits.reverse()               # Reverse in place
sorted_fruits = sorted(fruits) # Return sorted copy
length = len(fruits)           # Get length

# List comprehensions
squares = [x**2 for x in range(10)]
even_nums = [x for x in range(20) if x % 2 == 0]
```

### Tuples

```python
# Creating tuples (immutable)
coordinates = (10, 20)
person = ("John", 30, "New York")

# Accessing elements (like lists)
print(coordinates[0])  # 10
x, y = coordinates     # Unpacking

# Tuple methods
count = person.count("John")  # Count occurrences
index = person.index(30)      # Find index
```

### Dictionaries

```python
# Creating dictionaries
person = {"name": "John", "age": 30, "city": "New York"}
empty_dict = {}

# Accessing elements
print(person["name"])         # "John"
print(person.get("age"))      # 30
print(person.get("gender", "Not specified"))  # Default if key not found

# Modifying dictionaries
person["email"] = "john@example.com"  # Add or update
person.update({"age": 31, "phone": "123-456-7890"})
del person["city"]            # Delete key-value pair
age = person.pop("age")       # Remove and return value
person.clear()                # Remove all items

# Dictionary methods
keys = person.keys()          # View of keys
values = person.values()      # View of values
items = person.items()        # View of (key, value) tuples

# Dictionary comprehension
squares = {x: x**2 for x in range(6)}
```

### Sets

```python
# Creating sets (unordered collections of unique elements)
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 3, 2, 1])  # Convert list to set: {1, 2, 3}

# Set operations
fruits.add("orange")          # Add an element
fruits.remove("banana")       # Remove element (raises error if not found)
fruits.discard("kiwi")        # Remove if present (no error)
popped = fruits.pop()         # Remove and return arbitrary element
fruits.clear()                # Remove all elements

# Set operations
set1 = {1, 2, 3}
set2 = {3, 4, 5}
union = set1 | set2           # Union: {1, 2, 3, 4, 5}
intersection = set1 & set2    # Intersection: {3}
difference = set1 - set2      # Difference: {1, 2}
sym_diff = set1 ^ set2        # Symmetric difference: {1, 2, 4, 5}

# Set comprehension
even_squares = {x**2 for x in range(10) if x % 2 == 0}
```

## Functions

### Function Basics

```python
# Defining functions
def greet(name):
    return f"Hello, {name}!"

# Calling functions
message = greet("John")  # "Hello, John!"

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Keyword arguments
message = greet(greeting="Hi", name="John")  # "Hi, John!"

# Variable number of arguments
def add_all(*args):  # Tuple of positional arguments
    return sum(args)

total = add_all(1, 2, 3, 4)  # 10

# Variable number of keyword arguments
def print_info(**kwargs):  # Dictionary of keyword arguments
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="John", age=30)  # Prints "name: John" and "age: 30"
```

### Lambda Functions

```python
# Anonymous functions
square = lambda x: x**2
print(square(5))  # 25

# Lambda with filter, map, reduce
numbers = [1, 2, 3, 4, 5]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
squared = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]

from functools import reduce
product = reduce(lambda x, y: x * y, numbers)  # 120
```

## Modules and Packages

### Importing Modules

```python
# Basic import
import math
print(math.sqrt(16))  # 4.0

# Import with alias
import math as m
print(m.sqrt(16))  # 4.0

# Import specific functions
from math import sqrt, pi
print(sqrt(16))  # 4.0
print(pi)  # 3.141592653589793

# Import all functions (not recommended)
from math import *
```

### Creating Modules

```python
# File: mymodule.py
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159

# In another file
import mymodule
print(mymodule.greet("John"))  # "Hello, John!"
print(mymodule.PI)  # 3.14159
```

## File Operations

### Reading Files

```python
# Basic file reading
with open("file.txt", "r") as file:
    content = file.read()  # Read entire file
    
# Reading line by line
with open("file.txt", "r") as file:
    for line in file:
        print(line.strip())
        
# Reading lines into a list
with open("file.txt", "r") as file:
    lines = file.readlines()
```

### Writing Files

```python
# Writing to a file
with open("output.txt", "w") as file:
    file.write("Hello, World!")
    
# Appending to a file
with open("output.txt", "a") as file:
    file.write("\nMore text.")
```

## Error Handling

### Try-Except Blocks

```python
# Basic exception handling
try:
    num = int("abc")
except ValueError:
    print("Invalid conversion")

# Handling multiple exceptions
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero")
except (TypeError, ValueError):
    print("Type or value error")
    
# With else and finally
try:
    num = int("123")
except ValueError:
    print("Invalid conversion")
else:
    print("Conversion successful")  # Executed if no exception
finally:
    print("Always executed")  # Always executed
```

### Raising Exceptions

```python
# Raise an exception
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
    
# Custom exceptions
class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
```

## Classes and Objects

### Basic Class Definition

```python
# Define a class
class Person:
    # Class attribute
    species = "Homo sapiens"
    
    # Constructor method
    def __init__(self, name, age):
        # Instance attributes
        self.name = name
        self.age = age
        
    # Instance method
    def greet(self):
        return f"Hello, my name is {self.name}"
    
    # String representation
    def __str__(self):
        return f"{self.name}, {self.age} years old"
        
# Create an instance
john = Person("John", 30)
print(john.name)        # "John"
print(john.greet())     # "Hello, my name is John"
print(john)             # "John, 30 years old"
```

### Inheritance

```python
# Base class
class Animal:
    def __init__(self, name):
        self.name = name
        
    def speak(self):
        pass

# Derived class
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"
        
class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"
        
# Create instances
dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())  # "Rex says Woof!"
print(cat.speak())  # "Whiskers says Meow!"
```

## Common Libraries

### Standard Library

```python
# datetime - working with dates and times
import datetime
now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# random - random numbers and selections
import random
num = random.randint(1, 10)       # Random integer between 1 and 10
choice = random.choice([1, 2, 3]) # Random element from list

# os - operating system interfaces
import os
files = os.listdir(".")           # List files in current directory
path = os.path.join("dir", "file") # Join path components
```

### Data Science Libraries

```python
# NumPy - numerical computing
import numpy as np
arr = np.array([1, 2, 3])
mean = np.mean(arr)
matrix = np.zeros((3, 3))

# Pandas - data analysis
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
csv_data = pd.read_csv("data.csv")

# Matplotlib - data visualization
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.title("Simple Plot")
plt.show()
```

## List Comprehensions and Generators

### List Comprehensions (Advanced)

```python
# Nested list comprehension
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Conditional list comprehension
even_sqrs = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Dict comprehension
word = "hello"
char_count = {char: word.count(char) for char in word}
# {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### Generators

```python
# Generator function
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

# Using the generator
counter = count_up_to(5)
print(next(counter))  # 1
print(next(counter))  # 2

# Generator expression
squares = (x**2 for x in range(5))
print(list(squares))  # [0, 1, 4, 9, 16]
```

## Advanced Features

### Decorators

```python
# Decorator function
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} took {time.time() - start:.2f} seconds")
        return result
    return wrapper

# Using decorator
@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

# Call the decorated function
result = slow_function()
```

### Context Managers

```python
# Using with statement (built-in context manager)
with open("file.txt", "r") as file:
    content = file.read()

# Custom context manager
class MyContext:
    def __enter__(self):
        print("Entering context")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context")
        
# Using custom context manager
with MyContext() as ctx:
    print("Inside context")
```

### Type Hints (Python 3.5+)

```python
# Basic type hints
def greeting(name: str) -> str:
    return f"Hello, {name}"
    
# Type hints for collections
from typing import List, Dict, Tuple, Optional

def process_items(items: List[int]) -> Dict[int, str]:
    return {item: str(item) for item in items}
    
def get_coordinates() -> Tuple[int, int]:
    return (10, 20)
    
def find_user(id: int) -> Optional[str]:
    # May return None
    users = {1: "Alice", 2: "Bob"}
    return users.get(id)
```

## Conclusion

This guide provides a comprehensive overview of Python's syntax, features, and best practices. By understanding these concepts, you can start building your own applications and exploring the vast ecosystem of Python libraries and frameworks. Happy coding!

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Python Package Index (PyPI)](https://pypi.org/)

Feel free to reach out if you have any questions or need further assistance!
