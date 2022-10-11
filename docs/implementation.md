# 实现

## 格式更加精简的可折叠列表

### 需求描述

将下面这个格式

```markdown
[Functional-Light JavaScript](https://book.douban.com/subject/35002560/)

JavaScript 中平衡、实用的 FP。`y2017` `p388` `ll`
```

转化为

```html

<details>
    <summary>
        <a href="https://book.douban.com/subject/35002560/">Functional-Light JavaScript</a>
    </summary>
    JavaScript 中平衡、实用的 FP。<code>year:2017</code> <code>page:388</code> <code>level: medium</code>
</details>
```

显示效果：

<details>
<summary>
 <a href="https://book.douban.com/subject/35002560/">Functional-Light JavaScript</a>
</summary>
JavaScript 中平衡、实用的 FP。<code>year:2017</code> <code>page:388</code> <code>level: medium</code>
</details>

### 实现思路

markdown 解析的几种方案：

- 使用合适的 markdown parser 将原始的 markdown 解析为 AST。推荐此方式。
- 使用正则表达式来进行模式匹配，进行挑选。

---

列表项源格式：

```markdown
[book_title](book_link)

book_comment。other sentence。 [yXXXX] [pXXX] [LL] [TB]
```

列表项渲染格式：

```html

<details>
    <summary>
        <a href="{{book_link}}">{{book_title}}</a>
    </summary>
    {{book_comment}} <code>year:{{year}}</code> <code>page:{{page}}</code> <code>level:{{level}}</code>
</details>
```

显示效果：

<details>
<summary>
 <a href="{{book_link}}">{{book_title}}</a>
</summary>
{{book_comment}} <code>year:{{year}}</code> <code>page:{{page}}</code> <code>level:{{level}}</code>
</details>

### 实现细节

我们不关心标题元素，只关心段落元素。

```
{
  'type': 'Paragraph',
  'children': [
    {
      'type': 'Link',
      'target': 'https://book.douban.com/subject/26677354/',
      // link
      'title': '',
      'children': [
        {
          'type': 'RawText',
          'content': '数学女孩'
          // 名称
        }
      ]
    }
  ]
}
```

```
{
  'type': 'Paragraph',
  'children': [
    {
      'type': 'RawText',
      'content': '梦开始的地方。其实是披着小说外衣的数学证明题集，但有着一种独特的浪漫。可能这就是轻小说的魅力吧。' // 描述
    },
    {
      'type': 'InlineCode',
      'children': [
        {
          'type': 'RawText',
          'content': 'y2016' // 年份
        }
      ]
    },
    {
      'type': 'RawText',
      'content': ' '
    },
    {
      'type': 'InlineCode',
      'children': [
        {
          'type': 'RawText',
          'content': 'p327' // 页数
        }
      ]
    },
    {
      'type': 'RawText',
      'content': ' '
    },
    {
      'type': 'InlineCode',
      'children': [
        {
          'type': 'RawText',
          'content': 'LL' // 等级 / 难度
        }
      ]
    }
  ]
}
```

确认中间结果的解析正常：

```
item: {'type': 'Heading', 'level': 1, 'children': [{'type': 'RawText', 'content': 'awesome-programming-resources'}]}
item: {'type': 'Heading', 'level': 2, 'children': [{'type': 'RawText', 'content': 'Math'}]}
item: {'type': 'Heading', 'level': 3, 'children': [{'type': 'RawText', 'content': 'novel'}]}
current_list_item: <ListItem: 数学女孩:https://book.douban.com/subject/26677354/: 梦开始的地方。其实是披着小说外衣的数学证明题集，但有着一种独特的浪漫。可能这就是轻小说的魅力吧。:['y2016', 'p327', 'LL']>
item: {'type': 'ThematicBreak'}
current_list_item: <ListItem: 数学女孩 2:https://book.douban.com/subject/26681597/: 第二季。守关 BOSS 是费马大定理。:['y2015', 'p368', 'LH']>
item: {'type': 'ThematicBreak'}
current_list_item: <ListItem: 数学女孩 3:https://book.douban.com/subject/27193490/: 第三季。守关 BOSS 是哥德尔不完备定理。:['y2017', 'p406', 'LH']>
item: {'type': 'ThematicBreak'}
current_list_item: <ListItem: 数学女孩 4:https://book.douban.com/subject/33444625/: 第四季。主要讲随机算法。:['y2019', 'p504', 'LL']>
item: {'type': 'Heading', 'level': 3, 'children': [{'type': 'RawText', 'content': 'academics'}]}
current_list_item: <ListItem: 数学分析八讲（修订版）:https://book.douban.com/subject/26593890/: 一份简洁的数学分析介绍。:['Y2015', 'P175', 'LM']>
item: {'type': 'Heading', 'level': 2, 'children': [{'type': 'RawText', 'content': 'Version Control System'}]}
current_list_item: <ListItem: 精通 Git（第 2 版）:https://book.douban.com/subject/27133267/:Git 版本控制的入门书，由浅入深，可以酌情阅读。:['y2017', 'p420', 'LL']>
item: {'type': 'ThematicBreak'}
item: {'type': 'Heading', 'level': 2, 'children': [{'type': 'RawText', 'content': 'App Development'}]}
item: {'type': 'Heading', 'level': 3, 'children': [{'type': 'RawText', 'content': 'Desktop App'}]}
current_list_item: <ListItem: Electron in Action:https://book.douban.com/subject/30346427/: 关于 Electron 实战的一本务实落地的书籍。配套代码基本可运行。:['y2018', 'p376', 'LL']>
```

## 更多元信息挖掘
- item 数量
- item 对应的年份分布-数量
- level:count 这个map的显示