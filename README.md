# Coach Arrivals Project
A console based program that allows you to record how late busses were.  This is a solution to a GCSE problem that I used to improve my understanding of classes and dictionaries in python
Further documentation can be found [here](https://docs.google.com/document/d/e/2PACX-1vQKVWmQGtpmhX1jTdl5E3d4Hi5IYfJa-jIwjthXTRnsBovn3Uz3-hagJK0jLc3iPtYF0kDgjh_95qWI/pub)
This project took approximately an afternoon of coding.  Areas for improvment include:
- The class structure should have used a single class for the arrivals table and then used a nested dict instead of a nested class with a dict as a class attribute.  This would have allowed the data to be exported to JSON.  As it is the object is serialised.
- I feel that there is too much integration of the interface and the data structure.  If I was to repeat this project I would place the class of coach arrivals in a separate module.
- The code is not self documenting: my next project will need to conform to the pep 8 standards.
