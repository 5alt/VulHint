# VulHint

VulHint 是一款 sublime text 3 的代码审计插件。

插件包含一些预置的正则规则和提示的内容，在当前文本中匹配到代码的时候，会加框显示，鼠标移动到危险函数的时候，会展示提示信息。

在代码审计的时候，本插件可以针对相关知识点做出提醒。

## 漏洞提示

在编辑器行号前有标记符号，对规则匹配到的部分用方框标出。鼠标移动到该行会有相应提示。如果一行中有多个标记，则所有的提示信息都会出现，鼠标移动到某一个上则只会出现该规则的提示。

`alt+space` 可以切换到下一个提示点。

## 数据扩展

`VulData.sublime-settings` 中存放了相关的规则数据，可以方便的自行添加。

语言类型按照文件后缀名判断。每种语言类型下有不同的规则。

规则的格式为。
```
"rule_name": {"keyword":[], "discription": "test", "pattern": "regexp", bbais, ebias}
```

其中
* keyword 鼠标悬浮位置
* discription 悬浮显示内容，html显示
* pattern 正则表达式
* abais 开始处偏移
* bbais 结尾处偏移
* enable 是否启用该条规则

本插件已经内置了php的一些规则，欢迎大家提交新的规则以及对现有规则进行优化。

## License

MIT

## 联系

http://5alt.me

md5_salt [AT] qq.com

## 参考资料

Seay代码审计系统

https://www.sublimetext.com/docs/3/api_reference.html

https://cnpagency.com/blog/creating-sublime-text-3-plugins-part-1/

https://github.com/bradrobertson/sublime-packages

http://zxhfighter.github.io/blog/javascript/2013/07/30/sublime-plugin.html

