## [Python - List Comprehension - W3Schools](https://www.w3schools.com/python/python_lists_comprehension.asp)
**Snippet:** Python Tutorial Python HOME Python Intro Python Get Started Python Syntax Python Comments Python Variables. ... List Comprehension. List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list. Example: Based on a list of fruits, you want a new list, containing only the fruits with the ...

**Cleaned Text:**
Python - List Comprehension

List Comprehension

List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.

Example:

Based on a list of fruits, you want a new list, containing only the fruits with the letter "a" in the name.

Without list comprehension you will have to write a for statement with a conditional test inside:

Example fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = []



for x in fruits:

if "a" in x:

newlist.append(x)



print(newlist) Try it Yourself »

With list comprehension you can do all that with only one line of code:

Example fruits = ["apple", "banana", "cherry", "kiwi", "mango"]



newlist = [x for x in fruits if "a" in x]



print(newlist) Try it Yourself »

The Syntax

newlist = [expression for item in iterable if condition == True]

The return value is a new list, leaving the old list unchanged.

Condition

The condition is like a filter that only accepts the items that evaluate to True .

Example Only accept items that are not "apple": newlist = [x for x in fruits if x != "apple"] Try it Yourself »

The condition if x != "apple" will return True for all elements other than "apple", making the new list contain all fruits except "apple".

The condition is optional and can be omitted:

Example With no if statement: newlist = [x for x in fruits] Try it Yourself »

Iterable

The iterable can be any iterable object, like a list, tuple, set etc.

Example You can use the range() function to create an iterable: newlist = [x for x in range(10)] Try it Yourself »

Same example, but with a condition:

Example Accept only numbers lower than 5: newlist = [x for x in range(10) if x < 5] Try it Yourself »

Expression

The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list:

Example Set the values in the new list to upper case: newlist = [x.upper() for x in fruits] Try it Yourself »

You can set the outcome to whatever you like:

Example Set all values in the new list to 'hello': newlist = ['hello' for x in fruits] Try it Yourself »

The expression can also contain conditions, not like a filter, but as a way to manipulate the outcome:

Example Return "orange" instead of "banana": newlist = [x if x != "banana" else "orange" for x in fruits] Try it Yourself »

The expression in the example above says:

"Return the item if it is not banana, if it is banana return orange".

---

## [Python List Comprehensions - Python Tutorial](https://www.pythontutorial.net/python-basics/python-list-comprehensions/)
**Snippet:** Summary: in this tutorial, you'll learn about Python List comprehensions that allow you to create a new list from an existing one. Introduction to Python list comprehensions # In programming, you often need to transform elements of a list and return a new list. For example, suppose that you have a list of five numbers like this:

**Cleaned Text:**
Summary: in this tutorial, you’ll learn about Python List comprehensions that allow you to create a new list from an existing one.

Introduction to Python list comprehensions #

In programming, you often need to transform elements of a list and return a new list.

For example, suppose that you have a list of five numbers like this:

numbers = [ 1 , 2 , 3 , 4 , 5 ] Code language: Python ( python )

And you want to get a list of squares based on this numbers list

The straightforward way is to use a for loop:

numbers = [ 1 , 2 , 3 , 4 , 5 ] squares = [] for number in numbers: squares.append(number** 2 ) print(squares) Code language: Python ( python )

Try it

Output:

[ 1 , 4 , 9 , 16 , 25 ] Code language: JSON / JSON with Comments ( json )

In this example, the for loop iterates over the elements of the numbers list, squares each number and adds the result to the squares list.

Note that a square number is the product of the number multiplied by itself. For example, square number 2 is 2*2 = 4, square number of 3 is 3*3 = 9, and so on.

To make the code more concise, you can use the built-in map() function with a lambda expression:

numbers = [ 1 , 2 , 3 , 4 , 5 ] squares = list(map( lambda number: number** 2 , numbers)) print(squares) Code language: Python ( python )

