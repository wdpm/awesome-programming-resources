# TODO



## [?] 格式更加精简的可折叠列表

### 需求描述

将下面这个格式

```markdown
- [Functional-Light JavaScript](https://book.douban.com/subject/35002560/) - JavaScript 中平衡、实用的 FP。`year:2017` `page:388` `topic: functional programming` `level: medium`
```

转化为

```html
<details>
<summary>
 <a href="https://book.douban.com/subject/35002560/">Functional-Light JavaScript</a>
</summary>
JavaScript 中平衡、实用的 FP。<code>year:2017</code> <code>page:388</code> <code>topic: functional programming</code> <code>level: medium</code>
</details>
```



### 实现思路

列表项源格式：
```markdown
- [book_title](book_link) - book_comment [year:XXXX] [page:XXX] [topic:XXXX] [level:XXXX]
```
列表项渲染格式：
```html
<details>
<summary>
 <a href="{{book_link}}">{{book_title}}</a>
</summary>
{{book_comment}} <code>year:{{year}}</code> <code>page:{{page}}</code> <code>topic:{{topic}}</code> <code>level:{{level}}</code>
</details>
```

可以使用python jinjia2模版库来处理。f string也是可行的处理方案。