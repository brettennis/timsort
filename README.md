# Timsort

Timsort is a sorting algorithm created by Tim Peters for use in Python in 2001. The algorithm is a combination of Merge Sort and Insertion Sort. Learn more about how Timsort works in [this blog](https://medium.com/@rylanbauermeister/understanding-timsort-191c758a42f3).

This particular implementation sorts a list of 10,000 points on a plane in a counterclockwise fashion. For example, the point `(2,1)` is considered less than `(1,2)`. 

Type to the command line ``make run`` for a quick demo. ``input-points.txt`` is the unsorted list of points, and the sorted output is ``out-sorted.txt``.