Try it

Output:

[ 1 , 4 , 9 , 16 , 25 ] Code language: JSON / JSON with Comments ( json )

Since the map() function returns an iterator, you need to use the list() function to convert the iterator to a list.

Both the for loop and map() function can help you create a new list based on an existing one. But the code isn’t really concise and beautiful.

To help you create a list based on the transformation of elements of an existing list, Python provides a feature called list comprehensions.

The following shows how to use list comprehension to make a list of squares from the numbers list:

numbers = [ 1 , 2 , 3 , 4 , 5 ] squares = [number** 2 for number in numbers] print(squares) Code language: Python ( python )

Try it

Output:

[ 1 , 4 , 9 , 16 , 25 ] Code language: JSON / JSON with Comments ( json )

And here’s the list comprehension part:

squares = [number** 2 for number in numbers] Code language: Python ( python )

A list comprehension consists of the following parts:

An input list ( numbers )

) A variable that represents the elements of the list ( number )

) An output expression ( number**2 ) that returns the elements of the output list from the elements of the input list.

The following shows the basic syntax of the Python list comprehension:

[output_expression for element in list] Code language: Python ( python )

It’s equivalent to the following:

output_list = [] for element in list: output_list.append(output_expression) Code language: Python ( python )

Python list comprehension with if condition #

The following shows a list of the top five highest mountains on Earth:

mountains = [ [ 'Makalu' , 8485 ], [ 'Lhotse' , 8516 ], [ 'Kanchendzonga' , 8586 ], [ 'K2' , 8611 ], [ 'Everest' , 8848 ] ] Code language: Python ( python )

To get a list of mountains where the height is greater than 8600 meters, you can use a for loop or the filter() function with a lambda expression like this:

mountains = [ [ 'Makalu' , 8485 ], [ 'Lhotse' , 8516 ], [ 'Kanchendzonga' , 8586 ], [ 'K2' , 8611 ], [ 'Everest' , 8848 ] ] highest_mountains = list(filter( lambda m: m[ 1 ] > 8600 , mountains)) print(highest_mountains) Code language: Python ( python )

Try it

Output:

[[ 'K2' , 8611 ], [ 'Everest' , 8848 ]] Code language: Python ( python )

Like the map() function, the filter() function returns an iterator. Therefore, you need to use the list() function to convert the iterator to a list.

Python List comprehensions provide an optional predicate that allows you to specify a condition for the list elements to be included in the new list:

[output_expression for element in list if condition] Code language: Python ( python )

This list comprehension allows you to replace the filter() with a lambda expression:

mountains = [ [ 'Makalu' , 8485 ], [ 'Lhotse' , 8516 ], [ 'Kanchendzonga' , 8586 ], [ 'K2' , 8611 ], [ 'Everest' , 8848 ] ] highest_mountains = [m for m in mountains if m[ 1 ] > 8600 ] print(highest_mountains) Code language: Python ( python )

Try it

Output:

[[ 'K2' , 8611 ], [ 'Everest' , 8848 ]] Code language: Python ( python )

Python list comprehensions allow you to create a new list from an existing one.

Use list comprehensions instead of map() or filter() to make your code more concise and readable.

---

## [Python List Comprehension: Tutorial With Examples](https://python.land/deep-dives/list-comprehension)
**Snippet:** Alternatives to list comprehensions. The Python language could do without comprehensions; it would just not look as beautiful. Using functional programming functions like map() and reduce() can do everything a list comprehension can.. Another alternative is using for-loops.If you're coming from a C-style language, like Java, you'll be tempted to use for loops.

**Cleaned Text:**
There’s a concept called set-builder notation in mathematics, also called set comprehension. Inspired by this principle, Python offers list comprehensions. In fact, Python list comprehensions are one of the defining features of the language. It allows us to create concise, readable code that outperforms the uglier alternatives like for loops or using map() .

