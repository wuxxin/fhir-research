site: [Python List Comprehension: Tutorial With Examples](https://python.land/deep-dives/list-comprehension)
snippet: |
  Learn how to use list comprehensions, a powerful syntax that allows you to create a list from another list. See examples of basic and advanced list comprehensions, as well as set and dictionary comprehensions.
text: |
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

site: [List Comprehension in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python-list-comprehension/)
snippet: |
  Explanation: In the above list comprehension, the iterable is a list ' a', and the expression is val * 2, which multiplies each value from the list by 2. Conditional statements in list comprehension. List comprehensions can include conditional statements to filter or modify items based on specific criteria. These conditionals help us create customized lists quickly and making the code cleaner ...
text: |
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

site: [Python List Comprehension (With Examples) - Programiz](https://www.programiz.com/python-programming/list-comprehension)
snippet: |
  Learn how to use list comprehension to create a new list based on the values of an existing list. See examples of list comprehension with for loop, if statement, nested loop, string and more.
text: |
  List comprehension offers a concise way to create a new list based on the values of an existing list.

  Suppose we have a list of numbers and we desire to create a new list containing the double value of each element in the list.

  numbers = [1, 2, 3, 4] # list comprehension to create new list doubled_numbers = [num * 2 for num in numbers] print(doubled_numbers)

  Output

  [2, 4, 6, 8]

  Here is how the list comprehension works: Python List Comprehension

  Syntax of List Comprehension

  [expression for item in list if condition == True]

  Here,

  for every item in list , execute the expression if the condition is True .

  Note: The if statement in list comprehension is optional.

  for Loop vs. List Comprehension

  List comprehension makes the code cleaner and more concise than for loop.

  Let's write a program to print the square of each list element using both for loop and list comprehension.

  for Loop

  numbers = [1, 2, 3, 4, 5] square_numbers = [] # for loop to square each elements for num in numbers: square_numbers.append(num * num) print(square_numbers) # Output: [1, 4, 9, 16, 25]

  List Comprehension

  numbers = [1, 2, 3, 4, 5] # create a new list using list comprehension square_numbers = [num * num for num in numbers] print(square_numbers) # Output: [1, 4, 9, 16, 25]

  It's much easier to understand list comprehension once you know Python for loop().

  Conditionals in List Comprehension

  List comprehensions can utilize conditional statements like if…else to filter existing lists.

  Let's see an example of an if statement with list comprehension.

  # filtering even numbers from a list even_numbers = [num for num in range(1, 10) if num % 2 == 0 ] print(even_numbers) # Output: [2, 4, 6, 8]

  Here, list comprehension checks if the number from range(1, 10) is even or odd. If even, it appends the number in the list.

  Note: The range() function generates a sequence of numbers. To learn more, visit Python range().

  if...else With List Comprehension Let's use if...else with list comprehension to find even and odd numbers. numbers = [1, 2, 3, 4, 5, 6] # find even and odd numbers even_odd_list = ["Even" if i % 2 == 0 else "Odd" for i in numbers] print(even_odd_list) Output ['Odd', 'Even', 'Odd', 'Even', 'Odd', 'Even'] Here, if an item in the numbers list is divisible by 2, it appends Even to the list even_odd_list . Else, it appends Odd . Nested if With List Comprehension Let's use nested if with list comprehension to find even numbers that are divisible by 5. # find even numbers that are divisible by 5 num_list = [y for y in range(100) if y % 2 == 0 if y % 5 == 0] print(num_list) Output [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] Here, list comprehension checks two conditions: if y is divisible by 2 or not. if yes, is y divisible by 5 or not. If y satisfies both conditions, the number appends to num_list .

  Example: List Comprehension with String

  We can also use list comprehension with iterables other than lists.

  word = "Python" vowels = "aeiou" # find vowel in the string "Python" result = [char for char in word if char in vowels] print(result) # Output: ['o']

  Here, we used list comprehension to find vowels in the string 'Python' .
---

site: [Python - List Comprehension - W3Schools](https://www.w3schools.com/python/python_lists_comprehension.asp)
snippet: |
  Learn how to create a new list based on the values of an existing list using list comprehension. See examples of how to use expression, condition, iterable and syntax in list comprehension.
text: |
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
