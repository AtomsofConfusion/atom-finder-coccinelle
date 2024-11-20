# Using the Tool
After installation, the tool can be invoked with the following
> aoc-coccinelle

Additional arguments are supported, here is an example

> aoc-coccinelle 
    -pi "/stands for patch-input/the path to folder of .cocci patches"
    -si "/stands for source-input/the path to folder of .c source files"
    -v 0

# The Expected Output
The expected values should be the bare minimum of what Coccinelle should output. The testing mechanism works by first comparing whether the output and expected has the same amount of items. For instance, if the output has three items for line 16, whereas the expected only has two, the test should reach conclusion. 

Then the tool compares for each output, if it contains an input. For instance output = ['abc'], and expected = ['a'], here the test will pass as 'abc' contains 'a'. This is what I mean by expected should contain the "bare minimum". 

What won't work:
 - Check and remove: iterate through all items in output, if found matching expected, remove the expected from the list. Doesn't work because order can be unpredicable. ie. output = ['v1=v2+=v3', 'v1=v2+=v3', 'v2+=v3'], expected = ['v1=v2', 'v1=v2+=v3', 'v2+=v3']. In this loop, each iteration on the items in the output will check in the expected from the beginning. At the first 'v1=v2+=v3', it will check if it contains 'v1=v2', which it does. Then we will remove 'v1=v2' from the expected list. Then the second 'v1=v2+=v3' checks with 'v1=v2+=v3. The problem occurs like this. Suppose now the expected result order is slightly different from the output, where expected = ['v1=v2', 'v2+=v3', 'v1=v2+=v3']. When the loop is at the second 'v1=v2+=v3', it will remove 'v2+v3', leaving 'v2+=v3' detected as unmatched, resulting in false negative test result.

 In short, my current strategy is to run python tests first, then manually compare the outputs to make sure that Coccinelle patches are correct. The design choice is to make sure that what the python test filters out are indeed the incorrect ones (for exmaple, obvious discrepency between the number of items, or that the output looks entirely different from the expected atom). Then a maually checked is conducted to logically verify each individual output of coccinelle makes sense for that atom.