We’ll first look at the most well-known type: list comprehensions. Once we’ve got a good grasp of how they work, you’ll also learn about set comprehensions and dictionary comprehensions.

What are list comprehensions?

A Python list comprehension is a language construct. It’s used to create a Python list based on an existing list. Sounds a little vague, but after a few examples, that ‘ah-ha!’ moment will follow, trust me.

The basic syntax of a list comprehension is:

[ <expression> for item in list if <conditional> ]

The ‘if’-part is optional, as you’ll discover soon. However, we do need a list to start from. Or, more specifically, anything that can be iterated. We’ll use Python’s range() function, which is a special type of iterator called a generator: it generates a new number on each iteration.

Examples of list comprehensions

Enough theory, let’s look at the most basic example, and I encourage you to fire up a Python REPL to try this yourself:

>>> [x for x in range(1, 5)] [1, 2, 3, 4]

Some observations:

The expression part is just x

part is just Instead of a list, we use the range() function. We can use [1, 2, 3, 4] too, but using range() is more efficient and requires less typing for longer ranges.

The result is a list of elements, obtained from range(). Not very useful, but we did create our first Python list comprehension. We could just as well use:

>>> list(range(1,5)) [1, 2, 3, 4]

So let’s throw in that if-statement to make it more useful:

>>> [x for x in range(1,10) if x % 2 == 0] [2, 4, 6, 8]

The if-part acts like a filter. If the condition after the if resolves to True, the item is included. If it resolves to False, it’s omitted. This way, we can get only the even numbers using a list comprehension.

So far, our expression (the x ) has been really simple. Just to make this absolutely clear though, expression can be anything that is valid Python code and is considered an expression. Example:

>>> [x + 4 for x in [10, 20]] [14, 24]

This expression adds four to x, which is still quite simple. But we could also have done something more complicated, like calling a function with x as the argument:

def some_function(a): return (a + 5) / 2 m = [some_function(x) for x in range(8)] print(m) # [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

More advanced examples

You mastered the basics; congrats! Let’s continue with some more advanced examples.

Nested list comprehension

If expression can be any valid Python expression, it can also be another list comprehension. This can be useful when you want to create a matrix:

>>> m = [[j for j in range(3)] for i in range(4)] >>> m [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]

Or, if you want to flatten the previous matrix:

>>> [value for sublist in m for value in sublist] [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]

The same, but with some more whitespace to make this clearer:

>>> [value for sublist in m for value in sublist] [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]

The first part loops over the matrix m . The second part loops over the elements in each vector.

Alternatives to list comprehensions

The Python language could do without comprehensions; it would just not look as beautiful. Using functional programming functions like map() and reduce() can do everything a list comprehension can.

Another alternative is using for-loops. If you’re coming from a C-style language, like Java, you’ll be tempted to use for loops. Although it’s not the end of the world, you should know that list comprehensions are more performant and considered a better coding style.

Other comprehensions

If there are list comprehensions, why not create dictionary comprehension as well? Or what about set comprehensions? As you might expect, both exist.

Set comprehensions

The syntax for a Python set comprehension is not much different. We just use curly braces instead of square brackets:

{ <expression> for item in set if <conditional> }

For example:

>>> {s for s in range(1,5) if s % 2} {1, 3}

Dictionary comprehensions

A dictionary requires a key and a value. Otherwise, it’s the same trick again:

>>> {x: x**2 for x in (2, 4, 6)} {2: 4, 4: 16, 6: 36}

---

## [List Comprehension in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python-list-comprehension/)
**Snippet:** Explanation: In the above list comprehension, the iterable is a list ' a', and the expression is val * 2, which multiplies each value from the list by 2. Conditional statements in list comprehension. List comprehensions can include conditional statements to filter or modify items based on specific criteria. These conditionals help us create customized lists quickly and making the code cleaner ...

