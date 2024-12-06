# **Contents of This Repository**

This repository contains the **rectinter** tool to solve the problems of one- and two-set rectangles intersection, originally presented in *"An Optimal Worst Case Algorithm for Reporting Intersections of Rectangles"* by **J. L. Bentley and D. Wood**.

For a list of rectilinear rectangles represented by the coordinates of their lower-left and upper-right corners, it returns a list of rectangles that intersect each rectangle in the list.

---

# **Installation**

To use the software provided in this repository, you will need a working Python3 distribution installed on your computer.

### **Clone the Repository**
The simplest way to install **rectinter** is to use the `git` command-line tool. Run the following command:

```bash
git clone https://github.com/sg406651/rectinter.git
```
# **Usage**

To use **rectinter** after package installation simply import two functions:
```bash
from rectinter import rectinter_one_set, rectinter_two_sets
```

Input rectangles should have a format **(x1,y1,x2,y2)**, (x1,y1) representing lower-left and (x2,y2) representing upper-right corner of the rectangle.
Both functions support input in the form of **tuples** or **NumPy** arrays.

**rectinter_one_set** takes one argument: list of rectangles with the **(x1,y1,x2,y2)** format and returns a list of the same size, where for each index it contains the list of indexes of the rectangles intersecting given rectangle.

**rectinter_two_sets** takes two arguments: two lists of rectangles with the **(x1,y1,x2,y2)** format and returns two lists of the size equal to the starting lists, where for each index it contains the list of the indexes of the rectangles from the opposite set intersecting given rectangle.

# **Performance**
![Time performance of the rectinter compared to naive approach using pairwise comparison](time_complexity_new.png)
