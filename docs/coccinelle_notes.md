## Coccinelle Patch Notes

### Rulename
- Isomorphisms can be disabled at this portion with `disable`. Usage:

    ```
    @rule1 disable neg_if@
    ```


### Metadecl
- The detected results from other rules could be excluded in current rule. E.g.

    ```
    position p != rule1.p; // Positions in this rule will not include positions detected in rule1
    ```

- Conversely, results can also be constrained with other rules’ results. E.g.

    ```
    identifier fun = rule01.F; // Detected identifiers here must match the results in rule01
    ```

- `COMMA_LIST` constraints can be applied to limit the range of certain metavariables (normally type, binary operator, assignment operator) at declaration. E.g.

    ```
    binary operator bop = {^, &, |}; // In this case bop will only match ^, & and |
    ```
- `regexp_constraint` filters the detected results based on the given regular expression. E.g.

    ```
    constant c !~ "^0."; // Constant c should not start with 0 constant
    c1 =~ "^0."; // Constant c must start with 0
    ```

### Metavariables
#### Commonly used metavariables:
- **Position**
- Can be attached to any token
  ```
  a + b@p   // attach @p to b
  a +@E@p b //attach @p to metavariable E
  ```
- The returned position value is an object array. Some useful elements (print with Python script):
  - File name: `p[0].file`
  - Start column: `p[0].column`
  - End column: `p[0].column_end`
  - Start line: `p[0].line`
  - End line: `p[0].line_end`

#### Expression
- Can match any piece of code defined in C99 standard. However, Coccinelle will first match the entire part on the left and only one variable or constant on the right. For example,
- C code: `a + b – c + d;`
- Coccinelle: `e1 + e2`
- Then e1 will match `a` and `a + b – c`, e2 will match `b` and `d`.
- When @E is attached to an operator (binary operator, unary operator or assignment operator), it will match the expressions containing that operator. For example,
- C code: `a + b – c + d;`
- Coccinelle: `e1 +@E e2`
- Then E will be `a + b` and `a + b – c + d`.

#### Declaration
- It matches the declaration statement of variables. The position and Coccinelle code for D could be made more flexible.
- If we want to match the code: `int c = a + b;`
- Coccinelle code can be:
  - `i. t i = v1 + v2; @D`
  - `ii. t @D i = v1 + v2; // @D can be placed almost any position`
  - `iii. v1 +@D v2`
  - `iv. v1 + v2 @D`

#### Statement
- Like declaration and expression, metavariable statement matches anything that falls within C99 standard. The detected results will include the entire statement.

#### Identifier
- Identifier can match the name of variable, macro, and function

#### Type
- Type matches any existing type as well as the type defined by typedef.
- Metavariable type could be applied to the declarations of other metavariables. For example,
  - `type t1, t2;`
  - `constant {t1} c1; //`c1` should be of type `t1``
  - `constant {t2} c2; //`c2` should be of type `t2``

#### Assignment Operator and Binary Operator
- The accepted operators can be restricted by adding a comma list:

    ```
    binary operator b = {+, -, *, /};
    ```
- However, some logical operators or bitwise operator combinations cannot be detected using this method. In such cases, it is recommended to hardcode them:
- Invalid:
  ```
  binary operator b = {&};
  e1 | e2 b@E@p e3
  ```
- Recommended:
  ```
  e1 | e2 &@E@p e2
  ```

#### Unary Operator
- The current version does not support a unary operator metavariable type, even though it is mentioned in the official documentation. Therefore, hardcoding is the only method to match unary operators.
- The symbols `+` and `-` in the first column represent `line to add` and `line to remove`, respectively. To correctly match unary operators like `+`, `-` and `++`, it is recommended to include a space or tab before them.
  ```
  ++e @E   // lexical error: invalid in a + context: @
  ++e @E  // Executes successfully
  ```

#### Dots and Dot Variants
- Simply put, `…` can represent any codes or nothing. For example, consider a function declaration:

```
t1 fun (…, t2 I, …) { … }
```
- It matches all the following functions:
- `int fun1 (int i) { return i; }`
- `int fun2 (double i1, int i2) { return i2; }`
- `int fun3 (int i1, double i2) { return i1; }`
- `int fun4 (float i1, int i2, double i3) { return i2; }`

- The pattern in `<… …>` should be matched 0 or more times. The pattern in `<+… …+>` should be matched at least once.
