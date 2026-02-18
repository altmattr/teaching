# java_proficiency_01
Write a program which will print the first 10 fibonacci numbers to the console.

```template
function foo(){
  // do something
}

console.log(foo());
```

```solution
// I've gone for the ugliest possible model solution
function foo(i, j){
  console.log(i);
  if (i > 50) return;
  foo(j, i + j);
}
foo(1,1);
```