**Cleaned Text:**
List comprehension is a way to create lists using a concise syntax. It allows us to generate a new list by applying an expression to each item in an existing iterable (such as a list or range). This helps us to write cleaner, more readable code compared to traditional looping techniques.

For example, if we have a list of integers and want to create a new list containing the square of each element, we can easily achieve this using list comprehension.

Python a = [ 2 , 3 , 4 , 5 ] res = [ val ** 2 for val in a ] print ( res )



Output [4, 9, 16, 25]

Syntax of list comprehension

[expression for item in iterable if condition]

expression: The transformation or value to be included in the new list.

item: The current element taken from the iterable.

iterable: A sequence or collection (e.g., list, tuple, set).

if condition (optional): A filtering condition that decides whether the current item should be included.

This syntax allows us to combine iteration, modification, and conditional filtering all in one line.

for loop vs. list comprehension

The main difference is that a for loop requires multiple lines to create a new list by iterating over items and manually adding each one. Whereas, list comprehension do the same task in a single line, this makes the code simpler and easier to read.

Example: Let's take an example, where we want to double each number of given list into a new list

Using a for loop:

Python a = [ 1 , 2 , 3 , 4 , 5 ] # Create an empty list 'res' to store results res = [] # Iterate over each element in list 'a' for val in a : # Multiply each element by 2 and append it to 'res' res . append ( val * 2 ) print ( res )



Output [2, 4, 6, 8, 10]

Explanation: Create an empty list 'res' to store results and iterate over each element in list 'a' and for each items in list 'a', multiply it by 2 and append it to 'res' using append() method.

Using list comprehension:

Python a = [ 1 , 2 , 3 , 4 , 5 ] res = [ val * 2 for val in a ] print ( res )



Output [2, 4, 6, 8, 10]

Explanation: In the above list comprehension, the iterable is a list 'a', and the expression is val * 2, which multiplies each value from the list by 2.

Conditional statements in list comprehension

List comprehensions can include conditional statements to filter or modify items based on specific criteria. These conditionals help us create customized lists quickly and making the code cleaner and more efficient.

Example: Suppose we want to filter all even list from the given list.

Python a = [ 1 , 2 , 3 , 4 , 5 ] res = [ val for val in a if val % 2 == 0 ] print ( res )



Output [2, 4]

To learn more about filtering conditions in list comprehensions, please refer to "Python List Comprehension Using If-Else"

Examples of list comprehension

Creating a list from a range

A simple example is creating a list of numbers from 0 to 9.

Python # Creates a list of numbers from 0 to 9 a = [ i for i in range ( 10 )] print ( a )



Output [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Using nested loops

List comprehension can also be used with nested loops. Here, we generate a list of coordinate pairs for a simple 3x3 grid.

Python # Creates a list of tuples representing all combinations of (x, y) # where both x and y range from 0 to 2. coordinates = [( x , y ) for x in range ( 3 ) for y in range ( 3 )] print ( coordinates )



Output [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

Flattening a list of lists

Suppose we have a list of lists and we want to convert it into a single list.

Python mat = [[ 1 , 2 , 3 ], [ 4 , 5 , 6 ], [ 7 , 8 , 9 ]] res = [ val for row in mat for val in row ] print ( res )



Output [1, 2, 3, 4, 5, 6, 7, 8, 9]

Explanation: The line [val for row in mat for val in row] uses nested list comprehension to iterate through each row in mat. For each row, it iterates through each val in that row and collecting all values into a single list.

Related Articles:

---

## [When to Use a List Comprehension in Python](https://realpython.com/list-comprehension-python/)
**Snippet:** Every list comprehension in Python includes three elements: expression is the member itself, a call to a method, or any other valid expression that returns a value. In the example above, the expression number * number is the square of the member value.; member is the object or value in the list or iterable. In the example above, the member value is number.

**Cleaned Text:**
Almost there! Complete this form and click the button below to gain instant access:

---
